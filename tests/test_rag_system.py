"""
RAG System Test Suite
Tests for document processing, vector store, search, and answer generation
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.rag.document_processor import DocumentProcessor
from src.rag.query_processor import QueryProcessor
from src.rag.answer_generator import AnswerGenerator


def test_document_processor():
    """Test document processing and chunking"""
    print("\n" + "="*60)
    print("TEST 1: Document Processing")
    print("="*60)
    
    processor = DocumentProcessor(chunk_size=512, chunk_overlap=50)
    
    try:
        # Load and process documents
        chunks, stats = processor.process_all_documents("data/health_docs")
        
        # Validate
        assert len(chunks) > 0, "No chunks created"
        assert processor.validate_chunks(chunks), "Chunk validation failed"
        
        print(f"\n✅ Document Processing Test PASSED")
        print(f"   - Loaded {stats['total_documents']} documents")
        print(f"   - Created {stats['total_chunks']} chunks")
        print(f"   - Topics: {list(stats['chunks_per_topic'].keys())}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Document Processing Test FAILED: {str(e)}")
        return False


def test_query_processor():
    """Test query processing and enhancement"""
    print("\n" + "="*60)
    print("TEST 2: Query Processing")
    print("="*60)
    
    processor = QueryProcessor()
    
    test_queries = [
        "How much sleep do I need?",
        "What are the benefits of exercise?",
        "I'm stressed, what should I do?",
        "Why is water important?"
    ]
    
    try:
        for query in test_queries:
            processed = processor.process_query(query)
            
            # Validate
            assert 'cleaned' in processed, "Missing cleaned query"
            assert 'keywords' in processed, "Missing keywords"
            assert 'intent' in processed, "Missing intent"
            assert 'topics' in processed, "Missing topics"
            
            print(f"\n✓ Query: '{query}'")
            print(f"  Intent: {processed['intent']}")
            print(f"  Topics: {', '.join(processed['topics'])}")
            print(f"  Keywords: {', '.join(processed['keywords'][:5])}")
        
        print(f"\n✅ Query Processing Test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Query Processing Test FAILED: {str(e)}")
        return False


def test_answer_generator():
    """Test answer generation"""
    print("\n" + "="*60)
    print("TEST 3: Answer Generation")
    print("="*60)
    
    generator = AnswerGenerator()
    
    # Mock results
    mock_results = [
        ({
            'content': 'Sleep is essential for health. Adults need 7-9 hours per night. Quality sleep improves memory, mood, and immune function. Good sleep hygiene includes maintaining a consistent schedule.',
            'topic': 'sleep',
            'source': 'sleep.txt',
            'chunk_id': 'sleep_chunk_0'
        }, 0.85),
        ({
            'content': 'Creating a relaxing bedtime routine helps improve sleep quality. Keep your bedroom cool and dark. Avoid screens before bed.',
            'topic': 'sleep',
            'source': 'sleep.txt',
            'chunk_id': 'sleep_chunk_1'
        }, 0.78)
    ]
    
    try:
        query = "How much sleep do I need?"
        answer_dict = generator.generate_answer(query, mock_results)
        
        # Validate
        assert 'answer' in answer_dict, "Missing answer"
        assert 'confidence' in answer_dict, "Missing confidence"
        assert 'sources' in answer_dict, "Missing sources"
        assert 'key_points' in answer_dict, "Missing key points"
        
        print(f"\n✓ Query: '{query}'")
        print(f"  Answer: {answer_dict['answer'][:100]}...")
        print(f"  Confidence: {answer_dict['confidence']} ({answer_dict['confidence_score']:.2f})")
        print(f"  Sources: {answer_dict['sources']}")
        print(f"  Key Points: {len(answer_dict['key_points'])}")
        
        # Test formatting
        formatted = generator.format_answer(answer_dict)
        assert len(formatted) > 0, "Empty formatted answer"
        
        print(f"\n✅ Answer Generation Test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Answer Generation Test FAILED: {str(e)}")
        return False


def test_vector_store():
    """Test vector store creation and search"""
    print("\n" + "="*60)
    print("TEST 4: Vector Store")
    print("="*60)
    
    try:
        from src.rag.vector_store import VectorStore
        
        # Check if vector store exists
        vector_store = VectorStore()
        
        if vector_store.load_index():
            print("✓ Vector store loaded from disk")
            
            # Get statistics
            stats = vector_store.get_statistics()
            print(f"\n  Total vectors: {stats['total_vectors']}")
            print(f"  Embedding dimension: {stats['embedding_dimension']}")
            print(f"  Topics: {', '.join(stats['topics'])}")
            
            # Test search
            test_query = "How to improve sleep quality?"
            results = vector_store.search(test_query, top_k=3)
            
            print(f"\n✓ Search test: '{test_query}'")
            print(f"  Found {len(results)} results")
            
            if results:
                for i, (chunk, score) in enumerate(results, 1):
                    print(f"  {i}. Topic: {chunk['topic']}, Score: {score:.3f}")
            
            print(f"\n✅ Vector Store Test PASSED")
            return True
        else:
            print("⚠ Vector store not found - needs to be built first")
            print("  Run: python src/rag/vector_store.py")
            return False
            
    except Exception as e:
        print(f"\n❌ Vector Store Test FAILED: {str(e)}")
        return False


def test_end_to_end():
    """Test complete RAG pipeline"""
    print("\n" + "="*60)
    print("TEST 5: End-to-End RAG Pipeline")
    print("="*60)
    
    try:
        from src.rag.health_search import search_health_docs, get_system_stats
        
        # Get system stats
        stats = get_system_stats()
        
        if stats.get('status') == 'not_initialized':
            print("⚠ RAG system not initialized - building vector store...")
            from src.rag.vector_store import build_vector_store
            build_vector_store()
        
        # Test queries
        test_queries = [
            "How much sleep do adults need?",
            "What are the benefits of staying hydrated?",
            "Best exercises for beginners"
        ]
        
        for query in test_queries:
            print(f"\n{'='*60}")
            print(f"Query: '{query}'")
            print('='*60)
            
            response = search_health_docs(query, return_detailed=True)
            
            # Validate response
            assert isinstance(response, dict), "Response should be a dictionary"
            assert 'answer' in response, "Missing answer in response"
            
            print(f"\nAnswer: {response['answer'][:200]}...")
            print(f"Confidence: {response['confidence']} ({response['confidence_score']:.2f})")
            print(f"Sources: {response['sources']}")
            print(f"Key Points: {len(response['key_points'])}")
        
        print(f"\n✅ End-to-End Test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ End-to-End Test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("HEALTHWISE AI RAG SYSTEM TEST SUITE")
    print("="*60)
    
    results = {
        'Document Processing': test_document_processor(),
        'Query Processing': test_query_processor(),
        'Answer Generation': test_answer_generator(),
        'Vector Store': test_vector_store(),
        'End-to-End Pipeline': test_end_to_end()
    }
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

# Made with Bob
