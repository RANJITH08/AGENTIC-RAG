"""
Quick command-line test for AgenticRAG — run this before building the API,
so you can see the reasoning trace directly in the terminal.

Usage:
    python test_agent.py "What is the refund policy?"
"""

import sys
from agent import AgenticRAG

def main():
    if len(sys.argv) < 2:
        print('Usage: python test_agent.py "your question here"')
        sys.exit(1)

    query = sys.argv[1]

    print("Loading agent (this loads the embedding model + FAISS index)...")
    rag = AgenticRAG()

    print(f"\nQuery: {query}\n")
    result = rag.run(query)

    print("----- TRACE -----")
    for event in result["trace"]:
        print(f"[{event['step']}] {event['detail']}")

    print("\n----- FINAL ANSWER -----")
    print(result["answer"])

if __name__ == "__main__":
    main()