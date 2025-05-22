from datetime import datetime
from typing import Optional


class TodoListAggregate:
    def __init__(self, id: int, name: str, deleted_at: Optional[datetime] = None):
        self.id = id
        self.name = name
        self.deleted_at = deleted_at

    def rename(self, new_name: str):
        self.name = new_name

    def mark_deleted(self):
        self.deleted_at = datetime.utcnow()
