"""Class to process files using chromadb vector database"""
import os
from typing import List
import chromadb
from chromadb.errors import ChromaError
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChromaDb:

    def store_pdf_in_chroma(
        self,
        pdf_path: str,
        collection_name: str = "digital_twin_profile",
        persist_directory: str = "./chroma_db"
    ) -> None:
        """Extracts text from a PDF, chunks it, and stores it in ChromaDB."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found at path: {pdf_path}")

        # 1. Extract text from PDF
        try:
            reader = PdfReader(pdf_path)
            full_text = ""
            for page_num, page in enumerate(reader.pages):
                extracted = page.extract_text()
                if extracted:
                    full_text += f"\n--- Page {page_num + 1} ---\n{extracted}"
        except PdfReadError as e:
            raise ValueError(f"Failed to parse corrupted or invalid PDF: {e}") from e
        except OSError as e:
            raise IOError(f"OS error while reading the PDF file: {e}") from e

        # Raise an exception if no readable text is found inside the PDF
        if not full_text.strip():
            raise ValueError("No readable text found in the PDF. It may be a scanned image.")

        # 2. Split text into overlapping chunks for better retrieval
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        chunks = text_splitter.split_text(full_text)

        # Call the method to initialize the db and store the chunks
        ChromaDb.initialize_chroma_db_and_store_chunks(
            persist_directory, pdf_path, chunks, collection_name
        )

    def retrieve_from_chroma(
        self,
        question: str,
        collection_name: str = "digital_twin_profile",
        persist_directory: str = "./chroma_db",
        n_results: int = 3
    ) -> str:
        """Queries ChromaDB for the most relevant profile chunks matching the question."""
        if not question or not question.strip():
            raise ValueError("Query question cannot be empty.")

        if not os.path.exists(persist_directory):
            raise FileNotFoundError(f"ChromaDB directory not found at: {persist_directory}")

        try:
            client = chromadb.PersistentClient(path=persist_directory)
            # get_collection raises ValueError if the collection does not exist
            collection = client.get_collection(name=collection_name)

            # Query the db to get the results
            results = collection.query(
                query_texts=[question],
                n_results=n_results
            )
        except ChromaError as e:
            raise RuntimeError(f"ChromaDB error during retrieval: {e}") from e
        except ValueError as e:
            raise LookupError(f"Collection '{collection_name}' does not exist or query failed: {e}") from e

        documents: List[List[str]] = results.get("documents", [])
        if not documents or not documents[0]:
            return "There are no documents or relevant information matching your query."

        # Combine retrieved chunks into a single context string for your prompt
        return "\n\n".join(documents[0])

    @staticmethod
    def initialize_chroma_db_and_store_chunks(
        persist_directory: str,
        pdf_path: str,
        chunks: List[str],
        collection_name: str
    ) -> None:
        """Initialize chroma db and store the chunks."""
        try:
            client = chromadb.PersistentClient(path=persist_directory)
            collection = client.get_or_create_collection(name=collection_name)

            ids = [f"{os.path.basename(pdf_path)}_chunk_{i}" for i in range(len(chunks))]
            metadatas = [{"source": pdf_path, "chunk_index": i} for i in range(len(chunks))]

            # upsert updates existing IDs or inserts new ones safely
            collection.upsert(
                documents=chunks,
                ids=ids,
                metadatas=metadatas
            )
        except ChromaError as e:
            raise RuntimeError(f"ChromaDB error during storage: {e}") from e
        except ValueError as e:
            raise ValueError(f"Invalid data format passed to ChromaDB: {e}") from e
