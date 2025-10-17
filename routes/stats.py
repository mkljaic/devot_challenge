from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy import and_
from dateutil.relativedelta import relativedelta

import models, schemas

router = APIRouter(
    prefix="/stats",
    tags=["Stats"]
)

@router.get("/summary/all_time/{uid}", response_model = schemas.StatsOut)
def get_summary_all(uid: int, db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).filter(models.Expense.user_id == uid).all()

    spent = 0

    for exp in expenses:
        spent += abs(exp.amount)


    return {"spent": spent}

@router.get("/summary/monthly/{uid}", response_model = schemas.StatsOut)
def get_summary_monthly(uid: int, db: Session = Depends(get_db)):

    month = datetime.now().date() - timedelta(days = 30)
    expenses = (db.query(models.Expense).filter(and_(models.Expense.user_id == uid, models.Expense.date >= month)).all())

    if not expenses:
        raise HTTPException(status_code = 404, detail = "No expenses found for the last 30 days")

    spent = 0
    for exp in expenses:
        spent += abs(exp.amount)


    return {"spent": spent}

@router.get("/summary/quarterly/{uid}", response_model = schemas.StatsOut)
def get_summary_quarterly(uid: int, db: Session = Depends(get_db)):

    quarter = datetime.now().date() - relativedelta(months = 3)
    expenses = (db.query(models.Expense).filter(and_(models.Expense.user_id == uid, models.Expense.date >= quarter)).all())

    if not expenses:
        raise HTTPException(status_code = 404, detail = "No expenses found for the last quarter")

    spent = 0
    for exp in expenses:
        spent += abs(exp.amount)


    return {"spent": spent}

@router.get("/summary/yearly/{uid}", response_model = schemas.StatsOut)
def get_summary_yearly(uid: int, db: Session = Depends(get_db)):

    year = datetime.now().date() - relativedelta(year = 1)
    expenses = (db.query(models.Expense).filter(and_(models.Expense.user_id == uid, models.Expense.date >= year)).all())

    if not expenses:
        raise HTTPException(status_code = 404, detail = "No expenses found for the last year")

    spent = 0
    for exp in expenses:
        spent += abs(exp.amount)


    return {"spent": spent}