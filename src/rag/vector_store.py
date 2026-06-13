"""
Vector Store Module
Handles embedding generation and FAISS vector store operations
"""

import os
import pickle
import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from sentence_transformers import SentenceTransformer
import faiss

from .config import (
    EMBEDDING_MODEL,
    VECTOR_STORE_PATH,
    FAISS_INDEX_NAME,
    TOP_K_CHUNKS,
    SIMILARITY_THRESHOLD
)


class VectorStore:
    """Manages embeddings and FAISS vector store for semantic search"""
    
    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL,
        vector_store_path: str = VECTOR_STORE_PATH
    ):
        """
        Initialize the vector store
        
        Args:
            model_name: Name of the sentence-transformers model
            vector_store_path: Path to save/load vector store
        """
        self.model_name = model_name
        self.vector_store_path = vector_store_path
        self.index = None
        self.chunks = []
        self.embeddings = None
        
        print(f"🔄 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"✓ Model loaded (dimension: {self.embedding_dim})")
    
    def generate_embeddings(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Generate embeddings for a list of texts
        
        Args:
            texts: List of text strings to embed
            batch_size: Batch size for encoding
            
        Returns:
            Numpy array of embeddings
        """
        print(f"🔄 Generating embeddings for {len(texts)} texts...")
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True  # Normalize for cosine similarity
        )
        
        print(f"✓ Embeddings generated: shape {embeddings.shape}")
        return embeddings
    
    def create_index(self, chunks: List[Dict[str, str]]) -> None:
        """
        Create FAISS index from document chunks
        
        Args:
            chunks: List of chunk dictionaries with content and metadata
        """
        if not chunks:
            raise ValueError("No chunks provided to create index")
        
        print(f"\n🔄 Creating FAISS index from {len(chunks)} chunks...")
        
        # Store chunks for later retrieval
        self.chunks = chunks
        
        # Extract text content from chunks
        texts = [chunk['content'] for chunk in chunks]
        
        # Generate embeddings
        self.embeddings = self.generate_embeddings(texts)
        
        # Create FAISS index (using Inner Product for normalized vectors = cosine similarity)
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        
        # Add embeddings to index
        self.index.add(self.embeddings)
        
        print(f"✓ FAISS index created with {self.index.ntotal} vectors")
    
    def save_index(self) -> None:
        """Save the FAISS index and chunks to disk"""
        if self.index is None or not self.chunks:
            raise ValueError("No index or chunks to save. Create index first.")
        
        # Create directory if it doesn't exist
        os.makedirs(self.vector_store_path, exist_ok=True)
        
        # Save FAISS index
        index_path = os.path.join(self.vector_store_path, f"{FAISS_INDEX_NAME}.index")
        faiss.write_index(self.index, index_path)
        print(f"✓ FAISS index saved to: {index_path}")
        
        # Save chunks and embeddings
        data_path = os.path.join(self.vector_store_path, f"{FAISS_INDEX_NAME}.pkl")
        with open(data_path, 'wb') as f:
            pickle.dump({
                'chunks': self.chunks,
                'embeddings': self.embeddings,
                'model_name': self.model_name,
                'embedding_dim': self.embedding_dim
            }, f)
        print(f"✓ Chunks and metadata saved to: {data_path}")
    
    def load_index(self) -> bool:
        """
        Load the FAISS index and chunks from disk
        
        Returns:
            True if loaded successfully, False otherwise
        """
        index_path = os.path.join(self.vector_store_path, f"{FAISS_INDEX_NAME}.index")
        data_path = os.path.join(self.vector_store_path, f"{FAISS_INDEX_NAME}.pkl")
        
        if not os.path.exists(index_path) or not os.path.exists(data_path):
            print("⚠ No saved index found")
            return False
        
        try:
            print("🔄 Loading FAISS index from disk...")
            
            # Load FAISS index
            self.index = faiss.read_index(index_path)
            print(f"✓ FAISS index loaded: {self.index.ntotal} vectors")
            
            # Load chunks and embeddings
            with open(data_path, 'rb') as f:
                data = pickle.load(f)
            
            self.chunks = data['chunks']
            self.embeddings = data['embeddings']
            
            # Verify model compatibility
            if data['model_name'] != self.model_name:
                print(f"⚠ Warning: Loaded index uses different model: {data['model_name']}")
            
            print(f"✓ Loaded {len(self.chunks)} chunks")
            return True
            
        except Exception as e:
            print(f"✗ Error loading index: {str(e)}")
            return False
    
    def search(
        self,
        query: str,
        top_k: int = TOP_K_CHUNKS,
        threshold: float = SIMILARITY_THRESHOLD
    ) -> List[Tuple[Dict[str, str], float]]:
        """
        Search for similar chunks using semantic similarity
        
        Args:
            query: Search query string
            top_k: Number of top results to return
            threshold: Minimum similarity score (0-1)
            
        Returns:
            List of tuples (chunk_dict, similarity_score)
        """
        if self.index is None or not self.chunks:
            raise ValueError("Index not initialized. Create or load index first.")
        
        # Generate query embedding
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        
        # Search in FAISS index
        similarities, indices = self.index.search(query_embedding, top_k)
        
        # Filter by threshold and prepare results
        results = []
        for similarity, idx in zip(similarities[0], indices[0]):
            if similarity >= threshold:
                chunk = self.chunks[idx].copy()
                results.append((chunk, float(similarity)))
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store
        
        Returns:
            Dictionary with statistics
        """
        if self.index is None:
            return {'status': 'not_initialized'}
        
        stats = {
            'status': 'initialized',
            'total_vectors': self.index.ntotal,
            'embedding_dimension': self.embedding_dim,
            'model_name': self.model_name,
            'total_chunks': len(self.chunks),
            'topics': list(set(chunk['topic'] for chunk in self.chunks)),
            'chunks_per_topic': {}
        }
        
        # Count chunks per topic
        for chunk in self.chunks:
            topic = chunk['topic']
            stats['chunks_per_topic'][topic] = stats['chunks_per_topic'].get(topic, 0) + 1
        
        return stats
    
    def rebuild_index(self, chunks: List[Dict[str, str]]) -> None:
        """
        Rebuild the index from scratch with new chunks
        
        Args:
            chunks: List of chunk dictionaries
        """
        print("\n🔄 Rebuilding vector store...")
        self.create_index(chunks)
        self.save_index()
        print("✓ Vector store rebuilt successfully")


def build_vector_store(docs_folder: str = "data/health_docs") -> VectorStore:
    """
    Build a complete vector store from health documents
    
    Args:
        docs_folder: Path to health documents folder
        
    Returns:
        Initialized VectorStore instance
    """
    from .document_processor import DocumentProcessor
    
    print("=" * 60)
    print("Building HealthWise AI Vector Store")
    print("=" * 60)
    
    # Process documents
    processor = DocumentProcessor()
    chunks, stats = processor.process_all_documents(docs_folder)
    
    # Create vector store
    vector_store = VectorStore()
    vector_store.create_index(chunks)
    vector_store.save_index()
    
    print("\n" + "=" * 60)
    print("✅ Vector Store Build Complete!")
    print("=" * 60)
    
    # Display statistics
    vs_stats = vector_store.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"   Total vectors: {vs_stats['total_vectors']}")
    print(f"   Embedding dimension: {vs_stats['embedding_dimension']}")
    print(f"   Topics covered: {', '.join(vs_stats['topics'])}")
    print(f"\n   Chunks per topic:")
    for topic, count in vs_stats['chunks_per_topic'].items():
        print(f"     - {topic}: {count}")
    
    return vector_store


def main():
    """Test the vector store"""
    # Build vector store
    vector_store = build_vector_store()
    
    # Test search
    print("\n" + "=" * 60)
    print("Testing Search Functionality")
    print("=" * 60)
    
    test_queries = [
        "How much sleep do I need?",
        "What are the benefits of exercise?",
        "How to manage stress?",
        "Why is hydration important?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        results = vector_store.search(query, top_k=3)
        
        if results:
            print(f"   Found {len(results)} relevant chunks:")
            for i, (chunk, score) in enumerate(results, 1):
                print(f"\n   Result {i} (similarity: {score:.3f}):")
                print(f"     Topic: {chunk['topic']}")
                print(f"     Source: {chunk['source']}")
                preview = chunk['content'][:150] + "..." if len(chunk['content']) > 150 else chunk['content']
                print(f"     Preview: {preview}")
        else:
            print("   No results found above threshold")


if __name__ == "__main__":
    main()

# Made with Bob
