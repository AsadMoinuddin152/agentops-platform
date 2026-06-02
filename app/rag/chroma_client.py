# pyrefly: ignore [missing-import]
import chromadb
from app.core.config import CHROMA_PATH, CHROMA_COLLECTION

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name=CHROMA_COLLECTION
)