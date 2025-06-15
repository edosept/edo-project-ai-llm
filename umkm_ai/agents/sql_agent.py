import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class SQLAgent:
    """SQL Agent for UMKM database queries"""
    
    def __init__(self):
        self.db_config = self._load_db_config()
        self.db = None
        self.llm = None
        self.agent = None
        self.memory = None
        self.query_count = 0
        self._initialize()
    
    def _load_db_config(self) -> Dict[str, str]:
        """Load database configuration from environment variables"""
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
    
    def _initialize(self):
        """Initialize the SQL agent with ConversationSummaryBufferMemory"""
        try:
            required_vars = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'OPENAI_API_KEY']
            missing_vars = [var for var in required_vars if not os.getenv(var)]
            if missing_vars:
                raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
            
            connection_string = (
                f"postgresql://{self.db_config['user']}:{self.db_config['password']}@"
                f"{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
            )
            
            self.db = SQLDatabase.from_uri(
                connection_string,
                schema="umkm",
                include_tables=["bisnis", "produk", "penjualan", "detail_penjualan", "pengeluaran", "kas_harian"]
            )
            
            self.llm = ChatOpenAI(
                model_name="gpt-4o",
                temperature=0.3,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            
            # Initialize ConversationSummaryBufferMemory
            self.memory = ConversationSummaryBufferMemory(
                llm=self.llm,
                max_token_limit=4000,
                memory_key="chat_history",
                return_messages=True,
                ai_prefix="Assistant",
                human_prefix="User"
            )
            
            system_prompt = self._get_system_prompt()
            toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
            
            self.agent = create_sql_agent(
                llm=self.llm,
                toolkit=toolkit,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=15,
                max_execution_time=180,
                agent_type="openai-tools",
                system_message=system_prompt
            )
            
            logger.info("SQL Agent with ConversationSummaryBufferMemory initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing SQL Agent: {str(e)}")
            raise
    
    def _get_system_prompt(self) -> str:
        """Load system prompt from required file"""
        with open("prompts/sql_agent_context.txt", "r", encoding="utf-8") as f:
            return f.read()
    
    def _build_context_with_memory(self, question: str) -> str:
        """Build context string with conversation summary memory"""
        try:
            # Get conversation history from memory
            chat_history = self.memory.chat_memory.messages
            
            if not chat_history:
                return question
            
            # Get summary if available
            summary = ""
            if hasattr(self.memory, 'moving_summary_buffer') and self.memory.moving_summary_buffer:
                summary = f"CONVERSATION SUMMARY: {self.memory.moving_summary_buffer}\n\n"
            
            # Get recent messages (last 4 exchanges = 8 messages)
            recent_history = chat_history[-8:]
            
            context_parts = []
            for i in range(0, len(recent_history), 2):
                if i + 1 < len(recent_history):
                    context_parts.append(f"Previous Q: {recent_history[i].content}")
                    context_parts.append(f"Previous A: {recent_history[i+1].content[:200]}...")
            
            if summary or context_parts:
                recent_context = "\n".join(context_parts) if context_parts else ""
                context = f"{summary}RECENT CONVERSATION:\n{recent_context}\n\nCURRENT QUESTION: {question}"
                return context
            
            return question
            
        except Exception as e:
            logger.error(f"Error building context with memory: {str(e)}")
            return question
    
    def _add_business_insights(self, question: str, response: str) -> str:
        """Add business insights and recommendations based on data patterns"""
        if len(response) < 50:
            return response
            
        # Check if response already has insights
        if "From what I can see" in response or "Rekomendasi:" in response or "My recommendations" in response:
            return response
        
        # Detect language from question
        is_indonesian = any(word in question.lower() for word in [
            'bagaimana', 'apa', 'berapa', 'dimana', 'kapan', 'mengapa', 'kenapa',
            'penjualan', 'bisnis', 'warung', 'pelanggan', 'pembayaran', 'produk'
        ])
        
        if is_indonesian:
            insight_prompt = f"""
Anda adalah penasihat bisnis yang membantu. Berdasarkan analisis data ini, berikan wawasan tambahan.

Analisis Data:
{response}

Tambahkan wawasan bisnis dan rekomendasi dalam bahasa Indonesia yang akan DITAMBAHKAN setelah data di atas:

Dari data yang saya lihat, [analisis pola atau tren]. Hal ini menunjukkan [wawasan praktis tentang bisnis].

Rekomendasi saya:
- [Saran konkret pertama yang dapat ditindaklanjuti]
- [Saran praktis kedua]
- [Saran ketiga jika relevan]
"""
        else:
            insight_prompt = f"""
You are a helpful business advisor. Based on this data analysis, provide additional insights.

Data Analysis:
{response}

Add natural business insights and recommendations in English that will be APPENDED to the data above:

From what I can see in the data, [natural analysis of patterns or trends]. This suggests [practical insight about the business].

My recommendations would be:
- [First concrete, actionable suggestion]
- [Second practical suggestion] 
- [Third helpful suggestion if relevant]
"""
        
        try:
            insight_response = self.llm.invoke(insight_prompt)
            # APPEND insights to original response, don't replace
            return f"{response}\n\n{insight_response.content}"
        except Exception as e:
            logger.error(f"Error adding insights: {str(e)}")
            return response
    
    def _is_incomplete_response(self, question: str, response: str) -> bool:
        """Check if response is incomplete for multi-business queries"""
        question_lower = question.lower()
        response_lower = response.lower()
        
        # Check if question asks for all businesses
        asks_for_all = any(phrase in question_lower for phrase in [
            'semua warung', 'setiap warung', 'breakdown', 'all businesses', 
            'ketiga warung', '3 warung', 'masing-masing warung', 'each business'
        ])
        
        if not asks_for_all:
            return False
        
        # Check if response mentions all 3 business names properly
        business_mentions = [
            'warung kopi gembira' in response_lower or 'kopi gembira' in response_lower,
            'warung sayur buah sehat' in response_lower or 'sayur buah sehat' in response_lower,  
            'warung sembako berkah' in response_lower or 'sembako berkah' in response_lower
        ]
        
        complete_businesses = sum(business_mentions)
        
        # Also check for generic "Bisnis 1/2/3" patterns which are wrong
        has_generic_labels = any(label in response_lower for label in [
            'bisnis 1', 'bisnis 2', 'bisnis 3'
        ])
        
        # If less than 3 businesses mentioned OR using generic labels, it's incomplete
        return complete_businesses < 3 or has_generic_labels
    
    def query(self, question: str) -> str:
        """Process a question using the SQL agent with summary memory context"""
        try:
            self.query_count += 1
            logger.info(f"Processing SQL query #{self.query_count}: {question[:50]}...")
            
            # Build context with memory
            enhanced_question = self._build_context_with_memory(question)
            
            # Get response from agent
            response = self.agent.invoke({"input": enhanced_question})
            result = response["output"]
            
            # Validate response completeness and number formatting
            if self._is_incomplete_response(question, result):
                logger.warning("Detected incomplete response, retrying...")
                retry_question = f"{enhanced_question}\n\nIMPORTANT: Use actual business names from database - 'Warung Kopi Gembira', 'Warung Sayur Buah Sehat', 'Warung Sembako Berkah'. NEVER use 'Bisnis 1/2/3'. Always JOIN with umkm.bisnis table to get nama_bisnis. ALWAYS show complete numbers with proper formatting (e.g., 283,469,657.00) and transaction counts."
                retry_response = self.agent.invoke({"input": retry_question})
                result = retry_response["output"]
            
            # Add business insights and recommendations
            final_result = self._add_business_insights(question, result)
            
            # Save to memory
            self.memory.save_context(
                {"input": question},
                {"output": final_result}
            )
            
            logger.info(f"SQL query #{self.query_count} completed successfully")
            return final_result
            
        except Exception as e:
            error_msg = f"Maaf, terjadi kesalahan saat memproses pertanyaan Anda: {str(e)}"
            logger.error(f"Error in SQL query #{self.query_count}: {str(e)}")
            return error_msg
    
    def get_memory_summary(self) -> str:
        """Get current conversation summary from memory"""
        try:
            if hasattr(self.memory, 'moving_summary_buffer') and self.memory.moving_summary_buffer:
                return self.memory.moving_summary_buffer
            return "Belum ada riwayat percakapan"
        except Exception as e:
            logger.error(f"Error getting memory summary: {str(e)}")
            return "Error mengambil ringkasan percakapan"
    
    def clear_memory(self):
        """Clear conversation memory"""
        try:
            self.memory.clear()
            self.query_count = 0
            logger.info("Conversation memory cleared")
        except Exception as e:
            logger.error(f"Error clearing memory: {str(e)}")
    
    def get_conversation_history(self) -> list:
        """Get formatted conversation history"""
        try:
            messages = self.memory.chat_memory.messages
            history = []
            for msg in messages:
                role = "User" if isinstance(msg, HumanMessage) else "Assistant"
                history.append({
                    "role": role,
                    "content": msg.content,
                    "timestamp": getattr(msg, 'timestamp', None)
                })
            return history
        except Exception as e:
            logger.error(f"Error getting conversation history: {str(e)}")
            return []
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get database connection and table information"""
        try:
            table_info = self.db.get_table_info()
            return {
                "connection_status": "Connected",
                "database": self.db_config['database'],
                "tables": table_info,
                "query_count": self.query_count,
                "memory_type": "ConversationSummaryBufferMemory",
                "memory_summary": self.get_memory_summary()
            }
        except Exception as e:
            logger.error(f"Error getting database info: {str(e)}")
            return {
                "connection_status": "Error",
                "error": str(e),
                "query_count": self.query_count
            }
    
    def validate_connection(self) -> bool:
        """Validate database connection"""
        try:
            test_query = "SELECT COUNT(*) FROM umkm.penjualan WHERE DATE(tanggal_transaksi) = '2024-06-01'"
            result = self.db.run(test_query)
            logger.info(f"Database validation result: {result}")
            return bool(result)
        except Exception as e:
            logger.error(f"Database connection validation failed: {str(e)}")
            return False