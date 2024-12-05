from sqlalchemy import Column, Integer, String, Float
from database import Base

class Item(Base):
   __tablename__ = "products"
   
   id = Column(Integer, primary_key=True)
   name = Column(String, index=True)
   amount = Column(Integer, index=True)
   price = Column(Float, index=True)
   