
# UniGrant AI - Prompt Engineering Documentation

## Project Details
- **Project Name:** UniGrant AI
- **Problem Statement:** Unified Hybrid RAG for Structured and Unstructured Enterprise Intelligence
- **Tech Stack:** Python, SQLite, ChromaDB, Sentence Transformers, Groq API, Streamlit

---

## 1. Problem Understanding and Solution Design

### Prompt 1: Understanding the Problem
I have this problem statement about building a hybrid RAG system for a university. Data is stored in two places: structured data like student records and enrollments in a database, and unstructured data like grant policies and research documents. Explain what exactly needs to be built and what features are important for the solution.

**What I got from it:**
- Understood the difference between structured and unstructured data.
- Identified that both SQL and vector search are required.
- Understood why a query router is needed.

### Prompt 2: Planning the Architecture
Suggest a simple but effective architecture for this project. I want to use Python, SQLite, ChromaDB, Sentence Transformers and an LLM API. Divide the project into separate folders and modules so that the code is easy to manage. Also explain how the different modules will communicate with each other.

**What I got from it:**
- Created separate modules for database, ingestion, retrieval and generation.
- Decided to use SQLite for structured data and ChromaDB for document search.
- Kept the project modular instead of writing everything in one file.

---

## 2. Database Design and Synthetic Data

### Prompt 3: Creating the Database
Help me create the SQLite database for this project. I need tables for students, courses, enrollments and grants. Add proper primary keys and foreign keys and insert some sample data so I can test different types of queries. Give me the complete code and explain how to run it.

**What I got from it:**
- Created the required database tables.
- Added sample student, course, enrollment and grant records.
- Created a database that could be used for testing SQL retrieval.

---

## 3. Document Ingestion and Vector Storage

### Prompt 4: Building the Ingestion Pipeline
Now help me implement the document ingestion part. I have text files containing grant policies. Read these files, split the text into chunks with some overlap, generate embeddings using Sentence Transformers and store everything in ChromaDB. Make sure the database persists so I don't have to ingest everything again whenever I run the application.

**What I got from it:**
- Implemented document loading and chunking.
- Used `all-MiniLM-L6-v2` for embeddings.
- Stored document chunks in persistent ChromaDB storage.

### Prompt 5: Creating Vector Retrieval
Now create a separate Python file for retrieving documents. When a user asks something, search ChromaDB for the most relevant chunks and return the text along with its source. Keep it compatible with the ingestion code we already created.

**What I got from it:**
- Implemented semantic search.
- Retrieved relevant document chunks with source information.
- Tested retrieval using grant-related questions.

---

## 4. Intelligent Query Planning and Retrieval

### Prompt 6: Initial Query Router
Create a query router that decides whether a question should go to SQL, vector search or both. For example, questions about student count should go to SQL, questions about grant requirements should go to vector search, and eligibility questions should use both. Give me code that I can directly add to the project.

**What I got from it:**
- Created the initial rule-based query router.
- Tested different questions for SQL, VECTOR and HYBRID routes.

### Prompt 7: Improving the Router Using an LLM
The keyword-based router is limited because users can ask the same question in different ways. Can we improve this using Groq? I want the LLM to understand the question and return JSON containing the intent, route, student ID, branch, year, minimum GPA and grant name. Include validation so that the output follows the expected format.

**What I got from it:**
- Created an LLM-based query planner.
- Added intent classification and extraction of useful parameters.
- Tested it with student details, GPA filtering, grant policies and eligibility questions.

### Prompt 8: Connecting the Planner to Retrieval
Now integrate this query planner with the SQL and vector retrievers we have already built. Use the intent and extracted values from the planner to decide which database function to call. For hybrid questions, retrieve both SQL data and relevant document chunks. Don't unnecessarily change the modules that are already working.

**What I got from it:**
- Connected the query planner to the hybrid retriever.
- Used the extracted parameters for SQL retrieval.
- Combined SQL results and document evidence into one context.

---

