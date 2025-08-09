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

# Demo knowledge base
DEMO_DOCS = [
    """LangGraph is a library for building stateful, multi-actor applications with LLMs, used by thousands of developers in production. 
    It extends LangChain Expression Language with the ability to coordinate multiple chains (or actors) across multiple steps of computation 
    in a cyclic manner. It is inspired by Pregel and Apache Beam.""",
    
    """Retrieval-Augmented Generation (RAG) is a technique that enhances large language models by providing them with access to external 
    knowledge sources. Instead of relying solely on training data, RAG systems can retrieve relevant information from databases, 
    documents, or APIs to generate more accurate and up-to-date responses.""",
    
    """Vector databases are specialized database systems designed to store, index, and search high-dimensional vectors efficiently. 
    They are essential for AI applications like semantic search, recommendation systems, and RAG implementations. Popular vector 
    databases include Pinecone, Weaviate, Chroma, and FAISS.""",
    
    """AI agents are autonomous systems that can perceive their environment, make decisions, and take actions to achieve specific goals. 
    Modern AI agents often use large language models as their reasoning engine, combined with tools and memory systems to perform 
    complex tasks like research, analysis, and problem-solving.""",
    
    """Multi-agent systems involve multiple AI agents working together, either cooperatively or competitively, to solve complex problems. 
    Each agent can have specialized roles and capabilities, allowing for more sophisticated and scalable AI solutions."""
]




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