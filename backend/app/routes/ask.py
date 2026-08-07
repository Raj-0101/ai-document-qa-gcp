from fastapi import APIRouter, HTTPException

from app.models.question import QuestionRequest
from app.services.firestore_service import FirestoreService
from app.services.vertex_ai_service import VertexAIService

router = APIRouter(prefix="/api")

firestore = FirestoreService()
vertex = VertexAIService()


@router.post("/ask")
async def ask_document(request: QuestionRequest):

    document = firestore.get_document(request.document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    answer = vertex.ask_question(
        document["text"],
        request.question
    )

    return {
        "document_id": request.document_id,
        "question": request.question,
        "answer": answer
    }