"""
Simple Search Engine - Python 3.13 Compatible
No external AI dependencies required
"""

import os
import re
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class SimpleHealthSearch:
    """Simple TF-IDF based search engine"""
    
    def __init__(self, docs_folder="data/health_docs"):
        self.docs_folder = docs_folder
        self.documents = []
        self.doc_names = []
        self.vectorizer = None
        self.doc_vectors = None
        self.load_documents()
        
    def load_documents(self):
        """Load all health documents"""
        for filename in os.listdir(self.docs_folder):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.docs_folder, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():
                        self.documents.append(content)
                        self.doc_names.append(filename.replace('.txt', ''))
        
        if self.documents:
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            self.doc_vectors = self.vectorizer.fit_transform(self.documents)
    
    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, str, float]]:
        """
        Search documents using TF-IDF similarity
        
        Returns:
            List of (doc_name, content, score) tuples
        """
        if not self.documents:
            return []
        
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.doc_vectors)[0]
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum threshold
                results.append((
                    self.doc_names[idx],
                    self.documents[idx],
                    float(similarities[idx])
                ))
        
        return results
    
    def extract_relevant_section(self, content: str, query: str, max_length: int = 500) -> str:
        """Extract most relevant section from document"""
        sentences = content.split('.')
        query_words = set(query.lower().split())
        
        best_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue
            
            sentence_words = set(sentence.lower().split())
            overlap = len(query_words & sentence_words)
            
            if overlap > 0:
                best_sentences.append((sentence, overlap))
        
        best_sentences.sort(key=lambda x: x[1], reverse=True)
        
        result = '. '.join([s[0] for s in best_sentences[:3]])
        if len(result) > max_length:
            result = result[:max_length] + "..."
        
        return result if result else content[:max_length] + "..."


def search_health_docs(query: str) -> str:
    """
    Main search function - compatible with existing code
    """
    try:
        searcher = SimpleHealthSearch()
        results = searcher.search(query, top_k=2)
        
        if not results:
            return "I couldn't find specific information about that. Please try rephrasing your question or ask about sleep, hydration, nutrition, exercise, or stress management."
        
        response_parts = []
        response_parts.append(f"**Answer to: {query}**\n")
        
        for doc_name, content, score in results:
            relevant_section = searcher.extract_relevant_section(content, query)
            response_parts.append(f"\n**From {doc_name.title()} Guide:**")
            response_parts.append(relevant_section)
            response_parts.append(f"\n*Relevance: {score:.0%}*\n")
        
        response_parts.append("\n⚠️ **Disclaimer**: This information is for educational purposes only. Consult healthcare professionals for personalized medical advice.")
        
        return '\n'.join(response_parts)
        
    except Exception as e:
        return f"Search temporarily unavailable. Please try again. Error: {str(e)}"


# For backward compatibility
def initialize_rag_system():
    """Dummy function for compatibility"""
    return True


def get_system_stats():
    """Return system stats"""
    try:
        searcher = SimpleHealthSearch()
        return {
            'status': 'active',
            'documents': len(searcher.documents),
            'topics': searcher.doc_names,
            'method': 'TF-IDF Search'
        }
    except:
        return {'status': 'initializing'}

# Made with Bob
