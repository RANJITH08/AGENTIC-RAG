# 🤖 Agentic RAG

### Intelligent Full-Stack Retrieval-Augmented Generation System

> An Agentic RAG application that intelligently decides when to retrieve information, evaluates retrieved context, automatically reformulates unsuccessful queries, and generates context-grounded answers using LLMs.

---

## 🚀 Overview

This project is a full-stack **Agentic Retrieval-Augmented Generation (RAG)** application built to provide intelligent question answering over a private document knowledge base.

Unlike a traditional RAG system that always follows:

```text
User Query
    ↓
Retrieve Documents
    ↓
Generate Answer
```

this system introduces an agentic decision-making layer:

```text
User Query
    ↓
Agent Decision
    ↓
 ┌───────────────┐
 │               │
DIRECT        RETRIEVE
 │               │
 ▼               ▼
LLM          FAISS Search
                 ↓
          Retrieved Chunks
                 ↓
          Relevance Check
                 ↓
        ┌────────┴────────┐
        │                 │
      YES                 NO
        │                 │
        ▼                 ▼
Generate Answer     Reformulate Query
                          ↓
                     Retrieve Again
                          ↓
                    Relevance Check
                          ↓
                     Final Answer
```

The system therefore doesn't blindly retrieve and answer. It can decide, retrieve, evaluate, recover, and answer.

---

## ✨ Key Features

- 🧠 Intelligent Retrieval Routing
- 🔎 Semantic Vector Search
- 📚 Document-based Question Answering
- 🧪 LLM-based Relevance Checking
- 🔄 Automatic Query Reformulation
- ♻️ Controlled Retrieval Retries
- 💬 Context-Grounded Answer Generation
- 📊 Execution Trace Tracking
- 🖥️ Interactive Web Frontend
- ⚡ Groq-powered LLM inference
- 🗂️ FAISS Vector Database
- 🤗 Hugging Face Embeddings
- 🐍 Python Backend
- ⚛️ React + Vite Frontend

---

## 🧠 How Agentic RAG Works

### 1. User Query

The user submits a question through the frontend.

Example:

What is the employee work-from-home policy?


The query is sent to the backend.

### 2. Agent Decision

The LLM first determines whether the question requires information from the document knowledge base.

**Example — Direct Query**

User: Hello, how are you?
Agent: DIRECT

The system answers directly using the LLM.

**Example — Knowledge Query**

User: What is the company's leave policy?
Agent: RETRIEVE

The system starts the retrieval pipeline.

### 🔎 3. Semantic Retrieval

For retrieval-based queries, the system converts the query into an embedding using:

sentence-transformers/all-MiniLM-L6-v2


The embedding is searched against the FAISS vector database.

```text
User Query
    ↓
Embedding Model
    ↓
Query Vector
    ↓
FAISS Similarity Search
    ↓
Top 4 Document Chunks
```

The current retriever is configured to return `k = 4` document chunks.

### 🧪 4. Relevance Checking

Retrieved documents are not automatically trusted. The system sends the retrieved chunks to the LLM and asks whether they contain enough information to answer the original question.

Example:

Question: What is the refund policy?
Retrieved Documents: Information about employee attendance...
Relevance: NO
Reason: The retrieved documents do not contain refund information.


- If relevant (`YES`) → the system proceeds to answer generation.
- If not relevant (`NO`) → the system moves to query reformulation.

### 🔄 5. Query Reformulation

When retrieval fails, the LLM generates a better search query.

```text
Original Query
      +
Previous Search Query
      +
Relevance Failure Reason
      ↓
     LLM
      ↓
Improved Search Query
```

Example:

Original: What is the refund period?
↓ (poor retrieval)
Reformulated: refund policy return period eligibility


The new query is then sent to FAISS again.

### ♻️ 6. Controlled Retry

The system uses `MAX_RETRIES = 2`, preventing infinite retrieval loops:

Attempt 1 → Attempt 2 → Attempt 3


After the retry limit is reached, the system proceeds with the best available retrieved context.

### 💬 7. Final Answer Generation

Once relevant context is identified (or retries are exhausted), the system sends the retrieved information together with the original question to the LLM:

```text
Retrieved Context
       +
Original Question
       ↓
    Groq LLM
       ↓
 Final Answer
```

The generation prompt instructs the model to answer using only the provided context and to acknowledge when the context is insufficient.

---

