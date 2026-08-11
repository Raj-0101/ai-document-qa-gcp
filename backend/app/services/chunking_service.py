class ChunkingService:

    @staticmethod
    def create_chunks(
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200
    ):

        if not text:
            return []

        words = text.split()

        chunks = []
        start = 0

        while start < len(words):

            chunk_words = words[start:start + chunk_size]

            if chunk_words:
                chunks.append(" ".join(chunk_words))

            start += chunk_size - overlap

        return chunks