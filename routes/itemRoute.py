from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import SessionLocal
from schemas.itemRoute import ItemCreate, ItemRead, ItemUpdate
from service import itemService as service

router = APIRouter(prefix="/items", tags=["Items"])

item_not_found_msg = "Item не найден"
item_is_deleted_msg = "Item удалён"

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[ItemRead])
async def list_items(db: AsyncSession = Depends(get_db)):
    return await service.get_all(db)

@router.post("/", response_model=ItemRead)
async def create_item(data: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await service.create(db, data)

@router.get("/{item_id}", response_model=ItemRead)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await service.get(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail=item_not_found_msg)
    return item

@router.patch("/{item_id}", response_model=ItemRead)
async def update_item(item_id: int, data: ItemUpdate, db: AsyncSession = Depends(get_db)):
    item = await service.update(db, item_id, data)
    if not item:
        raise HTTPException(status_code=404, detail=item_not_found_msg)
    return item

@router.delete("/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await service.delete(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=item_not_found_msg)
    return {"detail": item_is_deleted_msg}
