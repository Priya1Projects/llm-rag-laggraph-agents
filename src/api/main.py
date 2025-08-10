from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sys
import os

sys.path.append('/workspaces/llm-rag-laggraph-agents/')
print(sys.path) 
from src.agents.ragagent import RAGAgent

app = FastAPI(title="🤖 RAG LangGraph API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_agent = RAGAgent()
graph = rag_agent.create_graph()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]



@app.get("/")
async def root():
    return {
        "message": "🤖 RAG LangGraph API is running!",
        "docs": "/docs",
        "status": "healthy"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "agents": "ready"}

@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    try:
        print(f"📝 Processing query: {request.question}")
        
        # Run the LangGraph workflow
        result = graph.invoke({"query": request.question})
        
        sources = [doc.metadata.get("source", "demo_doc") for doc in result.get("documents", [])]
        
        return QueryResponse(
            answer=result.get("generation", "Sorry, I couldn't generate an answer."),
            sources=list(set(sources))  # Remove duplicates
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)