"""
Enhanced Health Search Module
Integrates all RAG components for semantic search and answer generation
"""

import os
from typing import Optional, Dict, List, Tuple
from .vector_store import VectorStore
from .query_processor import QueryProcessor
from .answer_generator import AnswerGenerator
from .config import VECTOR_STORE_PATH, TOP_K_CHUNKS, SIMILARITY_THRESHOLD

# Global instances (initialized on first use)
_vector_store: Optional[VectorStore] = None
_query_processor: Optional[QueryProcessor] = None
_answer_generator: Optional[AnswerGenerator] = None


def initialize_rag_system(force_rebuild: bool = False) -> bool:
    """
    Initialize the RAG system components
    
    Args:
        force_rebuild: Force rebuild of vector store
        
    Returns:
        True if initialized successfully
    """
    global _vector_store, _query_processor, _answer_generator
    
    try:
        print("🔄 Initializing HealthWise AI RAG System...")
        
        # Initialize query processor
        _query_processor = QueryProcessor()
        print("✓ Query processor initialized")
        
        # Initialize answer generator
        _answer_generator = AnswerGenerator()
        print("✓ Answer generator initialized")
        
        # Initialize vector store
        _vector_store = VectorStore()
        
        # Try to load existing index
        if not force_rebuild and _vector_store.load_index():
            print("✓ Vector store loaded from disk")
            return True
        
        # Build new index if needed
        print("⚠ Building new vector store (this may take a minute)...")
        from .vector_store import build_vector_store
        _vector_store = build_vector_store()
        print("✓ Vector store built successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Error initializing RAG system: {str(e)}")
        return False


def get_rag_components() -> Tuple[VectorStore, QueryProcessor, AnswerGenerator]:
    """
    Get initialized RAG components, initializing if needed
    
    Returns:
        Tuple of (vector_store, query_processor, answer_generator)
    """
    global _vector_store, _query_processor, _answer_generator
    
    if _vector_store is None or _query_processor is None or _answer_generator is None:
        initialize_rag_system()
    
    return _vector_store, _query_processor, _answer_generator


def search_health_docs(query, top_k=TOP_K_CHUNKS, threshold=SIMILARITY_THRESHOLD, return_detailed=False):
    """
    Search health documents using semantic search and generate answer
    
    Args:
        query: User's health-related question
        top_k: Number of top results to retrieve
        threshold: Minimum similarity threshold
        return_detailed: Return detailed response dict instead of formatted string
        
    Returns:
        Formatted answer string or detailed response dict
    """
    try:
        # Get RAG components
        vector_store, query_processor, answer_generator = get_rag_components()
        
        # Process query
        processed_query = query_processor.process_query(query)
        search_query = processed_query['search_query']
        
        # Search vector store
        results = vector_store.search(search_query, top_k=top_k, threshold=threshold)
        
        # Generate answer
        answer_dict = answer_generator.generate_answer(query, results)
        
        # Add query processing info
        answer_dict['processed_query'] = processed_query
        
        if return_detailed:
            return answer_dict
        
        # Format and return answer
        return answer_generator.format_answer(answer_dict)
        
    except Exception as e:
        error_msg = f"Error processing query: {str(e)}"
        print(f"✗ {error_msg}")
        
        if return_detailed:
            # Return error dict for detailed mode
            return {
                'answer': f"I encountered an error while processing your question.",
                'confidence': 'none',
                'confidence_score': 0.0,
                'sources': 'Error',
                'key_points': [],
                'context': '',
                'disclaimer': '',
                'error': error_msg
            }
        
        return f"I encountered an error while processing your question. Please try again or rephrase your question.\n\nError: {error_msg}"


def search_with_context(
    query: str,
    conversation_history: Optional[List[str]] = None
) -> Dict:
    """
    Search with conversation context for multi-turn dialogue
    
    Args:
        query: Current query
        conversation_history: Previous queries in conversation
        
    Returns:
        Detailed response dictionary
    """
    # Enhance query with conversation context if available
    if conversation_history:
        # Simple context enhancement - can be improved with more sophisticated methods
        context_keywords = []
        for prev_query in conversation_history[-3:]:  # Last 3 queries
            context_keywords.extend(prev_query.lower().split())
        
        # Add context to current query if relevant
        if context_keywords:
            query = f"{query} (context: {' '.join(set(context_keywords))})"
    
    return search_health_docs(query, return_detailed=True)


def get_system_stats() -> Dict:
    """
    Get statistics about the RAG system
    
    Returns:
        Dictionary with system statistics
    """
    try:
        vector_store, _, _ = get_rag_components()
        return vector_store.get_statistics()
    except Exception as e:
        return {'error': str(e), 'status': 'not_initialized'}


def rebuild_vector_store() -> bool:
    """
    Rebuild the vector store from scratch
    
    Returns:
        True if successful
    """
    try:
        return initialize_rag_system(force_rebuild=True)
    except Exception as e:
        print(f"✗ Error rebuilding vector store: {str(e)}")
        return False


# Backward compatibility function (legacy)
def search_health_docs_legacy(query: str) -> str:
    """
    Legacy search function for backward compatibility
    Uses basic keyword matching (old implementation)
    """
    import os
    
    DOCS_FOLDER = "data/health_docs"
    query = query.lower()
    results = []
    
    for filename in os.listdir(DOCS_FOLDER):
        path = os.path.join(DOCS_FOLDER, filename)
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        if any(word in content.lower() for word in query.split()):
            results.append(content)
    
    if results:
        return "\n\n".join(results)
    return "No relevant health information found."