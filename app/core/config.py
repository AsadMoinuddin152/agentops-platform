import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("MODEL", "qwen2.5:1.5b")

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "project_memory")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

PROJECT_PATH = os.getenv("PROJECT_PATH", "./app")
CHUNK_LINES = int(os.getenv("CHUNK_LINES", "150"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "40"))

RAG_N_RESULTS = int(os.getenv("RAG_N_RESULTS", "30"))

METRICS_FILE = os.getenv("METRICS_FILE", "logs/metrics.jsonl")
LOG_FILE = os.getenv("LOG_FILE", "logs/agent_logs.jsonl")
MEMORY_LIMIT = int(os.getenv("MEMORY_LIMIT", "5"))