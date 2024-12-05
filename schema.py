from pydantic import BaseModel

class ItemBase(BaseModel):
   title: str
   amount: int
   price: float
   
class ItemCreate(ItemBase):
   pass

class ItemResponse(ItemBase):
   id: int
   class Config:
      from_attribute = True
