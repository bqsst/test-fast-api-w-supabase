from sqlalchemy.orm import Session
from sqlalchemy import Boolean, case
from schema import ItemCreate
from model import Item
from fastapi import HTTPException

def create_product(db: Session, item: ItemCreate):
   db_product = Item(**item.model_dump())
   db.add(db_product)
   db.commit()
   db.refresh(db_product)
   return db_product

def get_products(db: Session):
   db_product = db.query(Item).all()
   if db_product is None:
      raise HTTPException(status_code=404, detail="Product not found")
   return db_product

def get_product_by_id(db: Session, id: int):
   db_product = db.query(Item).filter(Item.id == id).first()
   if db_product is None:
      raise HTTPException(status_code=404, detail="Product not found")
   return db_product
