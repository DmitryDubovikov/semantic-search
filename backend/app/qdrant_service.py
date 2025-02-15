from qdrant_client import QdrantClient, models

client = QdrantClient(host="qdrant", port=6333)


def create_collection(collection_name: str, vector_size: int):
    existing_collections = client.get_collections().collections
    if collection_name not in [col.name for col in existing_collections]:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        )


def add_document(collection_name: str, doc_id: str, vector: list, payload: dict):
    client.upsert(
        collection_name=collection_name, points=[models.PointStruct(id=doc_id, vector=vector, payload=payload)]
    )


def search_document(collection_name: str, query_vector: list, limit: int = 5, score_threshold: float = 0.5):
    results = client.search(collection_name=collection_name, query_vector=query_vector, limit=limit)
    return [result for result in results if result.score >= score_threshold]
