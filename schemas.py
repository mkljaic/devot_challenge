from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    username: str
    email: str
    password: str
    balance: float = 1000.0

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    balance: float
    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str

class CategoryOut(CategoryBase):
    id: int
    class Config:
        orm_mode = True


class ExpenseBase(BaseModel):
    description: str
    amount: float
    date: date
    category_id: int
    user_id: int


class ExpenseOut(ExpenseBase):
    id: int
    category: CategoryOut
    class Config:
        orm_mode = True

class StatsOut(BaseModel):
    spent: float
    class Config:
        orm_mode = True