import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

from models import Category


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

@pytest.fixture(scope = "function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope = "function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    return client


def test_create_category(client):

    category_data = {
        "name": "Books"
    }

    response = client.post("/categories/", json = category_data)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Books"

def test_get_all_categories(client, db_session):

    category = Category(name = "Books")
    db_session.add(category)
    db_session.commit()


    response = client.get("/categories/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_category_by_id(client, db_session):
    test_category = Category(name = "Books")
    db_session.add(test_category)
    db_session.commit()
    db_session.refresh(test_category)

    response = client.get(f"/categories/{test_category.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == test_category.id
    assert data["name"] == "Books"


def test_delete_category(client, db_session):

    test_category = Category(name = "Books")
    db_session.add(test_category)
    db_session.commit()
    db_session.refresh(test_category)

    response = client.delete(f"/categories/{test_category.id}")
    assert response.status_code == 200