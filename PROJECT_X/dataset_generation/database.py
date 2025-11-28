from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from datetime import datetime

DATABASE_URL = "sqlite+aiosqlite:///./dataset.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    answer_1 = Column(Text, nullable=False)
    answer_2 = Column(Text, nullable=False)
    answer_3 = Column(Text, nullable=False)
    answer_4 = Column(Text, nullable=False)
    answer_5 = Column(Text, nullable=False)
    correct_answer_index = Column(Integer, nullable=False)  # 1-5
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    source_text = Column(Text, nullable=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
