import pytest
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from src.components.base.domain.dto.base import BaseDTO
from src.components.base.infra.repositories.postgres import BasePostgresRepository

Base = declarative_base()

class DummyUserModel(Base):
    __tablename__ = "dummy_users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)
    role = Column(String)
    deleted_at = Column(DateTime, nullable=True)

class DummyUserDTO(BaseDTO):
    id: int
    name: str
    status: str
    role: str
    deleted_at: Optional[datetime] = None

class DummyUserRepository(BasePostgresRepository[DummyUserDTO]):
    _model_type = DummyUserModel
    _dto_type = DummyUserDTO

@pytest.fixture
async def async_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with session_maker() as session:
        yield session
    
    await engine.dispose()

@pytest.mark.asyncio
async def test_update_returning_all_fields(async_session: AsyncSession):
    repo = DummyUserRepository(async_session)
    
    # Шаг 0: Создаем исходные данные
    created_user = await repo.create(name="Павел", status="new", role="admin")
    await async_session.commit()
    
    print("\n\n--- Исходный пользователь ---")
    print(f"ID: {created_user.id} | Name: '{created_user.name}' | Status: '{created_user.status}' | Role: '{created_user.role}'")

    # Шаг 1 и 2: Update в транзакции (без коммита)
    updated_user = await repo.update(created_user, status="active")
    
    print("\n--- 1. Возвращается ли ВЕСЬ документ при RETURNING? ---")
    print(f"Получили DTO: ID: {updated_user.id} | Name: '{updated_user.name}' | Status: '{updated_user.status}' | Role: '{updated_user.role}'")
    
    assert updated_user.status == "active"
    assert updated_user.name == "Павел"
    assert updated_user.role == "admin"
    print("✅ ДА: Вернулись не только обновленный 'status', но и старые 'name' и 'role', которые мы не трогали.")
    
    print("\n--- 2. Доступны ли измененные данные ДО коммита? ---")
    print(f"Текущий статус в DTO: {updated_user.status}")
    assert updated_user.status == "active"
    print("✅ ДА: Вызов update() сразу возвращает актуальные данные, хотя session.commit() мы еще не вызывали.")
    
    # Шаг 3: Коммит
    print("\n--- Вызываем session.commit() ---")
    await async_session.commit()

    # Шаг 4: Проверка после коммита
    fetched_user = await repo.get(created_user.id)
    
    print("\n--- 3. Сохранились ли данные ПОСЛЕ коммита? ---")
    print(f"Достали из БД: ID: {fetched_user.id} | Name: '{fetched_user.name}' | Status: '{fetched_user.status}' | Role: '{fetched_user.role}'")
    
    assert fetched_user.status == "active"
    assert fetched_user.name == "Павел"
    assert fetched_user.role == "admin"
    print("✅ ДА: В БД сохранился обновленный 'status' вместе с остальными полями.\n")
