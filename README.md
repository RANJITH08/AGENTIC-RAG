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

this system introduces an agentic decision-making layer:

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

The system therefore doesn't blindly retrieve and answer. It can decide, retrieve, evaluate, recover, and answer.

✨ Key Features
🧠 Intelligent Retrieval Routing
🔎 Semantic Vector Search
📚 Document-based Question Answering
🧪 LLM-based Relevance Checking
🔄 Automatic Query Reformulation
♻️ Controlled Retrieval Retries
💬 Context-Grounded Answer Generation
📊 Execution Trace Tracking
🖥️ Interactive Web Frontend
⚡ Groq-powered LLM inference
🗂️ FAISS Vector Database
🤗 Hugging Face Embeddings
🐍 Python Backend
⚛️ React + Vite Frontend
🧠 How Agentic RAG Works
1. User Query

The user submits a question through the frontend.

Example:

What is the employee work-from-home policy?

The query is sent to the backend.

2. Agent Decision

The LLM first determines whether the question requires information from the document knowledge base.

Example — Direct Query
User:
Hello, how are you?

Agent:
DIRECT

The system answers directly using the LLM.

Example — Knowledge Query
User:
What is the company's leave policy?

Agent:
RETRIEVE

The system starts the retrieval pipeline.

🔎 3. Semantic Retrieval

For retrieval-based queries, the system converts the query into an embedding using:

sentence-transformers/all-MiniLM-L6-v2

The embedding is searched against the FAISS vector database.

User Query
    ↓
Embedding Model
    ↓
Query Vector
    ↓
FAISS Similarity Search
    ↓
Top 4 Document Chunks

The current retriever is configured to return:

k = 4

document chunks.

🧪 4. Relevance Checking

Retrieved documents are not automatically trusted.

The system sends the retrieved chunks to the LLM and asks whether they contain enough information to answer the original question.

Example:

Question:
What is the refund policy?

Retrieved Documents:
Information about employee attendance...

Relevance:
NO

Reason:
The retrieved documents do not contain refund information.

If the retrieved information is relevant:

YES

the system proceeds to answer generation.

If it is not relevant:

NO

the system moves to query reformulation.

🔄 5. Query Reformulation

When retrieval fails, the LLM generates a better search query.

The reformulation process uses:

Original Query
      +
Previous Search Query
      +
Relevance Failure Reason
      ↓
     LLM
      ↓
Improved Search Query

Example:

Original:
What is the refund period?

        ↓

Poor Retrieval

        ↓

Reformulated:
refund policy return period eligibility

The new query is then sent to FAISS again.

♻️ 6. Controlled Retry

The system uses:

MAX_RETRIES = 2

This prevents infinite retrieval loops.

Maximum retrieval attempts:

Attempt 1
    ↓
Attempt 2
    ↓
Attempt 3

After the retry limit is reached, the system proceeds with the available retrieved context.

💬 7. Final Answer Generation

Once relevant context is identified, the system sends the retrieved information together with the original question to the LLM.

Retrieved Context
       +
Original Question
       ↓
    Groq LLM
       ↓
 Final Answer

The generation prompt instructs the model to answer using the provided context and acknowledge when the context is insufficient.

📊 Execution Tracing

The application records the major stages of the Agentic RAG workflow.

Each event contains:

Step
Detail
Metadata
Timestamp

Example:

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

The backend represents these events using a TraceEvent structure.

Supported events include:

agent_decision
retrieve
relevance_check
reformulate
answer_directly
final_answer
error

This makes the system easier to debug and allows execution information to be displayed in the frontend.

🏗️ System Architecture
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
                         │   Python API     │
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
🛠️ Technology Stack
Backend
Technology	Purpose
Python	Backend and AI application logic
LangChain	LLM and RAG orchestration
Groq	LLM inference
Llama 3.3 70B	Language model
FAISS	Vector similarity search
Hugging Face	Embedding generation
Sentence Transformers	Semantic embeddings
Frontend
Technology	Purpose
React	User interface
Vite	Frontend build and development
JavaScript	Frontend logic
HTML/CSS	Interface structure and styling
📁 Project Structure
agentic-rag/
│
├── backend/
│   │
│   ├── agent.py
│   ├── ingest.py
│   ├── main.py
│   ├── test_agent.py
│   ├── requirements.txt
│   │
│   ├── pdfs/
│   ├── uploads/
│   ├── vector_store/
│   ├── .venv/
│   └── .env
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
Important

