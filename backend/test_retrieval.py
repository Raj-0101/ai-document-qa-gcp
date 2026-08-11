from app.services.retrieval_service import RetrievalService


DOCUMENT_ID = "NK6idUtXN9cz49iIvcKG"

question = "What are the student's grades?"


retrieval = RetrievalService()

results = retrieval.search(
    document_id=DOCUMENT_ID,
    question=question,
    top_k=3
)


print("\nTop matching chunks:\n")

for result in results:

    print(
        f"Chunk {result['chunk_index']} "
        f"| Similarity: {result['similarity']:.4f}"
    )

    print(result["text"])
    print("-" * 60)