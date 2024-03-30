from pymongo import MongoClient
from config.database import db

collection=db['users']

task=db.task.find_one({'task_id':'t11'})
task_assigned_to_role=db.users.find_one({'user_id':task['assigned_to']})['role']
print(task_assigned_to_role)