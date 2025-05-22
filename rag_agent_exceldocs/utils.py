from langchain.schema.document import Document
from langchain.schema.retriever import BaseRetriever
from typing import List

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