# semantic-search

## Vector Search with Qdrant, FastAPI, and Fake News Generation

This project demonstrates how to set up a FastAPI backend that interacts with Qdrant for semantic vector search. The backend generates fake news data, stores it in Qdrant, and provides endpoints for adding news and searching based on vector queries.
Project Structure

    Docker Compose: Defines the qdrant and backend services.
    FastAPI: Used for the backend API that handles adding and searching news.
    Qdrant: A vector search engine that stores the news articles in a vectorized format.

## Setup

```shell
docker compose up -d --build
```

## API Endpoints

1. Swagger UI: http://localhost:8000/docs
2. Add News: http://localhost:8000/add_news/
3. Search News: http://localhost:8000/search/
4. Qdrant Dashboard: http://localhost:6333/dashboard