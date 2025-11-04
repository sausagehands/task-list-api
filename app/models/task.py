from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime
from typing import Optional
#do i need to import foreignkey?

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    
    # need to revisit this-- i imagine i have to map it, like id-- has to register time when is_complete = true
    completed_at: Mapped[Optional[datetime]]
    
    #converts task instance into dictionary
    def to_dict(self):
        return{
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None 
        }
    
    #creates a task from a dictionary
    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data.get('title'),
            description=task_data.get('description'),
            completed_at=task_data.get('completed_at')
            )
        
