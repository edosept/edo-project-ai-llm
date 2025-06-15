import gradio as gr
import logging
from typing import List, Tuple
from agents.sql_agent import SQLAgent
from agents.rag_agent import RAGAgent
from agents.router import Router

logger = logging.getLogger(__name__)

class GradioApp:
    """Mas Warung - AI UMKM Assistant"""
    
    def __init__(self):
        self.sql_agent = None
        self.rag_agent = None
        self.router = None
        self.chat_history = []
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all agents"""
        try:
            logger.info("Initializing agents...")
            
            self.sql_agent = SQLAgent()
            self.rag_agent = RAGAgent()
            self.router = Router()
            
            logger.info("All agents initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing agents: {str(e)}")
            raise
    
    def process_message(self, message: str, history: List[List[str]]) -> Tuple[str, List[List[str]]]:
        """Process user message and return response"""
        try:
            if not message.strip():
                return "", history
            
            logger.info(f"Processing message: {message[:50]}...")
            
            # Classify the message
            classification = self.router.classify(message)
            logger.info(f"Message classified as: {classification}")
            
            # Route to appropriate agent
            if classification == "SQL":
                response = self.sql_agent.query(message)
            else:
                response = self.rag_agent.query(message)
            
            # Update history
            history.append([message, response])
            
            logger.info("Message processed successfully")
            return "", history
            
        except Exception as e:
            error_msg = f"Maaf, terjadi kesalahan: {str(e)}"
            logger.error(f"Error processing message: {str(e)}")
            history.append([message, error_msg])
            return "", history
    
    def clear_conversation(self) -> List[List[str]]:
        """Clear conversation history"""
        try:
            self.sql_agent.clear_memory()
            self.rag_agent.clear_memory()
            self.router.clear_cache()
            
            logger.info("Conversation cleared")
            return []
            
        except Exception as e:
            logger.error(f"Error clearing conversation: {str(e)}")
            return []
    
    def create_interface(self):
        """Create Gradio interface"""
        with gr.Blocks(title="Mas Warung - AI UMKM", theme=gr.themes.Soft()) as interface:
            
            gr.Markdown("# 🏪 Mas Warung")
            gr.Markdown("Asisten AI untuk analisis data dan saran bisnis UMKM Anda")
            
            chatbot = gr.Chatbot(
                value=[],
                height=500,
                label="Percakapan dengan Mas Warung",
                placeholder="Mulai percakapan dengan Mas Warung..."
            )
            
            with gr.Row():
                msg_input = gr.Textbox(
                    placeholder="Tanya Mas Warung tentang data bisnis atau minta saran...",
                    label="Pesan",
                    scale=4
                )
                send_btn = gr.Button("Kirim", variant="primary", scale=1)
            
            clear_btn = gr.Button("Hapus Percakapan", variant="secondary")
            
            # Event handlers
            send_btn.click(
                self.process_message,
                inputs=[msg_input, chatbot],
                outputs=[msg_input, chatbot]
            )
            
            msg_input.submit(
                self.process_message,
                inputs=[msg_input, chatbot],
                outputs=[msg_input, chatbot]
            )
            
            clear_btn.click(
                self.clear_conversation,
                outputs=[chatbot]
            )
        
        return interface
    
    def launch(self, share=True, server_port=7860):
        """Launch the Gradio interface"""
        try:
            interface = self.create_interface()
            
            logger.info(f"Launching Gradio interface on port {server_port}")
            
            interface.launch(
                share=share,
                server_port=server_port,
                server_name="0.0.0.0"
            )
            
        except Exception as e:
            logger.error(f"Error launching Gradio interface: {str(e)}")
            raise