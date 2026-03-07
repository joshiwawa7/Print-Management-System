from sqlalchemy.orm import Session
from . import models, schemas

# Prices according to PRD.txt (Philippine pesos)
PRICES = {
    "bw": 2.0,
    "color": 5.0,
    "photo": 20.0,
}


def create_order(db: Session, order_in: schemas.OrderCreate):
    pt = order_in.print_type.lower()
    if pt not in PRICES:
        raise ValueError(f"invalid print_type: {order_in.print_type}")
    unit = PRICES[pt]
    total = unit * order_in.pages
    db_order = models.Order(
        customer_name=order_in.customer_name,
        pages=order_in.pages,
        print_type=pt,
        unit_price=unit,
        total_price=total,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_recent_orders(db: Session, limit: int = 10):
    return db.query(models.Order).order_by(models.Order.created_at.desc()).limit(limit).all()
