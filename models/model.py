from pydantic import BaseModel
from typing import Optional


class OldData(BaseModel):
    email:Optional[str]=None
    role:Optional[str]=None

class NewData(BaseModel):
    user_id:str
    name:str
    email:str
    role:str

class Task(BaseModel):
    task_id:str
    task_name:str
    deadline: str
    assigned_to:str

class EditTask(BaseModel):
    task_name:Optional[str]=None
    deadline: Optional[str]=None
    assigned_to:Optional[str]=None