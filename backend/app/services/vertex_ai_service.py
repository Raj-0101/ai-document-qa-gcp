import vertexai
from vertexai.generative_models import GenerativeModel

from app.config import PROJECT_ID, LOCATION


class VertexAIService:

    def __init__(self):
        vertexai.init(
            project=PROJECT_ID,
            location=LOCATION
        )

        self.model = GenerativeModel("gemini-2.5-flash")

    def ask_question(self, document_text: str, question: str):

        prompt = f"""
You are an AI assistant.

Answer ONLY using the document below.

Document:
{document_text}

Question:
{question}
"""

        response = self.model.generate_content(prompt)

        return response.text