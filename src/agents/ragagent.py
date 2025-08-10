from typing import Dict, List, TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
import PyPDF2
from dotenv import load_dotenv

load_dotenv()
# state management - query , documents and result string exchanged between nodes/agents 
class GraphState(TypedDict):
    query: str
    documents: List[Document]
    generation: str
# RAG Agents that will spilt documents into text chunks to create embedding and 
# store in vectorstore for efficient and accurate retrieval (retrieve agent)
# This will also send these embeddings ,query ,context to LLM GPT transformer model to 
# generate accurate answers for the bot (Generate agent)
class RAGAgent:
    def __init__(self):
        print("🚀 [bold blue]Initializing RAG System...[/bold blue]")
        
        

        self.llm = ChatOpenAI(
            model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.vectorstore = None
        self.graph = None
        
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.demo_docs = self.load_nutrition_pdfs()
        self.setup_vectorstore(self.demo_docs)
        
        # self.embeddings = model.encode(self.demo_docs)
        # print(self.embeddings)
        
        self.create_graph()

        
    def setup_vectorstore(self, documents: List[str]):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", " ", ""])
        
        docs = []
        for i, doc in enumerate(documents):
            splits = text_splitter.split_text(doc)
            docs.extend([Document(page_content=split, metadata={"source": f"doc_{i}"}) for split in splits])
        print(docs)
        self.vectorstore = FAISS.from_documents(docs, self.embeddings)  
        
        return "Vector store ready"
    
    def retrieve(self, state: GraphState) -> Dict:
        print(" RETRIEVING DOCUMENTS...")
        query = state["query"]
        
        if not self.vectorstore:
            return {"documents": []}
            
        documents = self.vectorstore.similarity_search(query, k=3)
        print(f"Found {len(documents)} relevant documents")
        return {"documents": documents}
    
    def generate(self, state: GraphState) -> Dict:
        print(" GENERATING RESPONSE...")
        query = state["query"]
        documents = state["documents"]
        
        docs_txt = "\n\n".join([d.page_content for d in documents])
        
        prompt = f"""You are a helpful AI assistant. Answer the question based on the provided context.

Context: {docs_txt}

Question: {query}

Answer (be concise and accurate):"""
        
        response = self.llm.invoke(prompt)
        print(" Response generated")
        return {"generation": response.content}
    
    # creates a graph of nodes or agents with edges connecting them to create a directed acyclic graph
    def create_graph(self):
        workflow = StateGraph(GraphState)
        
        workflow.add_node("retrieve", self.retrieve)
        workflow.add_node("generate", self.generate)
        
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)
        
        return workflow.compile()
    def query(self, question: str) -> Dict:
        console.print(f"\n💭 [bold]Processing: {question}[/bold]")
        console.print("─" * 50)
        
        result = self.graph.invoke({
            "query": question,
            "documents": [],
            "generation": "",
            "metadata": {}
        })
        
        return result
    def load_nutrition_pdfs(self):
        """Load nutrition PDF documents into the knowledge base"""
        pdf_dir = "data/PDFs"
        documents = []
        
        for filename in os.listdir(pdf_dir):
            if filename.endswith(".pdf"):
                filepath = os.path.join(pdf_dir, filename)
                
                with open(filepath, "rb") as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                    
                    documents.append(text)
        
        return documents