## 📊 Execution Tracing

The application records the major stages of the Agentic RAG workflow. Each event contains:

- Step
- Detail
- Metadata
- Timestamp

```text
🤖 Agent Decision
        ↓
🔎 Retrieval
        ↓
🧪 Relevance Check
        ↓
🔄 Query Reformulation
        ↓
🔎 Retrieval Again
        ↓
🧪 Relevance Check
        ↓
💬 Final Answer
```

The backend represents these events using a `TraceEvent` structure. Supported event types:

agent_decision · retrieve · relevance_check · reformulate · answer_directly · final_answer · error


This makes the system easier to debug and allows execution information to be displayed live in the frontend.

---

## 🏗️ System Architecture

```text
                         ┌──────────────────┐
                         │      USER        │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ React Frontend   │
                         │     + Vite       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   FastAPI Python │
                         │     Backend      │
                         └────────┬─────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │    Agentic RAG       │
                       │      Engine          │
                       └──────────┬───────────┘
                                  │
                         ┌────────┴────────┐
                         │                 │
                         ▼                 ▼
                  Retrieval Router    Direct Answer
                         │                 │
                         ▼                 ▼
                  Hugging Face        Groq LLM
                    Embeddings
                         │
                         ▼
                    FAISS Vector DB
                         │
                         ▼
                  Retrieved Chunks
                         │
                         ▼
                  Relevance Checker
                         │
                   ┌─────┴─────┐
                   │           │
                  YES          NO
                   │           │
                   ▼           ▼
              Generate     Reformulate
               Answer         Query
                               │
                               ▼
                          Search Again
                               │
                               ▼
                         Final Answer
                               │
                               ▼
                         Trace Events
                               │
                               ▼
                         React Frontend
```

---

## 🛠️ Technology Stack

**Backend**

| Technology | Purpose |
|---|---|
| Python | Backend and AI application logic |
| FastAPI | REST API layer |
| LangChain | LLM and RAG orchestration |
| Groq | LLM inference |
| gpt-oss-120b | Language model |
| FAISS | Vector similarity search |
| Hugging Face | Embedding generation |
| Sentence Transformers | Semantic embeddings |

**Frontend**

| Technology | Purpose |
|---|---|
| React | User interface |
| Vite | Frontend build and development |
| JavaScript | Frontend logic |
| HTML/CSS | Interface structure and styling |

---

## 📁 Project Structure

```text
agentic-rag/
│
├── backend/
│   │
│   ├── agent.py
│   ├── ingest.py
│   ├── main.py
│   ├── test_agent.py
│   ├── requirements.txt
│   ├── .env.example
│   │
│   ├── pdfs/            (local only)
│   ├── uploads/         (local only, auto-created)
│   ├── vector_store/    (local only, auto-generated)
│   ├── .venv/           (local only)
│   └── .env             (local only, never committed)
│
├── frontend/
│   │
│   ├── public/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── .gitignore
│
├── .gitignore
└── README.md
```

> **Important:** The following directories/files are local-only and should not be committed:
> ```
> backend/.env
> backend/.venv/
> backend/__pycache__/
> backend/pdfs/
> backend/uploads/
> backend/vector_store/
> frontend/node_modules/
> ```

---

## 📚 Document Ingestion

The document ingestion pipeline converts source documents into searchable vector representations.

```text
PDF / Document
      ↓
Document Loading
      ↓
Text Extraction
      ↓
Text Splitting
      ↓
Document Chunks
      ↓
Hugging Face Embeddings
      ↓
FAISS Vector Store
```

The ingestion logic is implemented in `backend/ingest.py`. Run the ingestion process from the `backend/` directory:

```bash
python ingest.py --pdf_dir ./pdfs --out ./vector_store
```

This generates the local FAISS vector store. New documents can also be added later through the `/upload` API endpoint without rebuilding the whole index.

---

## ⚙️ Installation

### Prerequisites

