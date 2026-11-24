
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"

MODEL_NAME = "all-MiniLM-L6-v2"

# Load the same embedding model used during ingestion
model = SentenceTransformer(MODEL_NAME)

# Connect to persistent ChromaDB
client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name="university_documents"
)


def search_documents(query, top_k=3):
    """Find the most relevant policy document chunks."""

    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count())
    )

    retrieved_documents = []

    for i in range(len(results["documents"][0])):
        retrieved_documents.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })

    return retrieved_documents


if __name__ == "__main__":
    question = "What are the eligibility requirements for research grants?"

    results = search_documents(question)

    print("\n--- Semantic Search Results ---")

    for result in results:
        print("\nSource:", result["source"])
        print("Distance:", round(result["distance"], 4))
        print("Content:\n", result["text"])
