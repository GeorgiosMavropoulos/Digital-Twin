# Digital Twin

A personal website with an AI chatbot that answers questions about me, my background, projects, and interests. The bot retrieves information from a vector database of my own materials, so its answers stay grounded in what I've actually provided.

## Features

- **Conversational Q&A** about my experience, skills, projects, and education
- **Retrieval-augmented answers** via ChromaDB, so responses draw on my own documents
- **Persistent memory** that remembers prior conversations across sessions
- **Gradio web interface** for chatting directly in the browser
- **CI/CD Pipeline using automated tests running on Github.

- # Tech Stack

- **Python 3.10+**
- **ChromaDB**: vector store for embeddings of my profile and documents, plus conversation memory
- **Gradio**: web UI for the chatbot
- - **LLM provider**: Gemini
- - **Tests: pytest
 

## Project Structure
digital-twin/
├── app.py               # Gradio interface and entry point
├── llm/                 # Chat logic: prompt assembly, LLM calls
  ├── llm_instance   
├── chroma/              # Chroma Vector Database
  ├── vector_db.py       # Conversation memory backed by ChromaDB
├── ingest.py            # Loads source documents into ChromaDB
├── config.py            # Settings and environment variable loading
├── data/
│   ├── profile/         # Bio, CV, project descriptions (Markdown/text)
│   └── faq/             # Common questions and preferred answers
├── requirements.txt
├── .env.example
└── README.md
