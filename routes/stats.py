from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from typing import Optional
from sqlalchemy import asc, desc

import models, schemas

router = APIRouter(
    prefix="/stats",
    tags=["Stats"]
)

@router.get("/summary/{uid}", response_model = schemas.StatsOut)
def get_summary(uid: int, db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).filter(models.Expense.user_id == uid).all()

    spent = 0

    for exp in expenses:
        spent += abs(exp.amount)


    return {"spent": spent}