import streamlit as st
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

# Page configuration
st.set_page_config(
    page_title="Asisten Bisnis UMKM Indonesia",
    page_icon="📈",
    layout="centered"  # Centered for chat-like experience
)

# Customize header with general business growth context
st.title("📈 Asisten Bisnis UMKM Indonesia")
st.markdown("Solusi cerdas untuk membantu UMKM Anda berkembang dengan insight berbasis data")

with st.expander("Contoh pertanyaan yang bisa Anda ajukan:"):
    st.markdown("""
    - Produk apa yang paling laris di bulan ini?
    - Bagaimana tren penjualan selama 3 bulan terakhir?
    - Usaha mana yang memberikan keuntungan paling besar?
    - Berapa rata-rata pengeluaran harian untuk setiap usaha?
    - Strategi apa yang bisa digunakan untuk meningkatkan profitabilitas?
    """)

# Set up the QA chain
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

# Initialize the system with caching
@st.cache_resource
def initialize_system():
    """Initialize the RAG system by connecting to existing Pinecone index"""
    with st.spinner("Menghubungkan ke basis data bisnis UMKM..."):
        qa_chain = setup_qa_chain()
    return qa_chain

# Initialize system
qa_chain = initialize_system()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": """
         Halo! Saya adalah asisten bisnis UMKM Anda👋\n
         ✨ **Apa yang ingin Anda ketahui tentang bisnis Anda hari ini?**
         """}
    ]

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Tanyakan tentang bisnis Anda..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Sedang menganalisis data bisnis Anda..."):
            try:
                full_response = qa_chain.invoke({"query": prompt})
                answer = full_response["result"]
                
                # Display the answer
                message_placeholder.markdown(answer)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"Maaf, saya mengalami kendala teknis: {str(e)}. Silakan coba lagi dalam beberapa saat."
                message_placeholder.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Add footer
st.markdown("---")
st.markdown("""
💡 **Tips:** 
- Untuk hasil terbaik, berikan pertanyaan yang spesifik
- Data-driven insights membantu Anda membuat keputusan bisnis yang lebih baik
- Analisis data dapat membantu Anda mengidentifikasi peluang pertumbuhan bisnis
""")