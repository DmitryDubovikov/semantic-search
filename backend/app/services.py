import uuid
from .schemas import NewsItem
from .embeddings import encode_text
from .qdrant_service import add_document, search_document


def add_news_service(item: NewsItem):
    vector = encode_text(item.content)
    news_id = str(uuid.uuid4())
    add_document(
        collection_name="news", doc_id=news_id, vector=vector, payload={"title": item.title, "content": item.content}
    )
    return {"message": "News added", "id": news_id}


def search_news_service(query: str):
    query_vector = encode_text(query)
    results = search_document(collection_name="news", query_vector=query_vector, limit=5)
    return [{"title": r.payload["title"], "content": r.payload["content"]} for r in results]
