from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import SessionLocal
from schemas.todolistRoute import *
from service import todolistService as service

router = APIRouter(prefix="/todolists", tags=["TodoLists"])

todolist_not_found_msg = "TodoList не найден"
todolist_is_deleted_msg = "TodoList удалён"
async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[TodoListRead])
async def list_todolists(db: AsyncSession = Depends(get_db)):
    return await service.get_all(db)

@router.post("/", response_model=TodoListRead)
async def create_todolist(data: TodoListCreate, db: AsyncSession = Depends(get_db)):
    return await service.create(db, data)

@router.get("/{todolist_id}", response_model=TodoListRead)
async def get_todolist(todolist_id: int, db: AsyncSession = Depends(get_db)):
    todo = await service.get(db, todolist_id)
    if not todo:
        raise HTTPException(status_code=404, detail=todolist_not_found_msg)
    return todo

@router.patch("/{todolist_id}", response_model=TodoListRead)
async def update_todolist(todolist_id: int, data: TodoListUpdate, db: AsyncSession = Depends(get_db)):
    todo = await service.update(db, todolist_id, data)
    if not todo:
        raise HTTPException(status_code=404, detail=todolist_not_found_msg)
    return todo

@router.delete("/{todolist_id}")
async def delete_todolist(todolist_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await service.delete(db, todolist_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=todolist_not_found_msg)
    return {"detail": todolist_is_deleted_msg}
