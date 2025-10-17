from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from database import get_db

import models, schemas

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("/", response_model = schemas.CategoryOut)
def create_category(category: schemas.CategoryBase, db: Session = Depends(get_db)):
    
    ex_cat = db.query(models.Category).filter_by(name = category.name).first()

    if ex_cat:
        raise HTTPException(status_code=400, detail="Category already exists")

    db_category = models.Category(name = category.name)

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category

@router.get("/", response_model = list[schemas.CategoryOut])
def get_all(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()

    return categories

@router.get("/{category_id}", response_model = schemas.CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter_by(id = category_id).first()

    if not category:
        raise HTTPException(status_code = 404, detail = "Category not found!")

    return category

@router.put("/{category_id}", response_model = schemas.CategoryOut)
def update_category(category_id: int, updated_category: schemas.CategoryBase, db: Session = Depends(get_db)):

    category = db.query(models.Category).filter_by(id = category_id).first()

    if not category:
        raise HTTPException(status_code = 404, detail = "Category not found!")

    category.name = updated_category.name
    db.commit()
    db.refresh(category)

    return category


@router.delete("/{category_id}")
def delete(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter_by(id = category_id).first()

    if not category:
        raise HTTPException(status_code = 404, detail = "Category not found!")
    
    db.delete(category)
    db.commit()
    
    return {"detail": "Category deleted succesfully!"}