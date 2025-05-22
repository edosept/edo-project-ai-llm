import gradio as gr
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Import the custom retriever from utils
from utils import CustomPineconeRetriever

# Load environment variables
load_dotenv()

# Global variable to store the QA chain
qa_chain = None

def setup_qa_chain():
    """Set up the question-answering chain by connecting to existing Pinecone index"""
    
    # Initialize Pinecone
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    index_name = "umkm-documents"
    
    # Initialize embeddings model
    embeddings = HuggingFaceEmbeddings(model_name="firqaaa/indo-sentence-bert-base")
    
    # Get the Pinecone index
    index = pc.Index(index_name)
    
    # Create custom retriever
    retriever = CustomPineconeRetriever(
        pinecone_index=index,
        embedding_function=embeddings,
        text_key="text",
        k=5
    )
    
    # Initialize LLM
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        openai_api_key=os.environ.get("AIMLAPI_API_KEY"),
        openai_api_base="https://api.aimlapi.com/v1",
        temperature=0.7,
        max_tokens=2048
    )

    # Create a custom prompt template with system message
    system_prompt = """
    You are a knowledgeable UMKM Financial Advisor specializing in helping small business owners in Indonesia manage their finances and grow their businesses. Your knowledge has been enhanced with data from the owner's financial records, allowing you to provide personalized insights and recommendations.

    IMPORTANT LANGUAGE INSTRUCTION: Detect the language of the user's question and ALWAYS respond in the SAME LANGUAGE. If the user asks in Bahasa Indonesia, respond in Bahasa Indonesia. If the user asks in English, respond in English.

    Your capabilities include:
    1. Analyzing sales data to identify top-selling products, peak business hours, and revenue trends
    2. Tracking expense patterns and suggesting cost optimization opportunities
    3. Calculating profit margins by product and business unit
    4. Monitoring cash flow and providing liquidity forecasts
    5. Comparing performance across different business units
    6. Identifying effective promotions and discount strategies
    7. Suggesting inventory management improvements

    When responding in Bahasa Indonesia:
    - Use informal but respectful language (gunakan "Anda" bukan "kamu" atau "Bapak/Ibu")
    - Use simple, clear language avoiding complex financial jargon
    - Format currency as Rupiah (Rp) with dots for thousands (e.g., Rp 1.500.000)
    - Use Indonesian business terminology and expressions

    When responding in English:
    - Maintain a friendly, professional tone
    - Use simple, clear language avoiding complex financial jargon
    - Format currency as Rupiah (Rp) with dots for thousands (e.g., Rp 1,500,000)
    - Explain any Indonesian terms that might not be familiar to English speakers

    In all cases:
    - Provide specific, data-backed insights rather than general advice
    - Include relevant numbers and calculations to support your recommendations
    - When appropriate, explain your reasoning briefly so the owner understands your logic
    - Always frame advice in a practical, actionable way that considers resource constraints

    The business owner manages multiple warung operations:
    1. Warung Kopi Gembira - A coffee shop selling beverages and simple meals
    2. Warung Sayur Buah Sehat - A fresh produce shop selling vegetables and fruits
    3. Warung Sembako Berkah - A grocery store selling daily essentials

    Your goal is to help the owner make data-driven decisions to increase profitability, manage resources efficiently, and grow their businesses sustainably.
    """

    prompt_template = """
    {system_prompt}

    Context information is below:
    {context}

    Question: {question}
    Answer:
    """

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"],
        partial_variables={"system_prompt": system_prompt}
    )

    # Create a question-answering chain with the custom prompt
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    return qa_chain

def initialize_system():
    """Initialize the system once"""
    global qa_chain
    if qa_chain is None:
        print("Initializing UMKM Business Assistant...")
        qa_chain = setup_qa_chain()
        print("System ready!")
    return qa_chain

def chat_with_assistant(message, history):
    """Handle chat interactions"""
    try:
        # Initialize system if not already done
        qa_system = initialize_system()
        
        # Get response from QA chain
        full_response = qa_system.invoke({"query": message})
        answer = full_response["result"]
        
        # Add the new exchange to history
        history.append([message, answer])
        return history, ""
        
    except Exception as e:
        error_msg = f"Maaf, saya mengalami kendala teknis: {str(e)}. Silakan coba lagi dalam beberapa saat."
        history.append([message, error_msg])
        return history, ""

# Create the Gradio interface
def create_interface():
    # Custom CSS for styling
    css = """
    .gradio-container {
        font-family: 'Arial', sans-serif;
    }
    .chat-message {
        padding: 10px;
        margin: 5px 0;
        border-radius: 10px;
    }
    """
    
    # Welcome message
    welcome_msg = """
    Halo! Saya adalah asisten bisnis UMKM Anda 👋

    ✨ Apa yang ingin Anda ketahui tentang bisnis Anda hari ini?
    """
    
    # Create the chat interface
    with gr.Blocks(
        title="📈 Asisten Bisnis UMKM Indonesia",
        theme=gr.themes.Soft(),
        css=css
    ) as demo:
        
        # Header
        gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h1>📈 Asisten Bisnis UMKM Indonesia</h1>
            <p style="font-size: 18px; color: #666;">
                Solusi cerdas untuk membantu UMKM Anda berkembang dengan insight berbasis data
            </p>
        </div>
        """)
        
        # Example questions accordion
        with gr.Accordion("💡 Contoh pertanyaan yang bisa Anda ajukan:", open=False):
            gr.Markdown("""
            - Produk apa yang paling laris di bulan ini?
            - Bagaimana tren penjualan selama 3 bulan terakhir?
            - Usaha mana yang memberikan keuntungan paling besar?
            - Berapa rata-rata pengeluaran harian untuk setiap usaha?
            - Strategi apa yang bisa digunakan untuk meningkatkan profitabilitas?
            """)
        
        # Chat interface
        chatbot = gr.Chatbot(
            value=[[None, welcome_msg]],
            height=400,
            bubble_full_width=False,
            show_label=False
        )
        
        # Input box
        msg = gr.Textbox(
            placeholder="Tanyakan tentang bisnis Anda...",
            show_label=False,
            container=False
        )
        
        # Clear button
        clear = gr.Button("🗑️ Hapus Percakapan", variant="secondary", size="sm")

        # Footer
        gr.HTML("""
        <div style="padding: 20px; border-top: 1px solid #eee; margin-top: 20px;">
            <h4 style="text-align: left;">💡 Tips:</h4>
            <p style="text-align: left;">• Untuk hasil terbaik, berikan pertanyaan yang spesifik</p>
            <p style="text-align: left;">• Data-driven insights membantu Anda membuat keputusan bisnis yang lebih baik</p>
            <p style="text-align: left;">• Analisis data dapat membantu Anda mengidentifikasi peluang pertumbuhan bisnis</p>
        </div>
        """)
        
        # Event handlers
        msg.submit(chat_with_assistant, [msg, chatbot], [chatbot, msg], queue=False)
        
        clear.click(lambda: [[None, welcome_msg]], None, chatbot, queue=False)
    
    return demo

# Launch the application
if __name__ == "__main__":
    # Initialize the system
    print("Starting UMKM Business Assistant...")
    
    # Create and launch the interface
    demo = create_interface()
    
    # Launch with custom settings
    demo.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,       # Default Gradio port
        share=True,            # Set to True if you want a public link
        debug=True,             # Enable debug mode
        show_error=True         # Show errors in the interface
    )