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
    page_title="Sales Assistant",
    page_icon="💬",
    layout="centered"  # Changed to centered for chat-like experience
)

# Simple header
st.title("💬 Sales Data Assistant")

with st.expander("Show example questions"):
    st.markdown("""
    - What were our top selling products last month?
    - What were the sales trends over the past quarter?
    - What products have the highest profit margin?
    """)

# Initialize the system with caching
@st.cache_resource
def initialize_system():
    """Initialize the RAG system with caching"""
    data_directory = "./data"
    
    with st.spinner("Loading sales data..."):
        documents = load_documents_from_directory(data_directory, file_limit=100)
        doc_chunks = prepare_documents_for_pinecone(documents)
        retriever = index_documents_in_pinecone(doc_chunks)
        qa_chain = setup_qa_chain(retriever)
        
    return qa_chain

# Initialize system
qa_chain = initialize_system()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your sales data assistant. Ask me anything about your sales data."}
    ]

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask about your sales data..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            try:
                full_response = qa_chain.invoke({"query": prompt})
                answer = full_response["result"]
                
                # Display the answer
                message_placeholder.markdown(answer)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