- Python 3.10+
- Node.js & npm
- Git
- A Groq API Key ([console.groq.com](https://console.groq.com))

### 🔧 Backend Setup

Navigate to the backend:
```bash
cd backend
```

Create a Python virtual environment:

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 🔐 Environment Variables

Copy the example file and fill in your key:
```bash
cp .env.example .env
```

`backend/.env` should contain:

GROQ_API_KEY=your_groq_api_key
FAISS_INDEX_PATH=./vector_store


**Security Notice:** Never commit your `.env` file. If a key is ever accidentally pushed to GitHub, immediately revoke/rotate it.

### ▶️ Run the Backend

From the `backend/` directory, with your virtual environment active:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive docs (Swagger UI) are at `http://127.0.0.1:8000/docs`.

### 🖥️ Frontend Setup

Open a new terminal and navigate to:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Start the development server:
```bash
npm run dev
```

Open the local URL provided by Vite in your browser (usually `http://localhost:5173`).

> Both the backend and frontend must be running at the same time — the frontend calls the backend directly at `http://127.0.0.1:8000`.

---

## 🔗 Full Application Flow

Once the backend and frontend are running:

```text
Browser
   ↓
React Frontend
   ↓
FastAPI Backend
   ↓
Agentic RAG Engine
   ↓
┌──────────────────────────────┐
│                              │
│ Groq LLM                     │
│ Hugging Face Embeddings      │
│ FAISS Vector Database        │
│ Retrieval + Relevance Logic  │
│ Query Reformulation          │
│                              │
└──────────────────────────────┘
   ↓
Answer + Trace
   ↓
React Frontend
```

---

## 🧪 Testing

A standalone command-line test script is included for quickly checking the agent without running the full API:

```bash
cd backend
python test_agent.py "your question here"
```

This prints the full reasoning trace and final answer directly to the terminal — useful for validating changes to `agent.py` before wiring them into the API.

Areas covered manually via this script:
- Direct-answer routing
- Retrieval routing
- Empty/insufficient retrieval handling
- Relevance checking
- Query reformulation
- Retry limits
- Final answer generation

---

## 💻 Example

**User Query:**

What is the employee work-from-home policy?


**Trace:**
```text
Agent Decision   → RETRIEVE
Retrieval        → Retrieved 4 chunks
Relevance Check  → NO
                   The retrieved documents discuss office attendance
                   but do not contain the remote work policy.
Reformulated     → "remote work WFH employee policy eligibility approval"
Second Retrieval → Retrieved 4 chunks
Relevance Check  → YES
Final Answer     → The retrieved documents provide information about
                   the company's work-from-home policy...
```

## 📡 Example Trace

A typical `/chat` response:

```json
{
  "answer": "The requested information is available in the documents.",
  "trace": [
    {
      "step": "agent_decision",
      "detail": "Retrieve from documents",
      "meta": { "needs_retrieval": true }
    },
    {
      "step": "retrieve",
      "detail": "Retrieved 4 chunk(s)",
      "meta": { "num_chunks": 4 }
    },
    {
      "step": "relevance_check",
      "detail": "The retrieved context is relevant.",
      "meta": { "relevant": true }
    },
    {
      "step": "final_answer",
      "detail": "The requested information is available..."
    }
  ]
}
```

---

## 🧩 Core Components

**`backend/agent.py`** — The main Agentic RAG engine. Responsible for:
```text
LLM Initialization
       ↓
Embedding Initialization
       ↓
FAISS Loading
       ↓
Retrieval Decision
       ↓
Document Retrieval
       ↓
Relevance Checking
       ↓
Query Reformulation
       ↓
Answer Generation
       ↓
Trace Generation
```

**`backend/ingest.py`** — Processes documents and generates/updates the FAISS vector store:
```text
Documents → Load → Split → Embed → FAISS
```

**`backend/main.py`** — FastAPI application entry point. Connects the Agentic RAG engine with the frontend via `/chat`, `/upload`, and `/health` endpoints.

**`backend/test_agent.py`** — Command-line test script for validating agent behavior without the API layer.

**`frontend/`** — React + Vite user interface. Communicates with the backend API and displays generated answers alongside a live execution trace.

---

## 🧠 Why Agentic RAG?

Traditional RAG assumes:

Query → Retrieve → Generate


But retrieval can fail due to:
- Ambiguous questions
- Different terminology
- Poor query formulation
- Similar but irrelevant documents
- Large knowledge bases
- Missing keywords

Agentic RAG adds a reasoning layer:

Query → Decide → Retrieve → Evaluate → Recover if necessary → Generate


This makes the retrieval workflow more adaptive.

### 📊 Traditional RAG vs Agentic RAG

| Feature | Traditional RAG | This Project |
|---|---|---|
| Query Routing | ❌ | ✅ |
| Vector Search | ✅ | ✅ |
| Relevance Checking | Usually ❌ | ✅ |
| Query Reformulation | Usually ❌ | ✅ |
| Retry Mechanism | Limited | ✅ |
| Context Grounding | ✅ | ✅ |
| Execution Trace | Usually ❌ | ✅ |
| Adaptive Retrieval | Limited | ✅ |

---

## 🛡️ Reliability

- **Relevance Validation** — Retrieved documents are evaluated before final generation.
- **Query Reformulation** — Poor retrieval results trigger a new search query.
- **Bounded Retries** — The system cannot enter an infinite retrieval loop.
- **Context Grounding** — Final responses are generated using retrieved context.
- **Empty Retrieval Handling** — The application handles cases where no documents are retrieved.
- **Execution Tracing** — Every major stage can be monitored and debugged.

---

## ⚠️ Current Limitations

This project is an Agentic RAG foundation and can be improved further.

- **LLM-Based Relevance Evaluation** — The relevance checker depends on an LLM and may occasionally make incorrect judgments.
- **Retrieval Ranking** — The current system relies primarily on vector similarity retrieval.
- **Source Citations** — Document names, page numbers, and exact source references can be added to final answers.
- **Conversation Memory** — Multi-turn conversational memory can be added for more advanced use cases.
- **Production Observability** — The existing trace mechanism can be integrated with dedicated monitoring and evaluation platforms.

---

## 🚀 Future Improvements

- [ ] Source/document citations
- [ ] Page-level references
- [ ] Retrieval similarity thresholds
- [ ] Hybrid keyword + vector search
- [ ] Cross-encoder reranking
- [ ] Conversation memory
- [ ] Multi-document reasoning
- [ ] Streaming responses
- [ ] Structured LLM outputs / Pydantic validation
- [ ] Hallucination detection & RAG evaluation
- [ ] Automated evaluation datasets
- [ ] Docker deployment
- [ ] Authentication & rate limiting
- [ ] CI/CD & production monitoring

---

## 🔒 Security & Privacy

Private and generated data should never be committed to the repository. The following are excluded using `.gitignore`:

.env
.venv/
pycache/
backend/pdfs/
backend/uploads/
backend/vector_store/
frontend/node_modules/
*.pdf


**Never upload:** API keys, passwords, private documents, user-uploaded files, personal information, production credentials.

If an API key is accidentally pushed to GitHub, immediately revoke/rotate the key.

---

## 📈 Production Architecture

The project can be extended into a production AI system:

```text
                         ┌───────────────┐
                         │     User      │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ React Client  │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │    API Layer  │
                         └───────┬───────┘
                                 │
                                 ▼
                      ┌─────────────────────┐
                      │  Agentic RAG Engine │
                      └──────────┬──────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
                ▼                ▼                ▼
          Query Router      Retrieval       Generation
                │                │                │
                │                ▼                │
                │           Vector DB             │
                │                │                │
                └────────────────┼────────────────┘
                                 │
                                 ▼
                           Final Answer
                                 │
                                 ▼
                          Trace / Monitoring
```

---

## 🎓 Key Learning Outcomes

This project provided practical experience with:

Retrieval-Augmented Generation · Agentic AI · Large Language Models · LLM orchestration · Semantic search · Vector databases · Embeddings · Prompt engineering · Retrieval routing · Relevance grading · Query reformulation · Retry strategies · Context grounding · Python backend development · React frontend development · API integration · AI application architecture · Execution tracing

---

## 💡 Project Goal

The goal of this project was to move beyond simply calling an LLM API and build a more structured AI system where the LLM participates in decision-making and retrieval control.

Instead of:

LLM + Vector Database


the system follows:
```text
LLM
 ↓
Decision
 ↓
Retrieval
 ↓
Evaluation
 ↓
Recovery
 ↓
Generation
```

This architecture provides a foundation for building more adaptive and reliable AI applications.

---

## 👨‍💻 Author

**Ranjith**
AI / GenAI Engineer | Python Developer | Computer Science Graduate

**Areas of Interest:** Generative AI · Agentic AI · Retrieval-Augmented Generation · LLM Applications · AI Automation · Machine Learning · Python · AI Engineering

---

## ⭐ If You Find This Project Useful

If you find this project useful or interesting:

- ⭐ Star the repository
- 🍴 Fork the project
- 💬 Share your feedback
- 🤝 Connect with me
