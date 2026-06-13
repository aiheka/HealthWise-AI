"""
Answer Generation Module
Generates contextual answers from retrieved chunks
"""

from typing import List, Tuple, Dict, Any
from .config import ANSWER_TEMPLATE, HEALTH_DISCLAIMER, HIGH_CONFIDENCE, MEDIUM_CONFIDENCE


class AnswerGenerator:
    """Generates answers from retrieved document chunks"""
    
    def __init__(self):
        """Initialize the answer generator"""
        self.template = ANSWER_TEMPLATE
        self.disclaimer = HEALTH_DISCLAIMER
    
    def extract_key_points(self, chunks: List[Dict[str, str]], max_points: int = 5) -> List[str]:
        """
        Extract key points from retrieved chunks
        
        Args:
            chunks: List of chunk dictionaries
            max_points: Maximum number of key points to extract
            
        Returns:
            List of key point strings
        """
        key_points = []
        
        for chunk in chunks[:max_points]:
            content = chunk['content']
            
            # Extract sentences that look like key points
            # Look for sentences with numbers, benefits, or recommendations
            sentences = content.split('.')
            
            for sentence in sentences:
                sentence = sentence.strip()
                
                # Skip if too short or too long
                if len(sentence) < 20 or len(sentence) > 200:
                    continue
                
                # Prioritize sentences with key indicators
                if any(indicator in sentence.lower() for indicator in [
                    'benefit', 'important', 'essential', 'recommend', 'should',
                    'help', 'improve', 'reduce', 'increase', 'support'
                ]):
                    if sentence not in key_points:
                        key_points.append(sentence)
                        if len(key_points) >= max_points:
                            return key_points
        
        # If we don't have enough key points, add first sentences from chunks
        if len(key_points) < max_points:
            for chunk in chunks:
                sentences = chunk['content'].split('.')[:2]
                for sentence in sentences:
                    sentence = sentence.strip()
                    if len(sentence) >= 20 and sentence not in key_points:
                        key_points.append(sentence)
                        if len(key_points) >= max_points:
                            break
        
        return key_points[:max_points]
    
    def build_context(self, results: List[Tuple[Dict[str, str], float]]) -> str:
        """
        Build context from retrieved chunks
        
        Args:
            results: List of (chunk, similarity_score) tuples
            
        Returns:
            Combined context string
        """
        if not results:
            return ""
        
        context_parts = []
        seen_content = set()
        
        for chunk, score in results:
            content = chunk['content'].strip()
            
            # Avoid duplicate content
            if content not in seen_content:
                context_parts.append(content)
                seen_content.add(content)
        
        return "\n\n".join(context_parts)
    
    def get_sources(self, results: List[Tuple[Dict[str, str], float]]) -> str:
        """
        Get source information from results
        
        Args:
            results: List of (chunk, similarity_score) tuples
            
        Returns:
            Formatted source string
        """
        sources = set()
        for chunk, _ in results:
            topic = chunk['topic'].capitalize()
            sources.add(topic)
        
        return ", ".join(sorted(sources))
    
    def calculate_confidence(self, results: List[Tuple[Dict[str, str], float]]) -> Tuple[str, float]:
        """
        Calculate confidence level based on similarity scores
        
        Args:
            results: List of (chunk, similarity_score) tuples
            
        Returns:
            Tuple of (confidence_level, average_score)
        """
        if not results:
            return "low", 0.0
        
        avg_score = sum(score for _, score in results) / len(results)
        
        if avg_score >= HIGH_CONFIDENCE:
            return "high", avg_score
        elif avg_score >= MEDIUM_CONFIDENCE:
            return "medium", avg_score
        else:
            return "low", avg_score
    
    def generate_direct_answer(
        self,
        query: str,
        results: List[Tuple[Dict[str, str], float]]
    ) -> str:
        """
        Generate a direct answer to the query
        
        Args:
            query: User's query
            results: Retrieved chunks with scores
            
        Returns:
            Direct answer string
        """
        if not results:
            return "I don't have enough information to answer that question."
        
        # Get the most relevant chunk
        top_chunk = results[0][0]
        content = top_chunk['content']
        
        # Extract the most relevant part based on query
        query_lower = query.lower()
        sentences = content.split('.')
        
        # Find sentences that best match the query
        relevant_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue
            
            # Check if sentence is relevant to query
            query_words = set(query_lower.split())
            sentence_words = set(sentence.lower().split())
            overlap = len(query_words & sentence_words)
            
            if overlap >= 2:  # At least 2 words in common
                relevant_sentences.append(sentence)
        
        if relevant_sentences:
            # Return first 2-3 most relevant sentences
            answer = '. '.join(relevant_sentences[:3])
            if not answer.endswith('.'):
                answer += '.'
            return answer
        
        # Fallback: return first paragraph
        paragraphs = content.split('\n\n')
        return paragraphs[0] if paragraphs else content[:300] + "..."
    
    def generate_answer(
        self,
        query: str,
        results: List[Tuple[Dict[str, str], float]],
        include_disclaimer: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a complete answer with all components
        
        Args:
            query: User's query
            results: Retrieved chunks with scores
            include_disclaimer: Whether to include health disclaimer
            
        Returns:
            Dictionary with answer components
        """
        if not results:
            return {
                'answer': "I couldn't find relevant information to answer your question. Please try rephrasing or ask about sleep, hydration, nutrition, exercise, or stress management.",
                'confidence': 'none',
                'confidence_score': 0.0,
                'sources': [],
                'key_points': [],
                'context': '',
                'disclaimer': self.disclaimer if include_disclaimer else ''
            }
        
        # Build context
        context = self.build_context(results)
        
        # Generate direct answer
        answer = self.generate_direct_answer(query, results)
        
        # Extract key points
        chunks = [chunk for chunk, _ in results]
        key_points = self.extract_key_points(chunks)
        
        # Get sources
        sources = self.get_sources(results)
        
        # Calculate confidence
        confidence_level, confidence_score = self.calculate_confidence(results)
        
        return {
            'answer': answer,
            'confidence': confidence_level,
            'confidence_score': confidence_score,
            'sources': sources,
            'key_points': key_points,
            'context': context,
            'disclaimer': self.disclaimer if include_disclaimer else '',
            'num_sources': len(results)
        }
    
    def format_answer(self, answer_dict: Dict[str, Any]) -> str:
        """
        Format the answer for display
        
        Args:
            answer_dict: Answer dictionary from generate_answer
            
        Returns:
            Formatted answer string
        """
        lines = []
        
        # Main answer
        lines.append("**Answer:**")
        lines.append(answer_dict['answer'])
        lines.append("")
        
        # Key points
        if answer_dict['key_points']:
            lines.append("**💡 Key Points:**")
            for i, point in enumerate(answer_dict['key_points'], 1):
                lines.append(f"{i}. {point}")
            lines.append("")
        
        # Sources and confidence
        lines.append(f"**📚 Sources:** {answer_dict['sources']}")
        lines.append(f"**🎯 Confidence:** {answer_dict['confidence'].capitalize()} ({answer_dict['confidence_score']:.2f})")
        lines.append("")
        
        # Disclaimer
        if answer_dict['disclaimer']:
            lines.append(answer_dict['disclaimer'])
        
        return '\n'.join(lines)
    
    def generate_fallback_response(self, query: str, detected_topics: List[str]) -> str:
        """
        Generate a fallback response when no good results are found
        
        Args:
            query: User's query
            detected_topics: Detected health topics
            
        Returns:
            Fallback response string
        """
        response = "I don't have specific information to answer that question directly. "
        
        if detected_topics and detected_topics[0] != 'general':
            topics_str = ', '.join(detected_topics)
            response += f"However, I can help you with questions about {topics_str}. "
        
        response += "\n\nTry asking about:\n"
        response += "• Sleep recommendations and sleep hygiene\n"
        response += "• Hydration benefits and water intake\n"
        response += "• Nutrition guidelines and healthy eating\n"
        response += "• Exercise types and fitness recommendations\n"
        response += "• Stress management techniques\n"
        
        return response


def main():
    """Test the answer generator"""
    generator = AnswerGenerator()
    
    # Mock results for testing
    mock_results = [
        ({
            'content': 'Sleep is essential for health. Adults need 7-9 hours per night. Quality sleep improves memory, mood, and immune function.',
            'topic': 'sleep',
            'source': 'sleep.txt'
        }, 0.85),
        ({
            'content': 'Good sleep hygiene includes maintaining a consistent schedule, creating a relaxing bedtime routine, and keeping your bedroom cool and dark.',
            'topic': 'sleep',
            'source': 'sleep.txt'
        }, 0.78)
    ]
    
    query = "How much sleep do I need?"
    
    print("=" * 60)
    print("Answer Generation Test")
    print("=" * 60)
    print(f"\nQuery: {query}\n")
    
    answer_dict = generator.generate_answer(query, mock_results)
    formatted = generator.format_answer(answer_dict)
    
    print(formatted)


if __name__ == "__main__":
    main()

# Made with Bob
