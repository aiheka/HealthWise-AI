"""
RAG System Configuration
Contains all configurable parameters for the enhanced RAG system
"""

# Embedding Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # 384 dimensions, fast
# Alternative: "sentence-transformers/all-mpnet-base-v2"  # 768 dimensions, more accurate

# Document Processing Configuration
CHUNK_SIZE = 512  # tokens per chunk
CHUNK_OVERLAP = 50  # token overlap between chunks
MIN_CHUNK_SIZE = 100  # minimum chunk size to keep

# Vector Store Configuration
VECTOR_STORE_PATH = "data/vector_store"
FAISS_INDEX_NAME = "health_knowledge_base"
DISTANCE_METRIC = "cosine"  # cosine, euclidean, or dot_product

# Retrieval Configuration
TOP_K_CHUNKS = 5  # number of chunks to retrieve
SIMILARITY_THRESHOLD = 0.65  # minimum similarity score (0-1)
MAX_CONTEXT_LENGTH = 2048  # maximum tokens in context

# Answer Generation Configuration
ANSWER_TEMPLATE = """Based on the health information available:

{context}

Answer: {answer}

💡 Key Points:
{key_points}

📚 Sources: {sources}
"""

# Query Processing Configuration
EXPAND_QUERIES = True  # enable query expansion
REMOVE_STOPWORDS = False  # keep stopwords for better context
HEALTH_SYNONYMS = {
    "sleep": ["rest", "sleeping", "slumber", "nap"],
    "exercise": ["workout", "physical activity", "fitness", "training"],
    "stress": ["anxiety", "tension", "pressure", "worry"],
    "hydration": ["water", "fluid", "drinking"],
    "nutrition": ["diet", "food", "eating", "meal"],
}

# Health Topics
HEALTH_TOPICS = [
    "sleep",
    "hydration",
    "nutrition",
    "exercise",
    "stress"
]

# Confidence Thresholds
HIGH_CONFIDENCE = 0.8
MEDIUM_CONFIDENCE = 0.65
LOW_CONFIDENCE = 0.5

# Health Disclaimer
HEALTH_DISCLAIMER = """
⚠️ **Important**: This information is for educational purposes only and should not replace professional medical advice. 
Always consult with a healthcare provider for personalized medical guidance.
"""

# Made with Bob
