from pymongo import MongoClient
from fastapi import FastAPI
from config.database import db
from models.model import newData,oldData

app=FastAPI()


@app.post('/admin/newuser/{admin_uid}')
def adduser(admin_uid,data:newData):
    collection=db.users
    for i in collection.find({'user_id':admin_uid}):
        collection.insert_one(dict(data))
        break
    else:
        return "return admin_id is not available"

@app.put('/admin/updateuser/{admin_uid}/{user_id}')
def update_user(admin_uid,user_id,data:oldData):
    collection=db.users
    for i in collection.find({'user_id':admin_uid}):
        if data.email and data.role:
            collection.update_one({'user_id':user_id},{'$set':dict(data)})
        else:
            if data.email==None:
                del data.email
                collection.update_one({'user_id':user_id},{'$set':dict(data)})
                
            else:
                del data.role
                collection.update_one({'user_id':user_id},{'$set':dict(data)})

@app.delete('/admin/{admin_uid}/{user_id}')
def delete_user(admin_uid,user_id):
    collection=db.users
    collection.delete_one({'user_id':user_id})