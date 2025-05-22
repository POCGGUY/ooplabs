from sqlalchemy.ext.asyncio import AsyncSession
from repository.todolist_repository import TodoListRepository
from schemas.todolistRoute import TodoListCreate, TodoListUpdate

async def create(session: AsyncSession, data: TodoListCreate):
    from model.todolistModel import TodoList
    todo = TodoList(**data.dict())
    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    return todo

async def update(session: AsyncSession, todolist_id: int, data: TodoListUpdate):
    repo = TodoListRepository(session)
    agg = await repo.load(todolist_id)
    if not agg:
        return None

    if data.name is not None:
        agg.rename(data.name)

    await repo.save(agg)
    return await session.get(type(agg), agg.id)

async def delete(session: AsyncSession, todolist_id: int):
    repo = TodoListRepository(session)
    agg = await repo.load(todolist_id)
    if not agg:
        return None

    agg.mark_deleted()
    await repo.save(agg)
    return agg
