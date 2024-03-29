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

    if admin['role']=='admin': #if the admin_id correct then this if statement executes to update the profile data
        if collection.find_one({'user_id':user_id}): #if the user_id exists then it will edit the data
            if data.email_id is None and data.role is None:    #if both fields are empty then it will rasie an error
                raise HTTPException(status_code=400, detail="Both the fields are Empty")
            if data.email_id is None or data.email_id=='string': #if email_id field is empty then delete email_id field
                del data.email_id
            if data.role is None or data.role=='string':   #if role field is empty then delete role field
                del data.role
            if data:
                collection.update_one({'user_id': user_id}, {'$set': dict(data)})  
            else:
                raise HTTPException(status_code=400, detail="Both the fields are empty")
        else:   #if the user_id does not exists then it will raise an error
            raise HTTPException(status_code=401,detail='user_id does not exist')
    else:   # if the admin_id is incorrect it will raise an Error
        raise HTTPException(status_code=401,detail='Admin_id is Wrong')

@app.delete('/admin/{admin_uid}/{user_id}')   #delete the profile(user or manager) --admin
def delete_user(admin_uid,user_id):
    collection=db.users
    admin=collection.find_one({'user_id':admin_uid})  
    if admin['role']=='admin':   #if user_id is admin then it will execute
        if collection.find_one({'user_id':user_id}):   #checks if the given user_id is present in the db
            collection.delete_one({'user_id':user_id})
        else:   #if the given user_id not available in the db --> it will raise an error
            raise HTTPException(status_code=400,detail="user_id does not exist")
    else:       #else it will raise an error 
        raise HTTPException(status_code=401,detail='Admin_id is wrong')

@app.post('/create_tasks/{user_id}')
def create_task(user_id,data:Task):  #task createion 
    collection=db.users           
    access= collection.count_documents({'user_id': user_id, 'role': {'$in': ['admin', 'manager']}})  #checks whether the given user_id(admin/manager) available in db
    if access:
        name,role=collection.find_one({'user_id':user_id})['name'],collection.find_one({'user_id':user_id})['role'] #storing name and role of the assigning user_id
        if db.users.find_one({'user_id':data.assigned_to}): #checks whether the assigned_to user_id is available in the db
            collection=db.task
            if role=='manager': #checks whether role is manager
                if db.users.find_one({'user_id':data.assigned_to})['role']=='admin':  # manager cant assign tasks to admin
                    raise HTTPException(status_code=400,detail='You dont have access to assign tasks to admin')
                else:
                    collection.insert_one({'task_id':data.task_id,'task':data.task,'deadline':data.deadline,'assigned_to':data.assigned_to,'assigned_by':name,'status':data.status})
            else:   #if role is not manager then it is admin
                collection.insert_one({'task_id':data.task_id,'task':data.task,'deadline':data.deadline,'assigned_to':data.assigned_to,'assigned_by':name,'status':data.status})
        else:   #user_id not availabe in db--> raise an error
            raise HTTPException(status_code=401,detail='User_id does not exist') 
    else:   #admin/manager id wrong --> raise an error
        raise HTTPException(status_code=401,detail='admin/manager id does not exist')
    
@app.put('/edit_task/{user_id}/{task_id}')
def edit_task(user_id,task_id,data:EditTask):
    collection=db.task
    profile=db.users.find_one({"user_id":user_id})  #checks whether user_id exists or not
    if profile:
        if profile['role']=='admin':       #checking the role of the user_id
            if collection.find_one({'task_id':task_id}):    #checks wherther the task id exists or not
                dic={}  #create dictionary to store the data
                for field_name,field_value in dict(data).items():
                    if field_value is not None and field_value!='string': #add key,value pairs to the dic variable if field_name is not none
                        dic[field_name]=field_value
                if dic:
                    collection.update_one({'task_id': task_id}, {'$set': dic})  # updating in the respective task_id
                else:
                    raise HTTPException(status_code=400, detail='No fields to update')      
            else:
                raise HTTPException(status_code=404,detail='task_id does not exist')


@app.get('/tasks/{user_id}')
def show_tasks(user_id):
    collection=db.task
    tasks=[]    # create list to store datas
    if db.users.find_one({'user_id':user_id}):  # checks whether the user_id available in the db
        cursor=collection.find({'assigned_to':user_id}) # it store the cursor object if any task assigned_to given user_id
        for i in cursor:    #iterating the cursor object
            task={}
            for key,value in i.items():
                task[key]=str(value)    #storing key,value pairs from the cursor object
            tasks.append(task)
        return tasks    #returning the list -- contains list of tasks assigned_to given user_id
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
            if role=='user':    #if regural user then they can delete only the task assigned to them
                if db.task.find_one({'task_id':task_id,'assigned_to':user_id}):
                        db.task.delete_one({'task_id':task_id})
                else:
                    raise HTTPException(status_code=404,detail='You dont have access to delete this task')
            
            #manager
            if role=='manager': #manager can delete tasks assinged to them and to the user
                if db.users.find_one({"user_id":user_id,'role':{'$in': ['user', 'manager']}}):
                    db.task.delete_one({'task_id':task_id})
                else:
                    raise HTTPException(status_code=404,detail='You dont have access to delete this task')
                
            #admin  
            if role=='admin':   #admin can delete tasks assigned to all (admin,manager,user)
                db.task.delete_one({'task_id':task_id})

        else:
            raise HTTPException(status_code=401,detail='task_id does not exist')
        
    else:
        raise HTTPException(status_code=401,detail='User_id does not exist')
