import streamlit as st
import requests
import json
import time

st.set_page_config(
    page_title=" RAG LangGraph Demo",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 2rem;
    color: #1f77b4;
}
.demo-tag {
    background: linear-gradient(90deg, #1f77b4, #ff7f0e);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: bold;
    display: inline-block;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header"> RAG LangGraph AI Agents</h1>', unsafe_allow_html=True)
st.markdown('<div class="demo-tag"> Live Cloud Demo - LLM + RAG + LangGraph</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header(" Configuration")
    api_url = st.text_input("API URL", value="http://localhost:8000", help="Change to your deployed API URL")
    
    # Test API connection
    if st.button("🔍 Test API Connection"):
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ API Connected!")
            else:
                st.error("❌ API Error")
        except:
            st.error("❌ Cannot connect to API")
    
    st.markdown("---")
    
    st.header("📚 Knowledge Base")
    st.info("Demo includes knowledge about:\n- LangGraph\n- RAG systems\n- Vector databases\n- AI agents")
    
    st.markdown("---")
    
    st.header("🔗 Links")
    st.markdown("[GitHub Repo](https://github.com/Priya1Projects/llm-rag-laggraph-agents)")
    st.markdown("[LangGraph Docs](https://langchain-ai.github.io/langgraph/)")

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Chat with RAG Agent")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Hello! I'm a RAG-powered NutriAssistAI agent built with LangGraph. Ask me anything about your daily nutrition questions"
        })

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about the nutrition..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner(" LangGraph agents working..."):
            try:
                start_time = time.time()
                response = requests.post(
                    f"{api_url}/query",
                    json={"question": prompt},
                    timeout=30
                )
                end_time = time.time()
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data["sources"]
                    
                    st.markdown(answer)
                    
                    # Show metadata
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.caption(f"⚡ Response time: {end_time - start_time:.2f}s")
                    with col_b:
                        st.caption(f"📄 Sources: {len(sources)}")
                    
                    # Add to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer
                    })
                else:
                    st.error(f"❌ API Error: {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error("⏰ Request timeout - try again")
            except Exception as e:
                st.error(f"❌ Connection error: {e}")

with col2:
    st.header("🎯 Try These Questions")
    
    sample_questions = [
        "How much protein do I need for muscle building?",
        "What supplements should vegans take?",
        "Best pre-workout nutrition for endurance sports?",
        "How to break a weight loss plateau?",
        "What foods are high in iron for plant-based diets?"
    ]
    
    for i, question in enumerate(sample_questions):
        if st.button(f"💡 {question}", key=f"q_{i}"):
            st.session_state.messages.append({"role": "user", "content": question})
            st.rerun()
    
    st.markdown("---")
    
    st.header("📊 System Info")
    st.code("""
🔧 Tech Stack:
- LangGraph: Agent orchestration
- FastAPI: Backend API
- Streamlit: Frontend UI
- FAISS: Vector storage
- Sentence Transformers: Embeddings
    """)
    
    if st.button("🔄 Clear Chat"):
        st.session_state.messages = []
        st.rerun()