## 5. Answer Generation and Eligibility Verification

### Prompt 9: Generating Answers Using Groq
Now implement the answer generator using the Groq API. It should take the user's question and the context returned by the retriever and generate a proper answer. Make sure it uses the retrieved information instead of making up answers. Also handle cases where the database or documents don't contain enough information.

**What I got from it:**
- Integrated Groq for answer generation.
- Passed SQL and document evidence to the LLM.
- Added instructions to avoid unsupported answers.

### Prompt 10: Eligibility Verification
I also need to check whether a particular student is eligible for a grant. Implement this separately so that it checks the student's GPA and year against the grant requirements. It should also identify the documents required for the application. Don't assume that a student has submitted those documents just because they are listed in the policy.

**What I got from it:**
- Implemented deterministic GPA and year checks.
- Retrieved required documents from grant policies.
- Kept academic eligibility separate from document submission status.

### Prompt 11: Improving Answer Quality
Some questions need different kinds of answers. For example, student details should show the profile, filtering questions should list matching students, and average GPA questions should show the SQL result directly. Improve the answer generation instructions to handle these cases properly. Also make sure that an eligibility verification result doesn't interfere with unrelated questions.

**What I got from it:**
- Improved responses for different query intents.
- Added better handling of SQL results and empty results.
- Made the answer generator use retrieved evidence as the source of truth.

---

## 6. Application Development

### Prompt 12: Building the Streamlit Application
Now create the Streamlit frontend for the project. I want a chat interface where users can enter questions and get answers from the hybrid RAG system. Add chat history, some example questions and a section where I can see the retrieved SQL and document information. Also mention clearly that the data is synthetic.

**What I got from it:**
- Created the Streamlit chat interface.
- Connected the frontend to retrieval and generation.
- Added sample questions, chat history and retrieval details.

---

## 7. Testing and Debugging

### Prompt 13: Testing Individual Modules
Give me test cases for the modules we have built so far. I want to verify that SQL retrieval, vector retrieval, query planning and eligibility verification are all working correctly. If something fails, help me fix that without rewriting the entire code.

**What I got from it:**
- Tested database queries and aggregate functions.
- Checked document retrieval.
- Tested the LLM query planner with different questions.
- Verified the eligibility logic.

### Prompt 14: Testing the Complete Application
Now give me some questions to test the complete application. Include SQL-only, vector-only and hybrid questions. I want to check whether the correct route is selected, the correct information is retrieved and the final answer makes sense.

**What I got from it:**
- Tested student count and filtering questions.
- Tested grant policy questions.
- Tested student grant eligibility questions.
- Verified that the complete Streamlit application works.

---

## 8. Demonstration Queries

These are the questions used to demonstrate the three retrieval routes:

| Type | Question |
|---|---|
| SQL | How many IT students are there? |
| VECTOR | What are the research grant requirements? |
| HYBRID | Is student 1 eligible for the Research Excellence Grant? |

---

## 9. Important Design Decisions

During development, the following decisions were made:

- Used SQLite because the structured university data is relational.
- Used ChromaDB for storing and searching document embeddings.
- Used Sentence Transformers to generate embeddings locally.
- Used Groq for query planning and answer generation.
- Used deterministic Python logic for eligibility checks instead of relying entirely on the LLM.
- Kept SQL retrieval restricted to SELECT queries.
- Used parameterized SQL queries for extracted values.
- Kept the query planner responsible for understanding and routing questions, not providing factual answers.
- Used synthetic university data for the demonstration.
- Made the system communicate when information is missing instead of assuming it exists.

---

## 10. Final Summary

Built UniGrant AI as a hybrid RAG application that can understand user questions, decide whether to use SQL or vector search, retrieve information from both sources when needed, and generate answers using the retrieved evidence.

The project combines database retrieval, semantic search, LLM-based query planning, deterministic eligibility verification and a Streamlit interface.

**Note:** The prompts in this document are reconstructed to represent the development interactions and are not exact copies of every original conversation.
