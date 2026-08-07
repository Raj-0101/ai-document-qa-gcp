from google.cloud import firestore_v1
from app.config import PROJECT_ID


class FirestoreService:

    def __init__(self):
        self.db = firestore_v1.Client(
            project=PROJECT_ID,
            database="default"
        )
        self.collection = self.db.collection("documents")

    def save_document(self, filename: str, text: str):

        doc_ref = self.collection.document()

        doc_ref.set({
            "filename": filename,
            "text": text
        })

        return doc_ref.id

    def get_document(self, document_id: str):

        doc = self.collection.document(document_id).get()

        if doc.exists:
            return doc.to_dict()

        return None