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

    def save_chunks(self, document_id: str, chunks: list[str]):

        chunks_collection = (
            self.collection
            .document(document_id)
            .collection("chunks")
        )

        for index, chunk in enumerate(chunks):

            chunks_collection.document(str(index)).set({
                "chunk_index": index,
                "text": chunk
            })

    def update_chunk_embedding(
        self,
        document_id: str,
        chunk_index: int,
        embedding: list[float]
    ):

        chunk_ref = (
            self.collection
            .document(document_id)
            .collection("chunks")
            .document(str(chunk_index))
        )

        chunk_ref.update({
            "embedding": embedding
        })

    def save_chunks_with_embeddings(
        self,
        document_id: str,
        chunks: list[str],
        embeddings: list[list[float]]
    ):

        chunks_collection = (
            self.collection
            .document(document_id)
            .collection("chunks")
        )

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):

            chunks_collection.document(str(index)).set({
                "chunk_index": index,
                "text": chunk,
                "embedding": embedding
            })

    def get_chunks(self, document_id: str):

        chunks_collection = (
            self.collection
            .document(document_id)
            .collection("chunks")
        )

        documents = chunks_collection.stream()

        chunks = []

        for doc in documents:

            data = doc.to_dict()

            chunks.append({
                "chunk_index": data.get("chunk_index"),
                "text": data.get("text", ""),
                "embedding": data.get("embedding", [])
            })

        return chunks