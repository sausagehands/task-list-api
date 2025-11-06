from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
#from datetime import datetime
#from typing import Optional

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]

    def to_dict(self):
        goal_as_dict = {}
        goal_as_dict["id"]= self.id
        goal_as_dict["title"]= self.title
                
        return goal_as_dict
    
    #creates a task from a dictionary
    @classmethod
    def from_dict(cls, task_data):
        new_task =  cls(title=task_data['title'])
        
        return new_task
