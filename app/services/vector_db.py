import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DB_DIR = "./chroma_db"

embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")

def process_and_store_pdf(file_path: str) -> int:
    loader = PyPDFLoader(file_path)
    pages =  loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 100,
        separators = ["\n\n", "\n", ".", ""]
    )
    chunks = text_splitter.split_documents(pages)

    Chroma.from_documents(
        documents = chunks,
        embedding = embeddings, 
        persist_directory = DB_DIR
    )

    return len(chunks)

def query_resume_context(query: str) -> str:
    if not os.path.exists(DB_DIR):
        return "No resume context found. Please upload and process the resume first."
    
    vector_store = Chroma(persist_directory = DB_DIR, embedding_function = embeddings)
    retriever = vector_store.as_retriever(search_kwargs = {"k" : 3})

    docs = retriever.invoke(query)

    return "\n\n".join([doc.page_content for doc in docs])
    

