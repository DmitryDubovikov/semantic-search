from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
import uuid
from qdrant_client import QdrantClient, models

app = FastAPI()

client = QdrantClient(host="qdrant", port=6333)


def create_collection(collection_name: str, vector_size: int):
    # Check if the collection already exists
    existing_collections = client.get_collections().collections
    if collection_name not in [col.name for col in existing_collections]:
        # If the collection doesn't exist, create it
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        )


create_collection("news", vector_size=384)


# Модель для векторизации. Можно вынести в embeddings.py
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# Определение модели запроса. Можно вынести в schemas.py
class NewsItem(BaseModel):
    title: str
    content: str


@app.post("/add_news/")
def add_news(item: NewsItem):
    vector = model.encode(item.content).tolist()
    news_id = str(uuid.uuid4())

    add_document(
        collection_name="news", doc_id=news_id, vector=vector, payload={"title": item.title, "content": item.content}
    )

    return {"message": "News added", "id": news_id}


@app.get("/search/")
def search_news(query: str):
    query_vector = model.encode(query).tolist()

    results = search_document(collection_name="news", query_vector=query_vector, limit=5)

    return [{"title": r.payload["title"], "content": r.payload["content"]} for r in results]


def add_document(collection_name: str, doc_id: str, vector: list, payload: dict):
    client.upsert(
        collection_name=collection_name, points=[models.PointStruct(id=doc_id, vector=vector, payload=payload)]
    )


def search_document(collection_name: str, query_vector: list, limit: int = 5, score_threshold: float = 0.5):
    results = client.search(collection_name=collection_name, query_vector=query_vector, limit=limit)

    filtered_results = [result for result in results if result.score >= score_threshold]

    return filtered_results
