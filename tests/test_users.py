import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

from models import User
from utils import utils

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
    with TestClient(app) as c:
        yield c 


def test_create_user(client):
    user_data = {
        "username": "Jessica",
        "email": "Jessica@mail.com",
        "password": "Jessica123",
        "balance": 1000
    }

    response = client.post("/users/", json = user_data)
    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "Jessica"
    assert data["email"] == "Jessica@mail.com"
    assert data["balance"] == 1000
    assert "id" in data  

def test_get_user_by_email(client, db_session):

    hashed_password = utils.hash_password("Paul123").decode("utf-8")

    test_user = User(
        username = "Paul", 
        email = "Paul@mail.com", 
        password = hashed_password, 
        balance = 500
        )
    
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    response = client.post(f"/users/login/email/{test_user.email}/Paul123")
    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "Paul"
    assert data["email"] == "Paul@mail.com"
    assert data["balance"] == 500


def test_get_user_by_username(client, db_session):

    hashed_password = utils.hash_password("Alia123").decode("utf-8")

    test_user = User(
        username = "Alia", 
        email = "Alia@mail.com", 
        password = hashed_password, 
        balance = 500
        )
    
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    response = client.post(f"/users/login/username/{test_user.username}/Alia123")
    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "Alia"
    assert data["email"] == "Alia@mail.com"
    assert data["balance"] == 500


def test_delete_expense(client, db_session):

    user_data = {
        "username": "Chani",
        "email": "Chani@mail.com",
        "password": "Chani",
        "balance": 1000
    }

    response = client.post("/users/", json = user_data)
    assert response.status_code == 200
    created_user = response.json()

    response = client.delete(f"/users/{created_user['id']}")
    assert response.status_code == 200

    data = response.json()
    assert data["detail"] == "User deleted succesfully!"

