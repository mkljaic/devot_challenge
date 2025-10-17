from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from typing import Optional
from sqlalchemy import asc, desc

import models, schemas

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

@router.post("/", response_model = schemas.ExpenseOut)
def create_expense(expense: schemas.ExpenseBase, db: Session = Depends(get_db)):

    user = db.query(models.User).filter_by(id = expense.user_id).first()

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found!")
    
    if expense.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive!")

    
    if user.balance < expense.amount:
        raise HTTPException(status_code = 400, detail = "Insufficient funds!")
    
    user.balance -= expense.amount

    db_expense = models.Expense(description = expense.description,
                                amount = expense.amount,
                                date = expense.date,
                                user_id = expense.user_id,
                                category_id = expense.category_id
                                )
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense

@router.get("/all", response_model = list[schemas.ExpenseOut])
def get_all(db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).all()

    return expenses

@router.get("/", response_model = list[schemas.ExpenseOut])
def get_expense(
    expense_id: Optional[int] = None,
    user_id: Optional[int] = None,
    category_id: Optional[int] = None,
    amount: Optional[float] = None,
    minmax: Optional[str] = None,
    db: Session = Depends(get_db)):

    expense = db.query(models.Expense)

    if expense_id:
        expense = expense.filter(models.Expense.id == expense_id)

    if user_id:
        expense = expense.filter(models.Expense.user_id == user_id)
    if category_id:
        expense = expense.filter(models.Expense.category_id == category_id)
    if amount:
        expense = expense.filter(models.Expense.amount <= amount)
    if minmax:
        if minmax.lower() == "min":
            expense = expense.order_by(asc(models.Expense.amount))
        elif minmax.lower() == "max":
            expense = expense.order_by(desc(models.Expense.amount))
        else:
            raise HTTPException(status_code = 400, detail = "Invalid option")

    results = expense.all()
    if not results:
        raise HTTPException(status_code = 404, detail = "Expense not found!")

    return results

@router.put("/{expense_id}", response_model = schemas.ExpenseOut)
def update_expense(expense_id: int, updated_expense: schemas.ExpenseBase, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter_by(id = expense_id).first()

    if not expense:
        raise HTTPException(status_code = 404, detail = "Expense not found!")
    
    expense.description = updated_expense.description
    expense.amount = updated_expense.amount

    if updated_expense.category_id is not None and updated_expense.category_id != expense.category_id:
        expense.category_id = updated_expense.category_id

    db.commit()
    db.refresh(expense)

    return expense

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter_by(id = expense_id).first()
    
    if not expense:
        raise HTTPException(status_code = 404, detail = "Expense not found!")
    
    user = db.query(models.User).filter_by(id = expense.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    
    user.balance += expense.amount
    
    db.delete(expense)
    db.commit()

    return {"detail": "Expense deleted succesfully!"}