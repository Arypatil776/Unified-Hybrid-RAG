
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = BASE_DIR / "documents"
CHROMA_DIR = BASE_DIR / "chroma_db"

# Embedding model
MODEL_NAME = "all-MiniLM-L6-v2"

CHUNK_SIZE = 600
CHUNK_OVERLAP = 100


def load_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        if text.strip():
            documents.append({
                "text": text,
                "source": file_path.name
            })

    return documents


def split_into_chunks(text):
    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def ingest_documents():
    print("Loading documents...")
    documents = load_documents()

    if not documents:
        print("No .txt documents found!")
        return

    print(f"Loaded {len(documents)} documents.")

    # Load embedding model
    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    all_chunks = []
    all_metadata = []
    all_ids = []

    # Chunk every document
    for document in documents:
        chunks = split_into_chunks(document["text"])

        for index, chunk in enumerate(chunks):
            all_chunks.append(chunk)

            all_metadata.append({
                "source": document["source"],
                "chunk_number": index
            })

            all_ids.append(
                f'{document["source"]}_{index}'
            )

    print(f"Created {len(all_chunks)} chunks.")

    # Generate embeddings
    print("Generating embeddings...")
    embeddings = model.encode(
        all_chunks,
        normalize_embeddings=True
    ).tolist()

    # Connect to persistent ChromaDB
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    collection = client.get_or_create_collection(
        name="university_documents",
        metadata={"hnsw:space": "cosine"}
    )

    # Clear previous data to avoid duplicates on reruns
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    # Store chunks and embeddings
    collection.add(
        ids=all_ids,
        documents=all_chunks,
        embeddings=embeddings,
        metadatas=all_metadata
    )

    print("\nIngestion completed successfully!")
    print(f"Documents: {len(documents)}")
    print(f"Chunks stored: {len(all_chunks)}")
    print(f"ChromaDB location: {CHROMA_DIR}")


if __name__ == "__main__":
    ingest_documents()