from app.services.firestore_service import FirestoreService
from app.services.chunking_service import ChunkingService


text = """
Google Cloud Platform provides many cloud services.
Cloud Storage is used to store files.
Firestore is a NoSQL database.
Vertex AI provides machine learning and generative AI services.
Cloud Run allows applications to run in containers.
"""

# Create chunks
chunks = ChunkingService.create_chunks(
    text,
    chunk_size=10,
    overlap=2
)

# Create Firestore service
firestore = FirestoreService()

# Create a test document
document_id = firestore.save_document(
    filename="test-document.txt",
    text=text
)

# Save chunks
firestore.save_chunks(
    document_id=document_id,
    chunks=chunks
)

print("Document ID:", document_id)
print("Number of chunks saved:", len(chunks))
print("Success!")