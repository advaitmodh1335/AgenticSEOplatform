import faiss
import numpy as np
import os
import pickle

INDEX_PATH = "faiss_index.bin"
METADATA_PATH = "faiss_metadata.pkl"


def create_index(dimension: int):
    return faiss.IndexFlatL2(dimension)


def save_index(index, metadata):
    faiss.write_index(index, INDEX_PATH)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)


def load_index():
    if not os.path.exists(INDEX_PATH) or not os.path.exists(METADATA_PATH):
        return None, []

    index = faiss.read_index(INDEX_PATH)
    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata


def search_index(index, query_vector, metadata, top_k=5):
    distances, indices = index.search(query_vector, top_k)

    results = []
    for idx in indices[0]:
        if idx != -1 and idx < len(metadata):
            results.append(metadata[idx])

    return results