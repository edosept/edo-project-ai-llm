import os
import pandas as pd
import io
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pinecone import Pinecone, ServerlessSpec
from langchain.schema.document import Document
from langchain.schema.retriever import BaseRetriever
from typing import List
import random


# Load environment variables from .env file
load_dotenv()

# Initialize Pinecone with the new API
pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY")
)

# Function to process Excel/CSV files
def process_spreadsheet_file(file_path):
    """Process spreadsheet file and convert it to document chunks"""
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_name)[1].lower().replace('.', '')
    documents = []
    
    try:
        # Determine file type and process accordingly
        if file_extension in ['csv', 'txt']:
            # For CSV files
            df = pd.read_csv(file_path)
            
            # Create a single document with metadata
            header = f"File: {file_name}\n"
            header += "Columns: " + ", ".join(df.columns.astype(str)) + "\n\n"
            csv_string = df.to_csv(index=False)
            full_content = header + csv_string
            
            doc = Document(
                page_content=full_content,
                metadata={
                    "source": file_name,
                    "file_type": file_extension,
                    "row_count": len(df),
                    "column_count": len(df.columns)
                }
            )
            documents.append(doc)
            
        else:
            # For Excel-like formats (xlsx, xls, xlsm, ods, etc.)
            # Choose the appropriate engine based on file type
            if file_extension == 'xls':
                engine = 'xlrd'  # For old .xls files
            elif file_extension in ['xlsx', 'xlsm', 'xlsb']:
                engine = 'openpyxl'  # For newer Excel formats
            elif file_extension == 'ods':
                engine = 'odf'  # For OpenDocument formats
            else:
                # Default to openpyxl for unknown formats
                engine = 'openpyxl'
            
            # Read all sheets from the Excel file
            dfs = pd.read_excel(file_path, sheet_name=None, engine=engine)
            
            # Process each sheet
            for sheet_name, df in dfs.items():
                # Convert dataframe to string with context
                header = f"File: {file_name} | Sheet: {sheet_name}\n"
                header += "Columns: " + ", ".join(df.columns.astype(str)) + "\n\n"
                
                # Convert to CSV string format for easy reading
                csv_string = df.to_csv(index=False)
                content = header + csv_string
                
                # Create a document with metadata
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": file_name,
                        "sheet": sheet_name,
                        "file_type": file_extension,
                        "row_count": len(df),
                        "column_count": len(df.columns)
                    }
                )
                documents.append(doc)
    
    except Exception as e:
        # Handle errors by creating a document with error information
        error_content = f"Error processing file: {file_name}\nError type: {type(e).__name__}\nError message: {str(e)}"
        error_doc = Document(
            page_content=error_content,
            metadata={
                "source": file_name,
                "file_type": file_extension,
                "error": True
            }
        )
        documents.append(error_doc)
        print(f"Error processing {file_name}: {str(e)}")
    
    return documents

# Function to load documents from local directory
def load_documents_from_directory(directory_path, file_limit=100):
    """Load spreadsheet documents from a local directory with a limit"""
    
    print(f"Looking for spreadsheet files in {directory_path}...")
    
    # Find all spreadsheet files in the directory (including subdirectories)
    all_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            # Check if file is a spreadsheet based on extension
            ext = os.path.splitext(file)[1].lower()
            if ext in ['.xlsx', '.xls', '.xlsm', '.xlsb', '.ods', '.csv', '.tsv']:
                all_files.append(os.path.join(root, file))
    
    # Limit the number of files if needed
    all_files = all_files[:file_limit]
    print(f"Found {len(all_files)} spreadsheet files")
    
    # Process each file
    all_documents = []
    for idx, file_path in enumerate(all_files):
        print(f"Processing file {idx+1}/{len(all_files)}: {os.path.basename(file_path)}")
        documents = process_spreadsheet_file(file_path)
        all_documents.extend(documents)
    
    print(f"Successfully processed {len(all_files)} spreadsheet files")
    print(f"Created {len(all_documents)} document chunks")
    
    return all_documents

# Process documents and prepare for Pinecone
def prepare_documents_for_pinecone(documents):
    """Split documents into chunks suitable for embedding"""
    
    # Create text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Adjust chunk size as needed
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", ",", " ", ""]
    )
    
    # Split documents into chunks
    print("Splitting documents into chunks...")
    doc_chunks = text_splitter.split_documents(documents)
    print(f"Created {len(doc_chunks)} document chunks")
    
    return doc_chunks

# Custom retriever
class CustomPineconeRetriever(BaseRetriever):
    pinecone_index: object
    embedding_function: object
    text_key: str = "text"
    k: int = 4
    
    class Config:
        arbitrary_types_allowed = True
    
    def _get_relevant_documents(self, query: str) -> List[Document]:
        # Create query embedding
        query_embedding = self.embedding_function.embed_query(query)
        
        # Query Pinecone
        results = self.pinecone_index.query(
            vector=query_embedding,
            top_k=self.k,
            include_metadata=True
        )
        
        # Convert results to documents
        docs = []
        for match in results["matches"]:
            metadata = match["metadata"] if match.get("metadata") else {}
            # Remove the text from metadata as it's the page content
            text = metadata.pop(self.text_key, "")
            docs.append(Document(page_content=text, metadata=metadata))
        
        return docs

