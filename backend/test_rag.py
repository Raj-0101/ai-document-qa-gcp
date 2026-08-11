from app.services.retrieval_service import RetrievalService
from app.services.vertex_ai_service import VertexAIService


DOCUMENT_ID = "NK6idUtXN9cz49iIvcKG"

question = "What is the CGPA of the student?"


retrieval = RetrievalService()
vertex = VertexAIService()


# 1. Retrieve relevant chunks
results = retrieval.search(
    document_id=DOCUMENT_ID,
    question=question,
    top_k=3
)


print("\nRetrieved chunks:\n")

for result in results:
    print(
        f"Chunk {result['chunk_index']} "
        f"| Similarity: {result['similarity']:.4f}"
    )
    print(result["text"])
    print("-" * 60)


# 2. Combine retrieved chunks
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
{question}

Answer clearly and briefly.
"""


# 4. Ask Gemini
response = vertex.client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)


print("\nAI Answer:")
print(response.text)