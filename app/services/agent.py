import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from app.services.vector_db import query_resume_context

load_dotenv()

@tool
def search_resume(query: str) -> str:
    """Search the candidate's resume context for information matching the query."""
    return query_resume_context(query)

system_message = (
    "You are an AI assistant representing the candidate. "
    "Answer questions about the candidate using only the provided tool. "
    "If the query is not about the candidate, or if the information is not present "
    "in the candidate's resume/details, state that the information is not available "
    "and stop querying. Do not make multiple repetitive tool calls if the tool does not "
    "provide new information."
)

def get_agent_executor():
    llm = ChatGroq(model_name = "llama-3.1-8b-instant", temperature = 0)

    return create_react_agent(model = llm, tools = [search_resume], prompt = system_message)