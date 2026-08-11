from google import genai
from google.genai.types import EmbedContentConfig

from app.config import PROJECT_ID, LOCATION


class EmbeddingService:

    def __init__(self):
        self.client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location=LOCATION
        )

    def create_embedding(self, text: str):

        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
            config=EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT"
            )
        )

        return response.embeddings[0].values

    def create_query_embedding(self, text: str):

        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
            config=EmbedContentConfig(
                task_type="RETRIEVAL_QUERY"
            )
        )

        return response.embeddings[0].values