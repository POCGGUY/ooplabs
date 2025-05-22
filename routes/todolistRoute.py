from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import SessionLocal
from schemas.todolistRoute import TodoListCreate, TodoListRead, TodoListUpdate
from service import todolistService as service

router = APIRouter(prefix="/todolists", tags=["TodoLists"])

not_found_msg = "TodoList не найден"
deleted_msg = "TodoList удалён"

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/", response_model=TodoListRead)
async def create_todolist(data: TodoListCreate, db: AsyncSession = Depends(get_db)):
    todo = await service.create(db, data)
    return TodoListRead(
        id=todo.id,
        name=todo.name,
        progress=0.0
    )

@router.patch("/{todolist_id}", response_model=TodoListRead)
async def update_todolist(todolist_id: int, data: TodoListUpdate, db: AsyncSession = Depends(get_db)):
    todo = await service.update(db, todolist_id, data)
    if not todo:
        raise HTTPException(404, not_found_msg)
    progress = (todo.completed_count / todo.total_count * 100) if todo.total_count else 0.0
    return TodoListRead(id=todo.id, name=todo.name, progress=progress)

@router.delete("/{todolist_id}")
async def delete_todolist(todolist_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await service.delete(db, todolist_id)
    if not deleted:
        raise HTTPException(404, not_found_msg)
    return {"detail": deleted_msg}
