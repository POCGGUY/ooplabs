import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from model.itemModel import Item
from model.todolistModel import TodoList

async def update_todolist_counts(session: AsyncSession, todolist_id: int):
    result = await session.execute(
        select(Item)
        .where(Item.todolist_id == todolist_id, Item.deleted_at.is_(None))
    )
    items = result.scalars().all()

    completed = sum(1 for item in items if item.is_done)
    total = len(items)

    todo = await session.get(TodoList, todolist_id)
    if todo:
        todo.completed_count = completed
        todo.total_count = total
        await session.commit()

async def get_all(session: AsyncSession):
    result = await session.execute(
        select(Item).where(Item.deleted_at.is_(None))
    )
    return result.scalars().all()

async def get(session: AsyncSession, item_id: int):
    result = await session.execute(
        select(Item).where(Item.id == item_id, Item.deleted_at.is_(None))
    )
    return result.scalar_one_or_none()

async def create(session: AsyncSession, data):
    item = Item(**data.dict())
    session.add(item)
    await session.commit()
    await session.refresh(item)
    await update_todolist_counts(session, item.todolist_id)
    return item

async def update(session: AsyncSession, item_id: int, data):
    item = await get(session, item_id)
    if not item:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)
    await session.commit()
    await session.refresh(item)
    await update_todolist_counts(session, item.todolist_id)
    return item

async def delete(session: AsyncSession, item_id: int):
    item = await get(session, item_id)
    if not item:
        return None
    item.deleted_at = datetime.datetime.utcnow()
    await session.commit()
    await update_todolist_counts(session, item.todolist_id)
    return item
