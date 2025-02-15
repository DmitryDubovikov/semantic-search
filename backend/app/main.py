from fastapi import FastAPI
from .qdrant_service import create_collection
from .services import add_news_service, search_news_service
from .schemas import NewsItem

app = FastAPI()

create_collection("news", vector_size=384)


@app.post("/add_news/")
def add_news(item: NewsItem):
    return add_news_service(item)


@app.get("/search/")
def search_news(query: str):
    return search_news_service(query)
