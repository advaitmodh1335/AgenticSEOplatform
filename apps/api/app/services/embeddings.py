from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts: list[str]):
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.astype("float32")


def embed_query(text: str):
    embedding = model.encode([text], convert_to_numpy=True)
    return embedding.astype("float32")