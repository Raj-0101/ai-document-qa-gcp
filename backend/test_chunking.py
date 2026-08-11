from app.services.chunking_service import ChunkingService


text = """
Google Cloud Platform provides many cloud services.
Cloud Storage is used to store files.
Firestore is a NoSQL database.
Vertex AI provides machine learning and generative AI services.
Cloud Run allows applications to run in containers.
"""

chunks = ChunkingService.create_chunks(
    text,
    chunk_size=10,
    overlap=2
)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {i} ---")
    print(chunk)