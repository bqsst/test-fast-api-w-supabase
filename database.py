from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL environment variable is not set")

if SUPABASE_URL.startswith('https://'):
    db_url = SUPABASE_URL.replace('https://', '')
    host_part = db_url.split('/')[0]
    path_part = '/'.join(db_url.split('/')[1:])
    DATABASE_URL = f"postgresql+asyncpg://postgres:{os.getenv('SUPABASE_DB_PASSWORD')}@{host_part}:5432/{path_part}"
else:
    DATABASE_URL = SUPABASE_URL.replace("postgres://", "postgresql+asyncpg://")

engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    echo=True
)

SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
