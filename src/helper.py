import os

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

chroma_path = "P:\Generative AI projects\Research-Paper-Summarizer\chroma_db"


def load_data():
    loader = DirectoryLoader(
        "P:\Generative AI projects\Research-Paper-Summarizer\data",
        glob="*.pdf",
        loader_cls=PyPDFLoader,
    )
    return loader.load()


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)


def load_embeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """load huggingface embeddings"""
    return HuggingFaceEmbeddings(model_name=model_name)


def load_db(embeddings):
    """load vector database. Requires embeddings"""

    if os.path.exists(chroma_path):
        print("🔄 Loading existing Chroma index...")
        return Chroma(persist_directory=chroma_path, embedding_function=embeddings)

    else:
        raise FileNotFoundError(
            f"❌ Chroma index not found at {chroma_path}. Please build it first."
        )


def build_db(embeddings, text_chunks):
    print("✨ Creating new Chroma index...")
    return Chroma.from_documents(
        documents=text_chunks, embedding=embeddings, persist_directory=chroma_path
    )


def load_llm(model="llama-3.1-8b-instant"):
    """Load llama model"""
    return ChatGroq(
        groq_api_key=GROQ_API_KEY, model=model, temperature=0.3, max_tokens=1000
    )


__all__ = [
    "load_data",
    "split_documents",
    "load_embeddings",
    "load_db",
    "build_db",
    "load_llm",
]
