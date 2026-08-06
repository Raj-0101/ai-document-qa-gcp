from fastapi import APIRouter, UploadFile, File

from app.services.storage_service import StorageService

router = APIRouter(prefix="/api")

storage = StorageService()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    result = storage.upload_pdf(file)
    return result