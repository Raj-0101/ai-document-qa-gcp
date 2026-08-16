import math

from app.services.firestore_service import FirestoreService
from app.services.embedding_service import EmbeddingService


class RetrievalService:

    def __init__(self):
        self.firestore = FirestoreService()
        self.embedding_service = EmbeddingService()

    @staticmethod
    def cosine_similarity(
        vector_a: list[float],
        vector_b: list[float]
    ):

        if not vector_a or not vector_b:
            return 0.0

        dot_product = sum(
            a * b
            for a, b in zip(vector_a, vector_b)
        )

        magnitude_a = math.sqrt(
            sum(a * a for a in vector_a)
        )

        magnitude_b = math.sqrt(
            sum(b * b for b in vector_b)
        )

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (
            magnitude_a * magnitude_b
        )

    def search(
        self,
        document_id: str,
        question: str,
        top_k: int = 3,
        similarity_threshold: float = 0.55
    ):

        # Create embedding for the question
        question_embedding = (
            self.embedding_service.create_query_embedding(
                question
            )
        )

        # Get document chunks
        chunks = self.firestore.get_chunks(
            document_id
        )

        results = []

        for chunk in chunks:

            similarity = self.cosine_similarity(
                question_embedding,
                chunk["embedding"]
            )

            # Ignore weak matches
            if similarity >= similarity_threshold:

                results.append({
                    "chunk_index": chunk["chunk_index"],
                    "text": chunk["text"],
                    "similarity": similarity
                })

        # Highest similarity first
        results.sort(
            key=lambda item: item["similarity"],
            reverse=True
        )

        return results[:top_k]