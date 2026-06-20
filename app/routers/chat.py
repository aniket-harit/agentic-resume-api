from fastapi import APIRouter, HTTPException
from app.schemas import QueryRequest, QueryResponse
from app.services.agent import get_agent_executor

router = APIRouter()
agent_executor = get_agent_executor()

@router.post("/query", response_model=QueryResponse)
def query_agent(payload: QueryRequest):
    try:
        inputs = {"messages": [("user", payload.query)]}
        result = agent_executor.invoke(inputs)
        
        messages = result.get("messages", [])
        if not messages:
            raise HTTPException(status_code=500, detail="No messages returned from agent executor.")
            
        # The last message contains the final generated answer
        answer = messages[-1].content
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")
