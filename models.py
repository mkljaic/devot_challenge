from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import date
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique = True, index=True, nullable =False)
    email = Column(String, unique = True, index=True, nullable = False)
    password = Column(String, nullable = False)
    balance = Column(Float, default = 1000.0)

    expenses = relationship("Expense", back_populates="user")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, unique = True, nullable = False)

    expenses = relationship("Expense", back_populates="category")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key = True, index = True)
    description = Column(String, nullable = False)
    amount = Column(Float, nullable = False)
    date = Column(Date, default = date)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates = "expenses")

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates = "expenses")
