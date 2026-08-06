from app.services.vertex_ai_service import VertexAIService

ai = VertexAIService()

answer = ai.ask_question(
    "Google Cloud is a cloud computing platform.",
    "What is Google Cloud?"
)

print(answer)