The following directories/files are local-only and should not be committed:

backend/.env
backend/.venv/
backend/__pycache__/
backend/pdfs/
backend/uploads/
backend/vector_store/
frontend/node_modules/
📚 Document Ingestion

The document ingestion pipeline converts source documents into searchable vector representations.

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

The ingestion logic is implemented in:

backend/ingest.py

Run the ingestion process from the backend directory:

python ingest.py

This generates the local FAISS vector store.

⚙️ Installation
Prerequisites

Install:

Python 3.10+
Node.js
npm
Git
Groq API Key
🔧 Backend Setup

Navigate to the backend:

cd backend

Create a Python virtual environment:

Windows
python -m venv .venv

Activate:

.venv\Scripts\activate
macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt
🔐 Environment Variables

Create:

backend/.env

Add:

GROQ_API_KEY=your_groq_api_key
FAISS_INDEX_PATH=./vector_store
Security Notice

Never commit your .env file.

Create a safe example file:

backend/.env.example

Example:

GROQ_API_KEY=your_groq_api_key_here
FAISS_INDEX_PATH=./vector_store
▶️ Run the Backend

From the backend directory:

python main.py

The API will start according to the configuration defined in main.py.

🖥️ Frontend Setup

Open a new terminal.

Navigate to:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

Open the local URL provided by Vite in your browser.

🔗 Full Application Flow

Once the backend and frontend are running:

Browser
   ↓
React Frontend
   ↓
Backend API
   ↓
Agentic RAG Engine
   ↓
┌──────────────────────────────┐
│                              │
│ Groq LLM                     │
│ Hugging Face Embeddings      │
│ FAISS Vector Database        │
│ Retrieval + Relevance Logic  │
│ Query Reformulation           │
│                              │
└──────────────────────────────┘
   ↓
Answer + Trace
   ↓
React Frontend
🧪 Testing

The project contains:

backend/test_agent.py

Run tests using:

pytest

or:

python -m pytest

Potential test areas include:

Direct-answer routing
Retrieval routing
Empty retrieval handling
Relevance checking
Query reformulation
Retry limits
Final answer generation
💻 Example
User Query
What is the employee work-from-home policy?
Agent Decision
RETRIEVE
Retrieval
Retrieved 4 chunks
Relevance Check
NO

The retrieved documents discuss office attendance
but do not contain the remote work policy.
Reformulated Query
remote work WFH employee policy eligibility approval
Second Retrieval
Retrieved 4 chunks
Relevance Check
YES
Final Answer
The retrieved documents provide information about
the company's work-from-home policy...
📡 Example Trace

A typical response can contain:

{
  "answer": "The requested information is available in the documents.",
  "trace": [
    {
      "step": "agent_decision",
      "detail": "Retrieve from documents",
      "meta": {
        "needs_retrieval": true
      }
    },
    {
      "step": "retrieve",
      "detail": "Retrieved 4 chunk(s)",
      "meta": {
        "num_chunks": 4
      }
    },
    {
      "step": "relevance_check",
      "detail": "The retrieved context is relevant.",
      "meta": {
        "relevant": true
      }
    },
    {
      "step": "final_answer",
      "detail": "The requested information is available..."
    }
  ]
}
🧩 Core Components
backend/agent.py

The main Agentic RAG engine.

Responsible for:

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
backend/ingest.py

Responsible for processing documents and generating the FAISS vector store.

Documents
    ↓
Load
    ↓
Split
    ↓
Embed
    ↓
FAISS
backend/main.py

Backend application/API entry point.

It connects the Agentic RAG engine with the frontend.

backend/test_agent.py

Contains tests for validating the backend Agentic RAG functionality.

