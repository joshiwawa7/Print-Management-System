from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base

# create DB tables on startup (simple for this scaffold)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Print Management System (PMS)")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/orders", response_model=schemas.OrderRead)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    try:
        db_order = crud.create_order(db, order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_order


@app.get("/orders/{order_id}", response_model=schemas.OrderRead)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@app.get("/orders", response_model=list[schemas.OrderRead])
def list_orders(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    return crud.get_recent_orders(db, limit=limit)
