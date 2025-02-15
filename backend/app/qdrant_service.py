import uuid

from qdrant_client import QdrantClient, models

from .embeddings import encode_text
from .fixtures import generate_news_fixtures

client = QdrantClient(host="qdrant", port=6333)


def create_collection(collection_name: str, vector_size: int, num_items: int = 10):
    existing_collections = client.get_collections().collections

    if collection_name not in [col.name for col in existing_collections]:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        )

        news_items = generate_news_fixtures(num_items=num_items)

        for item in news_items:
            doc_id = str(uuid.uuid4())
            vector = encode_text(item.content)
            payload = {"title": item.title, "content": item.content}

            add_document(collection_name=collection_name, doc_id=doc_id, vector=vector, payload=payload)


def add_document(collection_name: str, doc_id: str, vector: list, payload: dict):
    client.upsert(
        collection_name=collection_name, points=[models.PointStruct(id=doc_id, vector=vector, payload=payload)]
    )


def search_document(collection_name: str, query_vector: list, limit: int = 5, score_threshold: float = 0.5):
    results = client.search(collection_name=collection_name, query_vector=query_vector, limit=limit)
    return [result for result in results if result.score >= score_threshold]
