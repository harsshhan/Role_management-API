from pydantic import BaseModel
from typing import Optional

class oldData(BaseModel):
    email:Optional[str]=None
    role:Optional[str]=None

class newData(BaseModel):
    user_id:str
    name:str
    email:str
    role:str

