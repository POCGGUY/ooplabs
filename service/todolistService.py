from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from model.todolistModel import TodoList
from schemas.todolistRoute import TodoListCreate, TodoListUpdate

async def get_all(session: AsyncSession):
    result = await session.execute(select(TodoList))
    return result.scalars().all()

async def get(session: AsyncSession, todolist_id: int):
    return await session.get(TodoList, todolist_id)

async def create(session: AsyncSession, data: TodoListCreate):
    todo = TodoList(**data.dict())
    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    return todo

async def update(session: AsyncSession, todolist_id: int, data: TodoListUpdate):
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
    await session.delete(todo)
    await session.commit()
    return todo
