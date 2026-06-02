from sentence_transformers import SentenceTransformer
from app.core.config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)


def embed_text(text: str):
    return model.encode(text).tolist()