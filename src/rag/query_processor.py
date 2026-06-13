"""
Query Processing Module
Handles query preprocessing, expansion, and optimization
"""

import re
from typing import List, Set
from .config import HEALTH_SYNONYMS, EXPAND_QUERIES


class QueryProcessor:
    """Processes and enhances user queries for better retrieval"""
    
    def __init__(self, expand_queries: bool = EXPAND_QUERIES):
        """
        Initialize the query processor
        
        Args:
            expand_queries: Whether to expand queries with synonyms
        """
        self.expand_queries = expand_queries
        self.synonyms = HEALTH_SYNONYMS
    
    def clean_query(self, query: str) -> str:
        """
        Clean and normalize the query
        
        Args:
            query: Raw query string
            
        Returns:
            Cleaned query string
        """
        # Convert to lowercase
        query = query.lower().strip()
        
        # Remove extra whitespace
        query = re.sub(r'\s+', ' ', query)
        
        # Remove special characters but keep basic punctuation
        query = re.sub(r'[^\w\s\?\.\,\-]', '', query)
        
        return query
    
    def extract_keywords(self, query: str) -> List[str]:
        """
        Extract important keywords from query
        
        Args:
            query: Query string
            
        Returns:
            List of keywords
        """
        # Simple keyword extraction (can be enhanced with NLP)
        words = query.lower().split()
        
        # Common stopwords to filter (keeping health-relevant ones)
        stopwords = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'can', 'of', 'at', 'by',
            'for', 'with', 'about', 'as', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
            'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',
            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'all',
            'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
            'only', 'own', 'same', 'so', 'than', 'too', 'very'
        }
        
        keywords = [word for word in words if word not in stopwords and len(word) > 2]
        return keywords
    
    def expand_with_synonyms(self, query: str) -> str:
        """
        Expand query with synonyms for better matching
        
        Args:
            query: Original query
            
        Returns:
            Expanded query with synonyms
        """
        if not self.expand_queries:
            return query
        
        words = query.lower().split()
        expanded_terms = set(words)
        
        # Add synonyms for recognized health terms
        for word in words:
            if word in self.synonyms:
                expanded_terms.update(self.synonyms[word])
        
        # Return original query with added synonym context
        if len(expanded_terms) > len(words):
            synonym_additions = ' '.join(expanded_terms - set(words))
            return f"{query} {synonym_additions}"
        
        return query
    
    def identify_intent(self, query: str) -> str:
        """
        Identify the intent of the query
        
        Args:
            query: Query string
            
        Returns:
            Intent category
        """
        query_lower = query.lower()
        
        # Question patterns
        if any(word in query_lower for word in ['how', 'what', 'why', 'when', 'where']):
            return 'informational'
        
        # Action patterns
        if any(word in query_lower for word in ['should', 'can i', 'help me', 'recommend', 'suggest']):
            return 'actionable'
        
        # Problem patterns
        if any(word in query_lower for word in ['problem', 'issue', 'trouble', 'difficulty', 'pain']):
            return 'problem_solving'
        
        # Benefit patterns
        if any(word in query_lower for word in ['benefit', 'advantage', 'good for', 'help with']):
            return 'benefits'
        
        return 'general'
    
    def detect_health_topic(self, query: str) -> List[str]:
        """
        Detect which health topics are mentioned in the query
        
        Args:
            query: Query string
            
        Returns:
            List of detected topics
        """
        query_lower = query.lower()
        detected_topics = []
        
        # Topic keywords mapping
        topic_keywords = {
            'sleep': ['sleep', 'sleeping', 'rest', 'insomnia', 'nap', 'bedtime', 'tired', 'fatigue'],
            'hydration': ['water', 'hydration', 'drink', 'fluid', 'dehydration', 'thirst'],
            'nutrition': ['food', 'eat', 'diet', 'nutrition', 'meal', 'vitamin', 'protein', 'carb'],
            'exercise': ['exercise', 'workout', 'fitness', 'physical activity', 'training', 'gym', 'run', 'walk'],
            'stress': ['stress', 'anxiety', 'worry', 'tension', 'pressure', 'relax', 'calm', 'mindfulness']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_topics.append(topic)
        
        return detected_topics if detected_topics else ['general']
    
    def process_query(self, query: str) -> dict:
        """
        Complete query processing pipeline
        
        Args:
            query: Raw query string
            
        Returns:
            Dictionary with processed query information
        """
        # Clean the query
        cleaned = self.clean_query(query)
        
        # Extract keywords
        keywords = self.extract_keywords(cleaned)
        
        # Expand with synonyms
        expanded = self.expand_with_synonyms(cleaned)
        
        # Identify intent
        intent = self.identify_intent(cleaned)
        
        # Detect topics
        topics = self.detect_health_topic(cleaned)
        
        return {
            'original': query,
            'cleaned': cleaned,
            'expanded': expanded,
            'keywords': keywords,
            'intent': intent,
            'topics': topics,
            'search_query': expanded  # Use expanded query for search
        }
    
    def format_query_for_display(self, processed_query: dict) -> str:
        """
        Format processed query information for display
        
        Args:
            processed_query: Processed query dictionary
            
        Returns:
            Formatted string
        """
        lines = [
            f"Original Query: {processed_query['original']}",
            f"Intent: {processed_query['intent']}",
            f"Topics: {', '.join(processed_query['topics'])}",
            f"Keywords: {', '.join(processed_query['keywords'])}"
        ]
        return '\n'.join(lines)


def main():
    """Test the query processor"""
    processor = QueryProcessor()
    
    test_queries = [
        "How much sleep do I need?",
        "What are the benefits of exercise?",
        "I'm feeling stressed, what should I do?",
        "Why is drinking water important?",
        "Can you help me with my diet?",
        "Best foods for energy"
    ]
    
    print("=" * 60)
    print("Query Processing Tests")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n{'='*60}")
        processed = processor.process_query(query)
        print(processor.format_query_for_display(processed))
        if processed['expanded'] != processed['cleaned']:
            print(f"Expanded: {processed['expanded']}")


if __name__ == "__main__":
    main()

# Made with Bob
