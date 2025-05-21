import streamlit as st
import time
import os
from dotenv import load_dotenv
import sys

# Import functions from main.py
from main import (
    load_documents_from_directory,
    prepare_documents_for_pinecone,
    index_documents_in_pinecone,
    setup_qa_chain
)

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
    - Produk apa yang paling laris bulan ini?
    - Bagaimana tren penjualan selama 3 bulan terakhir?
    - Usaha mana yang memberikan keuntungan paling besar?
    - Berapa rata-rata pengeluaran harian untuk setiap usaha?
    - Produk apa yang memiliki margin keuntungan tertinggi?
    - Kapan jam operasional dengan penjualan tertinggi?
    - Strategi apa yang bisa meningkatkan profitabilitas?
    """)

# Initialize the system with caching
@st.cache_resource
def initialize_system():
    """Initialize the RAG system with caching"""
    data_directory = "./umkm_data"
    
    with st.spinner("Memuat data bisnis UMKM..."):
        documents = load_documents_from_directory(data_directory, file_limit=100)
        doc_chunks = prepare_documents_for_pinecone(documents)
        retriever = index_documents_in_pinecone(doc_chunks, index_name="umkm-documents")
        qa_chain = setup_qa_chain(retriever)
        
    return qa_chain

# Initialize system
qa_chain = initialize_system()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Saya adalah asisten bisnis UMKM Anda. Saya dapat membantu menganalisis data dan memberikan rekomendasi strategis untuk meningkatkan profitabilitas, mengelola sumber daya dengan efisien, dan mengembangkan bisnis Anda secara berkelanjutan. Apa yang ingin Anda ketahui tentang bisnis Anda hari ini?"}
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