# Index documents in Pinecone
def index_documents_in_pinecone(doc_chunks, index_name="drive-documents"):
    """Index document chunks in Pinecone vector database"""
    
    # Initialize embeddings model
    print("Initializing embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # embeddings = HuggingFaceEmbeddings(model_name="firqaaa/indo-sentence-bert-base")
    
    # Check if index exists, create if not
    dimension = 384  # Dimension for all-MiniLM-L6-v2
    # dimension = 768  # Dimension for firqaaa/indo-sentence-bert-base
    
    # List available indexes for debugging
    available_indexes = pc.list_indexes().names()
    print(f"Available indexes: {available_indexes}")
    
    # Update to use the new Pinecone API
    if index_name not in available_indexes:
        print(f"Creating new Pinecone index: {index_name}")
        # For free tier, use serverless spec with default settings
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric='cosine', # or euclidean similarity
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
        # Wait for index to be ready
        print("Waiting for index to be ready...")
        time.sleep(10)
    else:
        print(f"Using existing Pinecone index: {index_name}")
    
    print("Creating vector store and uploading embeddings...")
    
    # Get the Pinecone index
    index = pc.Index(index_name)
    
    # Process in much smaller batches - free tier likely has limits
    batch_size = 10
    max_retries = 3
    
    print(f"Total chunks to process: {len(doc_chunks)}")
    print(f"Processing in batches of {batch_size}")
    
    # Create a subset of documents for testing (remove this in production)
    # For troubleshooting, let's just try a small number first
    sample_size = min(100, len(doc_chunks))  # Start with just 100 documents for testing
    doc_chunks_sample = random.sample(doc_chunks, sample_size)
    print(f"Testing with a sample of {sample_size} documents")
    
    successful_uploads = 0
    
    for i in range(0, len(doc_chunks_sample), batch_size):
        batch = doc_chunks_sample[i:i+batch_size]
        
        # Convert documents to format expected by Pinecone
        texts = [doc.page_content for doc in batch]
        metadatas = [doc.metadata for doc in batch]
        
        # Create embeddings
        embeddings_batch = embeddings.embed_documents(texts)
        
        # Create unique IDs for each vector
        ids = [f"doc_{i+j}" for j in range(len(batch))]
        
        # Prepare vectors in Pinecone format
        vectors = []
        for j, (embedding, text, metadata) in enumerate(zip(embeddings_batch, texts, metadatas)):
            vectors.append({
                "id": ids[j],
                "values": embedding,
                "metadata": {
                    "text": text,
                    **metadata
                }
            })
        
        # Attempt to upsert with retries
        for attempt in range(max_retries):
            try:
                # Upsert to Pinecone
                index.upsert(vectors=vectors)
                successful_uploads += len(batch)
                print(f"Batch {i//batch_size + 1}: Successfully uploaded {len(batch)} vectors. Total: {successful_uploads}/{sample_size}")
                
                # Add a small delay between batches to avoid rate limiting
                time.sleep(1)
                break
            except Exception as e:
                print(f"Error in batch {i//batch_size + 1}, attempt {attempt+1}/{max_retries}: {str(e)}")
                if attempt == max_retries - 1:
                    print("Max retries reached. Continuing with next batch...")
                else:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
    
    print(f"Completed upload attempts. Successfully uploaded approximately {successful_uploads} document chunks to Pinecone")
    
    # Create our custom retriever
    retriever = CustomPineconeRetriever(
        pinecone_index=index,
        embedding_function=embeddings,
        text_key="text",
        k=5
    )
    
    # Return the retriever directly
    return retriever

# Set up the QA chain
def setup_qa_chain(retriever):
    """Set up the question-answering chain"""
    
    print("Setting up QA chain with AI model...")
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",  # Adjust based on available models in aimlapi.com
        openai_api_key=os.environ.get("AIMLAPI_API_KEY"),
        openai_api_base="https://api.aimlapi.com/v1",
        temperature=0.7,
        max_tokens=2048
    )

    # Create a custom prompt template with system message
    system_prompt = """
    You are an AI sales assistant for the company. Your role is to provide accurate, helpful information about sales data, trends, and performance metrics based on the Excel spreadsheets in the company's database.
    
    When answering questions:
    - Always be professional and concise
    - Reference specific data from the provided context
    - Compare metrics when relevant (e.g., today vs. yesterday, this week vs. last week)
    - Highlight significant changes or patterns
    - Provide actionable insights when possible
    - Mention the source file and sheet when referring to specific data
    
    Use only the information provided in the context to answer questions. If you don't have enough information, say so clearly.
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

# Main function
def main():
    # Path to your local directory containing Excel files
    data_directory = "./data"  # Change this to your directory path
    
    # Load documents from the local directory
    documents = load_documents_from_directory(data_directory, file_limit=100)
    
    # Prepare documents for indexing
    doc_chunks = prepare_documents_for_pinecone(documents)
    
    # Index documents in Pinecone
    retriever = index_documents_in_pinecone(doc_chunks)
    
    # Set up QA chain
    qa_chain = setup_qa_chain(retriever)
    
    # Example query function
    def query_documents(question):
        return qa_chain.run(question)
    
    # Example usage (in a real application, you'd call this from an API endpoint)
    print("\n--- Example Query ---")
    question = "How were yesterday's sales results? Was there an increase from the previous day?"
    print(f"Question: {question}")
    response = query_documents(question)
    print(f"Answer: {response}")

if __name__ == "__main__":
    main()