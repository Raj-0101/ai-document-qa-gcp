from google import genai
from google.genai.types import HttpOptions

from app.config import PROJECT_ID, LOCATION


class VertexAIService:

    def __init__(self):
        self.client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location=LOCATION,
            http_options=HttpOptions(api_version="v1"),
        )

    def ask_question(self, document_text: str, question: str):

        prompt = f"""
You are an intelligent document assistant.

Answer ONLY using the information contained in the document.

If the answer is not present in the document, reply:

"I couldn't find that information in the uploaded document."

Document:

{document_text}

Question:

{question}
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text