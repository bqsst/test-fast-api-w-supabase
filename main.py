from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, engine, Base
from schema import ItemCreate, ItemResponse
from controller import create_product, get_products, get_product_by_id
from dotenv import load_dotenv
import os

load_dotenv()

# สร้างตารางแบบ async
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await create_tables()

origins = [
    os.getenv("FRONTEND_URL")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/products", response_model=ItemResponse)
async def create_product_route(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await create_product(db, item)

@app.get("/products", response_model=List[ItemResponse])
async def get_products_route(db: AsyncSession = Depends(get_db)):
    return await get_products(db)

@app.get("/products/{id}", response_model=ItemResponse)
async def get_product_by_id_route(id: int, db: AsyncSession = Depends(get_db)):
    return await get_product_by_id(db, id)
