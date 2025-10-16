from fastapi import FastAPI
from database import Base, engine
from routes import categories, expenses, users, stats 

app = FastAPI(title="Home Budget API")

Base.metadata.create_all(bind=engine)

app.include_router(categories.router)
app.include_router(expenses.router)
app.include_router(users.router)
app.include_router(stats.router)

@app.get("/")
def root():
    return {"message": "Home Budget API radi!"}
