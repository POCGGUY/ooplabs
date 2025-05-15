import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from model.todolistModel import TodoList

async def get_all(session: AsyncSession):
    result = await session.execute(
        select(TodoList).where(TodoList.deleted_at.is_(None))
    )
    return result.scalars().all()

async def get(session: AsyncSession, todolist_id: int):
    result = await session.execute(
        select(TodoList)
        .where(TodoList.id == todolist_id, TodoList.deleted_at.is_(None))
    )
    return result.scalar_one_or_none()

async def create(session: AsyncSession, data):
    todo = TodoList(**data.dict())
    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    return todo

async def update(session: AsyncSession, todolist_id: int, data):
    todo = await get(session, todolist_id)
    if not todo:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(todo, key, value)
    await session.commit()
    await session.refresh(todo)
    return todo

async def delete(session: AsyncSession, todolist_id: int):
    todo = await get(session, todolist_id)
    if not todo:
        return None
    todo.deleted_at = datetime.datetime.utcnow()
    await session.commit()
    return todo

def calculate_progress(todolist: TodoList) -> float:
    if todolist.total_count == 0:
        return 0.0
    return (todolist.completed_count / todolist.total_count) * 100
