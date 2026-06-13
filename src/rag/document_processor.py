"""
Document Processing Module
Handles document loading, chunking, and preprocessing for the RAG system
"""

import os
from typing import List, Dict, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    MIN_CHUNK_SIZE,
    HEALTH_TOPICS
)


class DocumentProcessor:
    """Processes health documents for the RAG system"""
    
    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
        min_chunk_size: int = MIN_CHUNK_SIZE
    ):
        """
        Initialize the document processor
        
        Args:
            chunk_size: Target size for each chunk in tokens
            chunk_overlap: Number of overlapping tokens between chunks
            min_chunk_size: Minimum chunk size to keep
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
        
        # Initialize text splitter with recursive strategy
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
            keep_separator=True
        )
    
    def load_documents(self, docs_folder: str) -> List[Dict[str, str]]:
        """
        Load all documents from the health docs folder
        
        Args:
            docs_folder: Path to the folder containing health documents
            
        Returns:
            List of dictionaries containing document content and metadata
        """
        documents = []
        
        if not os.path.exists(docs_folder):
            raise FileNotFoundError(f"Documents folder not found: {docs_folder}")
        
        for filename in os.listdir(docs_folder):
            if filename.endswith('.txt'):
                filepath = os.path.join(docs_folder, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                    
                    # Extract topic from filename (e.g., 'sleep.txt' -> 'sleep')
                    topic = filename.replace('.txt', '')
                    
                    if content.strip():  # Only add non-empty documents
                        documents.append({
                            'content': content,
                            'source': filename,
                            'topic': topic,
                            'filepath': filepath
                        })
                        print(f"✓ Loaded: {filename} ({len(content)} characters)")
                    else:
                        print(f"⚠ Skipped empty file: {filename}")
                        
                except Exception as e:
                    print(f"✗ Error loading {filename}: {str(e)}")
        
        print(f"\n📚 Total documents loaded: {len(documents)}")
        return documents
    
    def chunk_document(self, document: Dict[str, str]) -> List[Dict[str, str]]:
        """
        Split a document into chunks with metadata
        
        Args:
            document: Dictionary containing document content and metadata
            
        Returns:
            List of chunk dictionaries with content and metadata
        """
        content = document['content']
        
        # Split the document into chunks
        text_chunks = self.text_splitter.split_text(content)
        
        # Filter out chunks that are too small
        text_chunks = [
            chunk for chunk in text_chunks 
            if len(chunk.strip()) >= self.min_chunk_size
        ]
        
        # Create chunk dictionaries with metadata
        chunks = []
        for idx, chunk_text in enumerate(text_chunks):
            chunk = {
                'content': chunk_text.strip(),
                'source': document['source'],
                'topic': document['topic'],
                'chunk_index': idx,
                'total_chunks': len(text_chunks),
                'chunk_id': f"{document['topic']}_chunk_{idx}"
            }
            chunks.append(chunk)
        
        return chunks
    
    def process_all_documents(self, docs_folder: str) -> Tuple[List[Dict[str, str]], Dict[str, int]]:
        """
        Load and chunk all documents from the folder
        
        Args:
            docs_folder: Path to the folder containing health documents
            
        Returns:
            Tuple of (list of all chunks, statistics dictionary)
        """
        print("🔄 Starting document processing...\n")
        
        # Load all documents
        documents = self.load_documents(docs_folder)
        
        if not documents:
            raise ValueError("No documents found to process")
        
        # Process each document into chunks
        all_chunks = []
        stats = {
            'total_documents': len(documents),
            'total_chunks': 0,
            'chunks_per_topic': {}
        }
        
        print("\n📝 Chunking documents...\n")
        
        for doc in documents:
            chunks = self.chunk_document(doc)
            all_chunks.extend(chunks)
            
            topic = doc['topic']
            stats['chunks_per_topic'][topic] = len(chunks)
            
            print(f"  {topic}: {len(chunks)} chunks")
        
        stats['total_chunks'] = len(all_chunks)
        
        print(f"\n✅ Processing complete!")
        print(f"   Total chunks created: {stats['total_chunks']}")
        print(f"   Average chunk size: {sum(len(c['content']) for c in all_chunks) // len(all_chunks)} characters")
        
        return all_chunks, stats
    
    def get_chunk_preview(self, chunk: Dict[str, str], max_length: int = 100) -> str:
        """
        Get a preview of a chunk for display purposes
        
        Args:
            chunk: Chunk dictionary
            max_length: Maximum length of preview
            
        Returns:
            Preview string
        """
        content = chunk['content']
        if len(content) <= max_length:
            return content
        return content[:max_length] + "..."
    
    def validate_chunks(self, chunks: List[Dict[str, str]]) -> bool:
        """
        Validate that chunks are properly formatted
        
        Args:
            chunks: List of chunk dictionaries
            
        Returns:
            True if all chunks are valid, False otherwise
        """
        required_keys = ['content', 'source', 'topic', 'chunk_index', 'chunk_id']
        
        for chunk in chunks:
            # Check all required keys are present
            if not all(key in chunk for key in required_keys):
                print(f"✗ Invalid chunk: missing required keys")
                return False
            
            # Check content is not empty
            if not chunk['content'].strip():
                print(f"✗ Invalid chunk: empty content")
                return False
        
        print(f"✓ All {len(chunks)} chunks are valid")
        return True


def main():
    """Test the document processor"""
    processor = DocumentProcessor()
    
    # Process documents
    docs_folder = "data/health_docs"
    chunks, stats = processor.process_all_documents(docs_folder)
    
    # Validate chunks
    processor.validate_chunks(chunks)
    
    # Display sample chunks
    print("\n📋 Sample chunks:\n")
    for i, chunk in enumerate(chunks[:3]):
        print(f"Chunk {i+1}:")
        print(f"  Topic: {chunk['topic']}")
        print(f"  Source: {chunk['source']}")
        print(f"  ID: {chunk['chunk_id']}")
        print(f"  Preview: {processor.get_chunk_preview(chunk)}")
        print()


if __name__ == "__main__":
    main()

# Made with Bob
