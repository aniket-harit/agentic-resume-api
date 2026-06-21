# Agentic Resume API

A robust backend service powering an agentic RAG (Retrieval-Augmented Generation) assistant for resume parsing and querying.

## Architecture
* **Framework:** FastAPI
* **Vector Database:** ChromaDB
* **AI Orchestration:** LangGraph
* **Frontend:** Native HTML/JS served directly via FastAPI endpoints

## Quick Start

1. Ensure your virtual environment is active.
2. Run the local development server:
```bash
   uvicorn app.main:app --reload