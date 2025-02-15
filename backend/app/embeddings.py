from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def encode_text(text: str) -> list:
    return model.encode(text).tolist()
