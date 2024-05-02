from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session 
from db.models import DbProduct
from schemas import ProductBase

def insert_product (db: Session, request: ProductBase, user_id):
    new_product = DbProduct(
        product_name = request.product_name, 
        description = request.description,
        price = request.price,
        quantity = request.quantity,
        seller_id = user_id,
        published = request.published
    )
    db.add(new_product) 
    db.commit()
    db.refresh(new_product)
    return new_product

def get_all_products (db: Session, nameFilter: str) -> List[DbProduct]:
    productsQuery = db.query(DbProduct)
    if(nameFilter != ''):
        productsQuery = productsQuery.filter(DbProduct.product_name.icontains(nameFilter))
    
    return productsQuery.all()

def count_all_products(db: Session) -> int: 
    return db.query(DbProduct).count()

def get_product_by_id(db: Session, id: int):
    product = db.query(DbProduct).filter(DbProduct.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id '{id}' not found."
        )
    return product

def update_product(db: Session, id: int, product_name: str, description: str, price: float, quantity: int):
    product = db.query(DbProduct).filter(DbProduct.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id '{id}' not found."
        )

    product.product_name = product_name
    product.description = description
    product.price = price
    product.quantity = quantity
    db.commit()
    return product

def delete_product(db: Session, id: int):
    product = db.query(DbProduct).filter(DbProduct.id == id).first()
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product with id '{id}' not found")

    db.delete(product)
    db.commit()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)