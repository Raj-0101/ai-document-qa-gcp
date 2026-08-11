from app.services.firestore_service import FirestoreService
from app.services.embedding_service import EmbeddingService


firestore = FirestoreService()
embedding_service = EmbeddingService()


chunks = [
    "Google Cloud Storage is used to store files.",
    "Firestore is a NoSQL database.",
    "Vertex AI provides generative AI services.",
    "Cloud Run runs applications in containers.",
    "Google Cloud provides many cloud services."
]


document_id = firestore.save_document(
    filename="embedding-test.txt",
    text="\n".join(chunks)
)


embeddings = []

for chunk in chunks:

    embedding = embedding_service.create_embedding(chunk)

    embeddings.append(embedding)

    print(
        f"Created embedding: {len(embedding)} dimensions"
    )


firestore.save_chunks_with_embeddings(
    document_id=document_id,
    chunks=chunks,
    embeddings=embeddings
)


print("\nSuccess!")
print("Document ID:", document_id)
print("Chunks:", len(chunks))
print("Embeddings:", len(embeddings))