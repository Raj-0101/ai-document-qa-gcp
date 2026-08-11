from fastapi import APIRouter, UploadFile, File

from app.services.storage_service import StorageService
from app.services.pdf_service import PDFService
from app.services.firestore_service import FirestoreService
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService


router = APIRouter(prefix="/api")


storage = StorageService()
firestore = FirestoreService()
embedding_service = EmbeddingService()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # 1. Upload PDF to Cloud Storage
    storage.upload_pdf(file)

    # 2. Reset file pointer
    file.file.seek(0)

    # 3. Extract text
    text = PDFService.extract_text(file)

    # 4. Save document
    document_id = firestore.save_document(
        filename=file.filename,
        text=text
    )

    # 5. Create chunks
    chunks = ChunkingService.create_chunks(
        text,
        chunk_size=1000,
        overlap=200
    )

    # 6. Generate embeddings
    embeddings = []

    for chunk in chunks:

        embedding = embedding_service.create_embedding(chunk)

        embeddings.append(embedding)

    # 7. Save chunks + embeddings
    firestore.save_chunks_with_embeddings(
        document_id=document_id,
        chunks=chunks,
        embeddings=embeddings
    )

    return {
        "document_id": document_id,
        "filename": file.filename,
        "characters": len(text),
        "chunks": len(chunks),
        "embedding_dimensions": (
            len(embeddings[0]) if embeddings else 0
        ),
        "preview": text[:300]
    }