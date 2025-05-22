from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from model.todolistModel import TodoList
from model.itemModel import Item
from domain.todolist_aggregate import TodoListAggregate


class TodoListRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def load(self, todolist_id: int) -> TodoListAggregate:
        db_obj = await self.session.get(TodoList, todolist_id)
        if not db_obj:
            return None
        return TodoListAggregate(id=db_obj.id, name=db_obj.name, deleted_at=db_obj.deleted_at)

    async def save(self, aggregate: TodoListAggregate):
        db_obj = await self.session.get(TodoList, aggregate.id)
        if not db_obj:
            raise ValueError("TodoList not found")

        db_obj.name = aggregate.name
        db_obj.deleted_at = aggregate.deleted_at

        result = await self.session.execute(
            select(
                func.count().label("total"),
                func.count().filter(Item.is_done).label("completed")
            ).where(Item.todolist_id == db_obj.id, Item.deleted_at.is_(None))
        )
        total, completed = result.one()

        db_obj.total_count = total
        db_obj.completed_count = completed

        self.session.add(db_obj)
        await self.session.commit()
