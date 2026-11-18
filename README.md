# Digital Twin

A personal website with an AI chatbot that answers questions about me, my background, projects, and interests. The bot retrieves information from a vector database of my own materials, so its answers stay grounded in what I've actually provided.

## Features

- **Conversational Q&A** about my experience, skills, projects, and education
- **Retrieval-augmented answers** via ChromaDB, so responses draw on my own documents
- **Persistent memory** that remembers prior conversations across sessions
- **Next.JS web interface** for chatting directly in the browser
- **CI/CD Pipeline using automated tests running on Github (To-Do).

- # Tech Stack

- **Python 3.10+**
- **ChromaDB**: vector store for embeddings of my profile and documents, plus conversation memory
- **Next.JS**: web UI for the chatbot
- **LLM provider**: Gemini
- **Tests: pytest
 
```
digital-twin/
├── backend/
│   ├── __init__.py
│   ├── inference.py          # FastAPI app entry point (uvicorn backend.inference:app)
│   ├── api/
│   │   ├── __init__.py
│   │   └── router.py         # /chat endpoint (StreamingResponse)
│   ├── llm/
│   │   ├── __init__.py
│   │   └── llm_client.py     # LLMService: Gemini chat, tool loop, streaming
│   ├── vector_db/
│   │   ├── __init__.py
│   │   └── vec_db.py         # ChromaDb: PDF ingestion and retrieval
│   ├── tools/
│   │   ├── __init__.py
│   │   └── tool.py           # Tools class with callable functions
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── prompt_templates.py
│   └── models/
│       ├── __init__.py
│       └── py_models.py      # ChatRequest, ChatResponse, Message
├── frontend/
│   ├── app/
│   │   └── page.tsx          # Next.js chat UI with streamed replies
│   ├── public/
│   │   └── me.jpg            # Profile photo
│   ├── .env.local            # NEXT_PUBLIC_API_URL (not committed)
│   └── ...                   # package.json, next.config, etc.
├── Profile.pdf               # LinkedIn profile summary used for RAG
├── requirements.txt
├── .env.example
├── .gitignore                # include .env, chroma_db/, frontend/.env.local
└── README.md
```
