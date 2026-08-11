from fastapi import APIRouter, HTTPException

from app.models.question import QuestionRequest
from app.services.retrieval_service import RetrievalService
from app.services.vertex_ai_service import VertexAIService


router = APIRouter(prefix="/api")


retrieval = RetrievalService()
vertex = VertexAIService()


@router.post("/ask")
async def ask_document(request: QuestionRequest):

    # 1. Retrieve relevant chunks
    results = retrieval.search(
        document_id=request.document_id,
        question=request.question,
        top_k=3
    )

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No relevant content found in the document."
        )

    # 2. Build context from retrieved chunks
    context = "\n\n".join(
        result["text"]
        for result in results
    )

    # 3. Create RAG prompt
    prompt = f"""
You are an AI document assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer is not present in the context, say:
"I couldn't find that information in the document."

Context:
{context}

Question:
{request.question}

Answer clearly and briefly.
"""

    # 4. Generate answer with Gemini
    response = vertex.client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "document_id": request.document_id,
        "question": request.question,
        "answer": response.text,
        "sources": [
            {
                "chunk_index": result["chunk_index"],
                "similarity": result["similarity"]
            }
            for result in results
        ]
    }