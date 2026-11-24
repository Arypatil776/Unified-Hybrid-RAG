# UniGrant AI

**Unified Hybrid RAG for Structured and Unstructured Enterprise Intelligence**

UniGrant AI is a university information assistant that combines structured database retrieval and semantic document search. It uses an LLM-based query planner to understand user queries and route them to SQL, vector search, or both.

## Features

- LLM-based query planning and intent classification.
- SQL retrieval from structured university data.
- Semantic search over university policy documents.
- Hybrid retrieval combining SQL and document evidence.
- Deterministic grant eligibility verification.
- Grounded answer generation using retrieved evidence.

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| Frontend | Streamlit |
| Database | SQLite |
| Vector Store | ChromaDB |
| Embeddings | Sentence Transformers |
| LLM | Groq API |

## Project Structure

```text
Hybrid-RAG/
├── app.py
├── config.py
├── requirements.txt
├── database/
├── documents/
├── ingestion/
├── retrieval/
├── generation/
├── chroma_db/
└── logs/
```

## Setup and Execution

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Configure environment variables**

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

**3. Initialize the database**

```bash
python -m database.setup_db
```

**4. Ingest documents**

```bash
python -m ingestion.ingest
```

**5. Start the application**

```bash
streamlit run app.py
```

## Example Queries

| Route | Example |
|---|---|
| SQL | How many IT students are there? |
| VECTOR | What are the research grant requirements? |
| HYBRID | Is student 1 eligible for the Research Excellence Grant? |

## Note

The application uses synthetic student records and sample grant policies for demonstration purposes.