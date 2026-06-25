from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, document

app = FastAPI(
    title="Agentic RAG Resume Assistant",
    description="A FastAPI app using LangGraph and Chroma DB to query resumes.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(document.router, prefix="/api/v1", tags=["Document"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

import os
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def read_root():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Interactive UI Template not found!</h1>", status_code=404)


@app.get("/health", response_class = HTMLResponse)
def health_check():
    return HTMLResponse(content = """
    <h1>Health: Healthy</h1>
    """)