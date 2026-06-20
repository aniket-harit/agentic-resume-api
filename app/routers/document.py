import os
import shutil
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas import UploadResponse
from app.services.vector_db import process_and_store_pdf

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    tmp_path = None
    try:
        # Create a temporary file to save the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        # Process the PDF and load chunks to vector DB
        num_chunks = process_and_store_pdf(tmp_path)
        
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
            
        return UploadResponse(message=f"Successfully processed resume. Created {num_chunks} chunks.")
    except Exception as e:
        # Cleanup if anything fails
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
