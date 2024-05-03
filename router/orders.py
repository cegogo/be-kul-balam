from fastapi import APIRouter, Depends
from schemas import Order, UserBase
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_orders
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/orders',
    tags=['orders']
)

#Create order by user
@router.post('/')
def create_order(db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    order = db_orders.create_empty_order(db, current_user.id)
    return order

#Get an order
@router.get('/{id}', response_model=Order)
def get_order(id: int, db: Session = Depends (get_db)):
    return db_orders.get_order(db, id)

#Delete an order
@router.delete('/{id}')
def delete_order(id:int, db:Session = Depends(get_db)):
    return db_orders.delete_order(db, id)