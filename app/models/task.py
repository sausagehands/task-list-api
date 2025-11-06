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
        task_as_dict = {}
        task_as_dict["id"]= self.id
        task_as_dict["title"]= self.title
        task_as_dict["description"]= self.description
        task_as_dict["is_complete"]= self.completed_at is not None
        
        if self.completed_at:
            task_as_dict["completed_at"]= self.completed_at.isoformat() if self.completed_at else None 
        
        return task_as_dict
    
    #creates a task from a dictionary
    @classmethod
    def from_dict(cls, task_data):
        new_task =  cls(
            title=task_data['title'],
            description=task_data['description'],
            completed_at=task_data.get('completed_at')
            )
        
        return new_task
        
