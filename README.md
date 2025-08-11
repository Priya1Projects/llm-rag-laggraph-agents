
# MULTI AGENT RAG SYSTEM

This is simple RAG System to demonstrate how to build a simple Chat Assistant with Langraph
This assistant is a nutritional assistant that will answer your daily nutrition based questions.

# Architecture 

User query -> Retrival agent ( retrieves from PDFs knowledge base) -> Generate Agent (takes embeddings and query and generates relevant response)

# Tech Stack

Python (Langchain, Langraph, openAI, sentence transformers)
FASTAPi
Streamlit
Docker
Github codespaces for development
HuggingFace Spaces for deployment 

## License

[MIT](https://choosealicense.com/licenses/mit/)

---
sdk: docker
app_port: 7860 

---
