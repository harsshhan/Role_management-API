from fastapi import FastAPI,HTTPException
from config.database import db
from models.model import NewData,OldData,Task

app=FastAPI()


@app.post('/admin/newuser/{admin_uid}')
def adduser(admin_uid,data:NewData):    #this function is to add new profile(user or manager) by admin 
    collection=db.users
    admin=collection.find_one({'user_id':admin_uid})  
    if admin: #if admin user_id available in the database then new profile will be added to the db
        collection.insert_one(dict(data))
    else:       #else it will raise an error
        raise HTTPException(status_code=401,detail='Admin_id is Wrong')

@app.put('/admin/updateuser/{admin_uid}/{user_id}')
def update_user(admin_uid,user_id,data:OldData):    #this function is to update the existing profile(manager or user) by admin
    collection=db.users
    admin=collection.find_one({'user_id':admin_uid})    #check and store if admin user_id is available in the database

    if admin: #if the admin_id correct then this if statement executes to update the profile data
        if collection.find_one({'user_id':user_id}): #if the user_id exists then it will edit the data
            if data.email and data.role:
                collection.update_one({'user_id':user_id},{'$set':dict(data)})
            elif data.email==None:
                del data.email
                collection.update_one({'user_id':user_id},{'$set':dict(data)})   
            elif data.role==None:
                del data.role
                collection.update_one({'user_id':user_id},{'$set':dict(data)})
            else:   #if the user_id does not exists then it will raise an error
                raise HTTPException(status_code=400, detail="Both the fields are Empty")
    else:   # if the admin_id is incorrect it will raise an Error
        raise HTTPException(status_code=401,detail='Admin_id is Wrong')

@app.delete('/admin/{admin_uid}/{user_id}')   #delete the profile(user or manager) --admin
def delete_user(admin_uid,user_id):
    collection=db.users
    admin=collection.find_one({'user_id':admin_uid})  
    if admin:    #if admin user_id is correct then the given user_id profile will be deleted
        collection.delete_one({'user_id':user_id})
    else:       #else it will raise an error 
        raise HTTPException(status_code=401,detail='Admin_id is wrong')

@app.post('/admin/create_tasks/{admin_uid}')
def create_task(admin_uid,data:Task):
    collection=db.users
    for i in collection.find({'user_id':admin_uid}):
        if i['role']=='admin' or i['role']=='manager':
            collection=db.task
            if db.users.find_one({'user_id':data.assigned_to}):
                collection.insert_one({'task':data.task_name,'deadline':data.deadline,'assigned_to':data.assigned_to,'assigned_by':i['name']})
                break
            else:
                raise HTTPException(status_code=401,detail='user_id does not exist')
                
    else:
        raise HTTPException(status_code=401,detail='admin/manager id does not exist')


@app.get('/tasks/{user_id}')
def show_tasks(user_id):
    collection=db.task
    tasks=[]
    if db.users.find_one({'user_id':user_id}):
        cursor=db.task.find({'assigned_to':'m1'})
        task={}
        for i in cursor:
            for key,value in i.items():
                task[key]=str(value)
            tasks.append(task)
        return tasks
    else:
        raise HTTPException(status_code=401,detail='user_id does not exist')
        
