from fastapi import APIRouter, HTTPException

from app.models.question import QuestionRequest
from app.services.retrieval_service import RetrievalService
from app.services.vertex_ai_service import VertexAIService


router = APIRouter(prefix="/api")


retrieval = RetrievalService()
vertex = VertexAIService()


@router.post("/ask")
async def ask_document(request: QuestionRequest):

    try:
        # 1. Retrieve relevant chunks
        results = retrieval.search(
            document_id=request.document_id,
            question=request.question,
            top_k=3
        )

        # 2. No relevant information found
        if not results:
            return {
                "document_id": request.document_id,
                "question": request.question,
                "answer": "I couldn't find that information in the document.",
                "sources": []
            }

        # 3. Build context
        context = "\n\n".join(
            result["text"]
            for result in results
        )

        # 4. RAG prompt
        prompt = f"""
You are an AI document assistant.

Answer the user's question using ONLY the information
provided in the context below.

Do not use outside knowledge.

If the answer is not present in the context, say:
"I couldn't find that information in the document."

Context:
{context}

Question:
{request.question}

Answer clearly and briefly.
"""

        # 5. Ask Gemini
        response = vertex.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        # 6. Return answer + sources
        return {
            "document_id": request.document_id,
            "question": request.question,
            "answer": response.text,
            "sources": [
                {
                    "chunk_index": result["chunk_index"],
                    "similarity": result["similarity"],
                    "text": result["text"]
                }
                for result in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )