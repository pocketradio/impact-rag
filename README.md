# Impact RAG

Impact RAG is a repo-aware code analysis tool that uses retrieval-augmented generation (RAG) to answer questions directly from a codebase. Instead of guessing or relying on general knowledge, it indexes a repository using abstract syntax trees, pulls in the most relevant code snippets, and generates answers that stay grounded in the actual code.

---

## To note:

The system currently only supports Python repositories with AST-based symbol extraction and will be extended with tree-sitter to support additional languages in the future.

![Status](https://img.shields.io/badge/status-WIP-orange)

---

## Tech Stack

Backend:

- Python
- FastAPI
- LangChain
- Groq
- ChromaDB

Frontend:

- next.js
- tailwind
