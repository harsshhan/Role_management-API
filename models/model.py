from pydantic import BaseModel
from typing import Optional


class OldData(BaseModel):
    email_id:Optional[str]=None
    role:Optional[str]=None

class NewData(BaseModel):
    user_id:str
    name:str
    email_id:str
    role:str

class Task(BaseModel):
    task_id:str
    task:str
    deadline: str
    assigned_to:str
    status:str

class EditTask(BaseModel):
    task:Optional[str]=None
    deadline: Optional[str]=None
    assigned_to:Optional[str]=None
    status:Optional[str]=None