frontend/

Contains the React + Vite user interface.

The frontend communicates with the backend API and displays the generated answers and execution information.

🧠 Why Agentic RAG?

Traditional RAG assumes:

Query
 ↓
Retrieve
 ↓
Generate

But retrieval can fail due to:

Ambiguous questions
Different terminology
Poor query formulation
Similar but irrelevant documents
Large knowledge bases
Missing keywords

Agentic RAG adds a reasoning layer:

Query
 ↓
Decide
 ↓
Retrieve
 ↓
Evaluate
 ↓
Recover if necessary
 ↓
Generate

This makes the retrieval workflow more adaptive.

📊 Traditional RAG vs Agentic RAG
Feature	Traditional RAG	This Project
Query Routing	❌	✅
Vector Search	✅	✅
Relevance Checking	Usually ❌	✅
Query Reformulation	Usually ❌	✅
Retry Mechanism	Limited	✅
Context Grounding	✅	✅
Execution Trace	Usually ❌	✅
Adaptive Retrieval	Limited	✅
🛡️ Reliability

The system includes several mechanisms to improve reliability:

Relevance Validation

Retrieved documents are evaluated before final generation.

Query Reformulation

Poor retrieval results trigger a new search query.

Bounded Retries

The system cannot enter an infinite retrieval loop.

Context Grounding

Final responses are generated using retrieved context.

Empty Retrieval Handling

The application handles cases where no documents are retrieved.

Execution Tracing

Every major stage can be monitored and debugged.

⚠️ Current Limitations

This project is an Agentic RAG foundation and can be improved further.

LLM-Based Relevance Evaluation

The relevance checker depends on an LLM and may occasionally make incorrect judgments.

Retrieval Ranking

The current system relies primarily on vector similarity retrieval.

Source Citations

Document names, page numbers, and exact source references can be added to final answers.

Conversation Memory

Multi-turn conversational memory can be added for more advanced use cases.

Production Observability

The existing trace mechanism can be integrated with dedicated monitoring and evaluation platforms.

🚀 Future Improvements
 Source/document citations
 Page-level references
 Retrieval similarity thresholds
 Hybrid keyword + vector search
 Cross-encoder reranking
 Conversation memory
 Multi-document reasoning
 Streaming responses
 Structured LLM outputs
 Pydantic validation
 Hallucination detection
 RAG evaluation
 Automated evaluation datasets
 Docker deployment
 Authentication
 Rate limiting
 CI/CD
 Production monitoring
🔒 Security & Privacy

Private and generated data should never be committed to the repository.

The following are excluded using .gitignore:

.env
.venv/
__pycache__/
backend/pdfs/
backend/uploads/
backend/vector_store/
frontend/node_modules/
*.pdf
Never upload:
API keys
Passwords
Private documents
User-uploaded files
Personal information
Production credentials

If an API key is accidentally pushed to GitHub, immediately revoke/rotate the key.

📈 Production Architecture

The project can be extended into a production AI system:

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
🎓 Key Learning Outcomes

This project provided practical experience with:

Retrieval-Augmented Generation
Agentic AI
Large Language Models
LLM orchestration
Semantic search
Vector databases
Embeddings
Prompt engineering
Retrieval routing
Relevance grading
Query reformulation
Retry strategies
Context grounding
Python backend development
React frontend development
API integration
AI application architecture
Execution tracing
💡 Project Goal

The goal of this project was to move beyond simply calling an LLM API and build a more structured AI system where the LLM participates in decision-making and retrieval control.

Instead of:

LLM + Vector Database

the system follows:

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

This architecture provides a foundation for building more adaptive and reliable AI applications.

👨‍💻 Author
Ranjith

AI / GenAI Engineer | Python Developer | Computer Science Student

Areas of Interest
Generative AI
Agentic AI
Retrieval-Augmented Generation
LLM Applications
AI Automation
Machine Learning
Python
AI Engineering
⭐ If You Find This Project Useful

If you find this project useful or interesting:

⭐ Star the repository

🍴 Fork the project

💬 Share your feedback

🤝 Connect with me