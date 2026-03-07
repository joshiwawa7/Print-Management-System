from pydantic import BaseModel
from datetime import datetime


class OrderCreate(BaseModel):
    customer_name: str
    pages: int
    print_type: str


class OrderRead(BaseModel):
    id: int
    customer_name: str
    pages: int
    print_type: str
    unit_price: float
    total_price: float
    created_at: datetime

    class Config:
        orm_mode = True
