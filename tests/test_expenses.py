import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

from models import User, Category


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


def test_create_expense(client, db_session):
    test_user = User(
        username = "Duncan", 
        email = "Duncan@mail.com", 
        password = "Duncan", 
        balance = 1000
        )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    test_category = Category(name = "Books")
    db_session.add(test_category)
    db_session.commit()
    db_session.refresh(test_category)

    expense_data = {
        "description": "Dune",
        "amount": 50,
        "date": "2025-10-17",
        "user_id": test_user.id,
        "category_id": 1
    }

    response = client.post("/expenses/", json = expense_data)
    assert response.status_code == 200

    data = response.json()
    assert data["description"] == "Dune"
    assert data["amount"] == 50

def test_get_all_expenses(client, db_session):

    test_user = User(
        username = "Leto",
        email = "Leto@mail.com",
        password = "Leto",
        balance = 1000
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    test_category = Category(name = "Books")
    db_session.add(test_category)
    db_session.commit()
    db_session.refresh(test_category)

    expense_data = {
        "description": "Dune",
        "amount": 50,
        "date": "2025-10-17",
        "user_id": test_user.id,
        "category_id": test_category.id
    }

    response = client.post("/expenses/", json = expense_data)
    assert response.status_code == 200

    response = client.get("/expenses/all")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  
    assert data[0]["description"] == "Dune"
    assert data[0]["amount"] == 50


def test_delete_expense(client, db_session):

    test_user = User(
        username = "Gurney",
        email = "Gurney@mail.com",
        password = "Gurney",
        balance = 1000
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    test_category = Category(name = "Books")
    db_session.add(test_category)
    db_session.commit()
    db_session.refresh(test_category)

    expense_data = {
        "description": "Dune",
        "amount": 50,
        "date": "2025-10-17",
        "user_id": test_user.id,
        "category_id": test_category.id
    }

    response = client.post("/expenses/", json = expense_data)
    assert response.status_code == 200
    created_expense = response.json()

    response = client.delete(f"/expenses/{created_expense['id']}")
    assert response.status_code == 200

    data = response.json()
    assert data["detail"] == "Expense deleted succesfully!"

