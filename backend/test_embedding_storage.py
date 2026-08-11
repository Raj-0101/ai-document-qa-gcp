from app.services.firestore_service import FirestoreService
from app.services.embedding_service import EmbeddingService


firestore = FirestoreService()
embedding_service = EmbeddingService()

document_id = "q9ANjjsG1eo09fBbQ083"

text = "Cloud Run allows applications to run containers."

embedding = embedding_service.create_embedding(text)

firestore.update_chunk_embedding(
    document_id=document_id,
    chunk_index=0,
    embedding=embedding
)

print("Embedding stored successfully!")
print("Dimensions:", len(embedding))