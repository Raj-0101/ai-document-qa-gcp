from app.services.embedding_service import EmbeddingService


service = EmbeddingService()

text = "Cloud Run allows applications to run containers."

embedding = service.create_embedding(text)

print("Embedding created successfully!")
print("Dimensions:", len(embedding))
print("First 10 values:", embedding[:10])