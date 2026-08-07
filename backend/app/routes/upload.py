from fastapi import APIRouter, UploadFile, File

from app.services.storage_service import StorageService
from app.services.pdf_service import PDFService
from app.services.firestore_service import FirestoreService

router = APIRouter(prefix="/api")

storage = StorageService()
firestore = FirestoreService()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Upload PDF to Cloud Storage
    storage.upload_pdf(file)

    # Reset file pointer
    file.file.seek(0)

    # Extract text
    text = PDFService.extract_text(file)

    # Save metadata and extracted text to Firestore
    document_id = firestore.save_document(
        filename=file.filename,
        text=text
    )

    return {
        "document_id": document_id,
        "filename": file.filename,
        "characters": len(text),
        "preview": text[:300]
    }