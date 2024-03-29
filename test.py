from pymongo import MongoClient
from config.database import db
from models.model import EditTask

client=MongoClient("mongodb+srv://harshan:harshanmathi@role-management.a68cz.mongodb.net/?retryWrites=true&w=majority&appName=role-management")
edit_task=EditTask()
for field_name, field_value in dict(edit_task).items():
    if field_value is None:
        del field_name
        
        
