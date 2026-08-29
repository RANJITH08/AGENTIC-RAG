"""
Agentic RAG core.

Flow:
  user query -> agent decides: answer directly / retrieve
  if retrieve -> relevance check on chunks
      relevant     -> generate answer
      not relevant -> reformulate query -> retrieve again (max N retries)
  every step is logged into a `trace` list so the API can stream it to the UI.
"""

import os
import time
from dataclasses import dataclass, field
from typing import Literal

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

MAX_RETRIES = 2
GROQ_MODEL = "openai/gpt-oss-120b"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "./vector_store")


@dataclass
class TraceEvent:
    step: Literal[
        "agent_decision", "retrieve", "relevance_check",
        "reformulate", "answer_directly", "final_answer", "error"
    ]
    detail: str
    meta: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self):
        return {
            "step": self.step,
            "detail": self.detail,
            "meta": self.meta,
            "timestamp": self.timestamp,
        }


class AgenticRAG:
    def __init__(self):
        self.llm = ChatGroq(model=GROQ_MODEL, temperature=0)
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.vector_store = self._load_vector_store()
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})

    def reload_vector_store(self):
        self.vector_store = self._load_vector_store()
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})

    def _load_vector_store(self) -> FAISS:
        if not os.path.exists(FAISS_INDEX_PATH):
            raise FileNotFoundError(
                f"No FAISS index found at {FAISS_INDEX_PATH}. Run ingest.py first."
            )
        return FAISS.load_local(
            FAISS_INDEX_PATH, self.embeddings, allow_dangerous_deserialization=True
        )

    def run(self, query: str) -> dict:
        trace: list[TraceEvent] = []
        current_query = query

        needs_retrieval = self._needs_retrieval(query)
        trace.append(TraceEvent(
            step="agent_decision",
            detail="Answer directly" if not needs_retrieval else "Retrieve from documents",
            meta={"needs_retrieval": needs_retrieval},
        ))

        if not needs_retrieval:
            answer = self._answer_directly(query)
            trace.append(TraceEvent(step="answer_directly", detail=answer))
            return {"answer": answer, "trace": [t.to_dict() for t in trace]}

        chunks = []
        for attempt in range(MAX_RETRIES + 1):
            chunks = self.retriever.invoke(current_query)
            trace.append(TraceEvent(
                step="retrieve",
                detail=f"Retrieved {len(chunks)} chunk(s) for: \"{current_query}\"",
                meta={"query": current_query, "num_chunks": len(chunks)},
            ))

            is_relevant, reason = self._check_relevance(query, chunks)
            trace.append(TraceEvent(
                step="relevance_check",
                detail=reason,
                meta={"relevant": is_relevant, "attempt": attempt},
            ))

            if is_relevant or attempt == MAX_RETRIES:
                break

            current_query = self._reformulate_query(query, current_query, reason)
            trace.append(TraceEvent(
                step="reformulate",
                detail=f"Reformulated to: \"{current_query}\"",
                meta={"new_query": current_query},
            ))

        answer = self._generate_answer(query, chunks)
        trace.append(TraceEvent(step="final_answer", detail=answer))

        return {"answer": answer, "trace": [t.to_dict() for t in trace]}

    def _needs_retrieval(self, query: str) -> bool:
        prompt = (
        "You are deciding whether to search a document knowledge base before answering.\n"
        "Reply DIRECT only if the query is clearly small talk, a greeting, or a "
        "question about the assistant itself (e.g. 'hi', 'how are you', 'what can you do').\n"
        "For anything else — including general knowledge, definitions, or topic "
        "questions that the documents might cover — reply RETRIEVE, since the "
        "documents may contain the specific or more accurate answer.\n"
        f'Query: "{query}"\n'
        'Reply with exactly one word: "RETRIEVE" or "DIRECT".'
        )
        result = self.llm.invoke(prompt).content.strip().upper()
        return "DIRECT" not in result
    
    def _answer_directly(self, query: str) -> str:
        prompt = f"Answer this briefly and naturally: {query}"
        return self.llm.invoke(prompt).content.strip()

    def _check_relevance(self, original_query: str, chunks) -> tuple[bool, str]:
        if not chunks:
            return False, "No chunks retrieved."

        context = "\n---\n".join(c.page_content[:400] for c in chunks)
        prompt = (
            f'Question: "{original_query}"\n\n'
            f"Retrieved passages:\n{context}\n\n"
            "Do these passages contain enough information to answer the question? "
            'Reply with "YES: <one line reason>" or "NO: <one line reason>".'
        )
        result = self.llm.invoke(prompt).content.strip()
        is_relevant = result.upper().startswith("YES")
        reason = result.split(":", 1)[-1].strip() if ":" in result else result
        return is_relevant, reason

    def _reformulate_query(self, original_query: str, last_query: str, reason: str) -> str:
        prompt = (
            f'Original question: "{original_query}"\n'
            f'Previous search query: "{last_query}"\n'
            f"Why it failed: {reason}\n\n"
            "Rewrite the search query with different phrasing or more specific "
            "keywords likely to match the source documents. "
            "Reply with only the new query, nothing else."
        )
        return self.llm.invoke(prompt).content.strip().strip('"')

    def _generate_answer(self, query: str, chunks) -> str:
        if not chunks:
            return (
            "I couldn't find relevant information in the documents to answer "
            "that confidently."
        )
        context = "\n---\n".join(c.page_content for c in chunks)
        prompt = (
        "Answer the question thoroughly and in detail, using only the context below. "
        "Explain the reasoning, include relevant specifics, examples, or sub-points "
        "found in the context, and organize the answer clearly (use short paragraphs "
        "or bullet points if helpful). If the context is insufficient for a full answer, "
        "say what's missing.\n\n"
        f"Context:\n{context}\n\nQuestion: {query}\n\nDetailed Answer:"
        )
        return self.llm.invoke(prompt).content.strip()