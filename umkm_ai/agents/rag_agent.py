import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

class RAGAgent:
    """
    RAG Agent for UMKM business advice and general conversation.
    Provides business guidance, tips, and strategies for Indonesian UMKM owners.
    """
    
    def __init__(self):
        self.llm = None
        self.memory = None
        self.knowledge_base = {}
        self.response_count = 0
        self._initialize()
    
    def _initialize(self):
        """Initialize the RAG agent with ConversationSummaryBufferMemory"""
        try:
            # Validate required environment variables
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("Missing required environment variable: OPENAI_API_KEY")
            
            # Initialize LLM
            self.llm = ChatOpenAI(
                model_name="gpt-4o",
                temperature=0.7,
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
            
            # Load knowledge base
            self._load_knowledge_base()
            
            logger.info("RAG Agent with ConversationSummaryBufferMemory initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing RAG Agent: {str(e)}")
            raise
    
    def _load_knowledge_base(self):
        """Load UMKM-specific knowledge base from prompts folder"""
        try:
            # Load base context from prompts folder
            with open("prompts/base_context.txt", "r", encoding="utf-8") as f:
                base_context = f.read()
            
            self.knowledge_base = {
                "base_context": base_context
            }
            
            logger.info("Knowledge base loaded from prompts/base_context.txt")
            
        except Exception as e:
            logger.error(f"Error loading knowledge base: {str(e)}")
            raise FileNotFoundError("prompts/base_context.txt is required but not found")
    
    def _build_system_message(self, question: str) -> str:
        """Build system message from base context"""
        return self.knowledge_base.get("base_context", "")
    
    def query(self, question: str) -> str:
        """
        Process a question using RAG approach with conversation memory
        
        Args:
            question (str): User's question about business advice
            
        Returns:
            str: Agent's response with business guidance
        """
        try:
            self.response_count += 1
            logger.info(f"Processing RAG query #{self.response_count}: {question[:50]}...")
            
            # Build system message
            system_message = self._build_system_message(question)
            
            # Get conversation history from memory
            chat_history = self.memory.chat_memory.messages
            
            # Build messages for LLM
            messages = [SystemMessage(content=system_message)]
            
            # Add relevant conversation history
            if chat_history:
                # Include last 6 messages (3 exchanges) for context
                recent_history = chat_history[-6:]
                messages.extend(recent_history)
            
            # Add current question
            messages.append(HumanMessage(content=question))
            
            # Get response from LLM
            response = self.llm.invoke(messages)
            answer = response.content
            
            # Save to memory
            self.memory.save_context(
                {"input": question},
                {"output": answer}
            )
            
            logger.info(f"RAG query #{self.response_count} completed successfully")
            return answer
            
        except Exception as e:
            error_msg = f"Maaf, terjadi kesalahan saat memproses pertanyaan Anda: {str(e)}"
            logger.error(f"Error in RAG query #{self.response_count}: {str(e)}")
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
            self.response_count = 0
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
    
    def add_knowledge(self, content: str):
        """Add new knowledge to the base context"""
        try:
            self.knowledge_base["base_context"] += f"\n\n{content}"
            logger.info("Added new knowledge to base context")
        except Exception as e:
            logger.error(f"Error adding knowledge: {str(e)}")
    
    def get_knowledge_base_info(self) -> Dict[str, Any]:
        """Get information about the current knowledge base"""
        try:
            base_length = len(self.knowledge_base.get("base_context", ""))
            return {
                "base_context_length": base_length,
                "response_count": self.response_count,
                "status": "loaded_from_prompts_folder"
            }
        except Exception as e:
            logger.error(f"Error getting knowledge base info: {str(e)}")
            return {"error": str(e), "response_count": self.response_count}