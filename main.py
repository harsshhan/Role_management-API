from fastapi import FastAPI,HTTPException
from config.database import db
from models.model import NewData,OldData,Task,EditTask

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
            if data.role==None or data.role=='string':
                del data.role
                collection.update_one({'user_id':user_id},{'$set':dict(data)})
            elif data.email==None or data.email=='string':
                del data.email
                collection.update_one({'user_id':user_id},{'$set':dict(data)})   
            elif data.email and data.role:
                collection.update_one({'user_id':user_id},{'$set':dict(data)})
            elif data==[]:   
                raise HTTPException(status_code=400, detail="Both the fields are Empty")
        else:   #if the user_id does not exists then it will raise an error
            raise HTTPException(status_code=401,detail='user_id does not exist')
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

@app.post('/create_tasks/{user_id}')
def create_task(user_id,data:Task):  #task createion 
    collection=db.users
    access= collection.count_documents({'user_id': user_id, 'role': {'$in': ['admin', 'manager']}})
    if access:
        name=collection.find_one({'user_id':user_id})['name']
        collection=db.task
        if db.users.find_one({'user_id':data.assigned_to}):  #if the assigned userid exists then tasks will be added
            collection.insert_one({'task_id':data.task_id,'task':data.task_name,'deadline':data.deadline,'assigned_to':data.assigned_to,'assigned_by':name})
            
        else:
            raise HTTPException(status_code=401,detail='user_id does not exist')
                     
    else:
        raise HTTPException(status_code=401,detail='admin/manager id does not exist')
    
@app.put('/edit_task/{user_id}/{task_id}')
def edit_task(user_id,task_id,data:EditTask):
    collection=db.task
    if db.users.find_one({'user_id':user_id}): # checks if the given userid is admin/manager
        if collection.find_one({'task_id':task_id}):    #checks wherther the task id exists or not
            dic={}
            for field_name,field_value in dict(data).items():
                if field_value is not None and field_value!='string': #add key,value pairs to the dic variable if field_name is not none
                    dic[field_name]=field_value
            if dic:
                collection.update_one({'task_id': task_id}, {'$set': dic})  # updating in the respective task_id
            else:
                raise HTTPException(status_code=400, detail='No fields to update')
              
        else:
            raise HTTPException(status_code=404,detail='task_id does not exist')
    else:
        raise HTTPException(status_code=401,detail='Admin/manager id does not exist')
    

@app.get('/tasks/{user_id}')
def show_tasks(user_id):
    collection=db.task
    tasks=[]
    if db.users.find_one({'user_id':user_id}):
        cursor=collection.find({'assigned_to':user_id})
        for i in cursor:
            task={}
            for key,value in i.items():
                task[key]=str(value)
            tasks.append(task)
        return tasks
    else:
        raise HTTPException(status_code=401,detail='user_id does not exist')
        
@app.delete('/tasks/{user_id}/{task_id}')
def delete_task(user_id,task_id):
    profile=db.users.find_one({'user_id':user_id})  #checks if the user_id exists
    task=db.task.find_one({'task_id':task_id})      #checks if the task_id exists
    if profile:
        if task:
            role=profile['role']     #storing the role of given user_id

            #regular user
            if role=='user':    #if user then they can delete only the task assigned to them
                if db.task.find_one({'task_id':task_id,'assigned_to':user_id}):
                        db.task.delete_one({'task_id':task_id})
                else:
                    raise HTTPException(status_code=404,detail='You dont have access to delete this task')
            
            #manager
            if role=='manager':
                if db.users.find_one({"user_id":user_id,'role':{'$in': ['user', 'manager']}}):
                    db.task.delete_one({'task_id':task_id})
                else:
                    raise HTTPException(status_code=404,detail='You dont have access to delete this task')
                
            #admin
            if role=='admin':
                db.task.delete_one({'task_id':task_id})

        else:
            raise HTTPException(status_code=401,detail='task_id does not exist')
        
    else:
        raise HTTPException(status_code=401,detail='User_id does not exist')
