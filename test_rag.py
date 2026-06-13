from src.rag.health_search import search_health_docs

print("Starting test...")

result = search_health_docs("stress")

print("RESULT:")
print(result)