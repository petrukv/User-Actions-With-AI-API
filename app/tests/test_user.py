import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app


client = TestClient(app)


def test_create_post():
    post_data = {
        "title": "Test Post",
        "content": "This is a test post"
    }
    response = client.post("/user/posts", json=post_data, headers={"Authorization": "Bearer "})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == post_data["title"]
    assert data["content"] == post_data["content"]

def test_get_post():
    response = client.get("/user/post/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"


def test_comments_daily_breakdown():
    response = client.get("/user/comments-daily-breakdown?date_from=2024-10-01&date_to=2024-10-31", 
                          headers={"Authorization": f"Bearer "})

    assert response.status_code == 200

    expected_data = [
        {
            "date": "2024-10-21",
            "total_comments": 4,
            "blocked_comments": 0
        }
    ]
    assert response.json() == expected_data