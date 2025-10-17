import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import timedelta, date

from main import app
from database import Base, get_db

from models import User, Category, Expense


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


def create_test_data(db_session, amount, time):
    test_user = User(
        username = "Ghanima",
        email = "Ghanima@mail.com",
        password = "Ghanima",
        balance = 1000
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    test_category = Category(name = "Books")
    db_session.add(test_category)
    db_session.commit()
    db_session.refresh(test_category)

    test_expense = Expense(
        description = "Dune",
        amount = amount,
        date = date.today() - timedelta(days = time),
        user_id = test_user.id,
        category_id = test_category.id
    )
    db_session.add(test_expense)
    db_session.commit()
    db_session.refresh(test_expense)

    return test_user, test_category, test_expense

def test_summary_all_(client, db_session):
    user, _, _ = create_test_data(db_session, amount = 150, time = 10)

    response = client.get(f"/stats/summary/all_time/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["spent"] == 150

def test_summary_quarterly(client, db_session):
    user, _, _ = create_test_data(db_session, amount = 300, time = 60)  

    response = client.get(f"/stats/summary/quarterly/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["spent"] == 300

def test_summary_yearly(client, db_session):
    user, _, _ = create_test_data(db_session, amount = 400, time = 200)  

    response = client.get(f"/stats/summary/yearly/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["spent"] == 400

def test_summary_monthly_no_expenses(client, db_session):
    user, _, _ = create_test_data(db_session, amount=100, time = 40)  

    response = client.get(f"/stats/summary/monthly/{user.id}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No expenses found for the last 30 days"