from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from model.itemModel import Item
from schemas.itemRoute import ItemCreate, ItemUpdate

async def get_all(session: AsyncSession):
    result = await session.execute(select(Item))
    return result.scalars().all()

async def get(session: AsyncSession, item_id: int):
    return await session.get(Item, item_id)

async def create(session: AsyncSession, data: ItemCreate):
    item = Item(**data.dict())
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item

async def update(session: AsyncSession, item_id: int, data: ItemUpdate):
    item = await get(session, item_id)
    if not item:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)
    await session.commit()
    await session.refresh(item)
    return item

async def delete(session: AsyncSession, item_id: int):
    item = await get(session, item_id)
    if not item:
        return None
    await session.delete(item)
    await session.commit()
    return item
