from google.cloud import storage
from app.config import BUCKET_NAME

class StorageService:
    def __init__(self):
        self.client = storage.Client()
        self.bucket = self.client.bucket(BUCKET_NAME)

    def upload_pdf(self, file):
        blob = self.bucket.blob(file.filename)
        blob.upload_from_file(
            file.file,
            content_type=file.content_type
        )

        return {
            "filename": file.filename,
            "gcs_path": f"gs://{BUCKET_NAME}/{file.filename}"
        }