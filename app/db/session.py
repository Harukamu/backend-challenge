from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+asyncpg://mesa:mesa@localhost:5433/mesa_challenge"

# Motor async
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Sesión async moderna
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base para modelos
Base = declarative_base()
