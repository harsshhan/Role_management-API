from fastapi import FastAPI,HTTPException
from config.database import db
from models.model import NewData,OldData,Task,EditTask

app=FastAPI()


@app.post('/admin/newuser/{admin_uid}')
def adduser(admin_uid,data:NewData):    #this function is to add new profile(user or manager) by admin 
    collection=db.users
    try:
        admin=collection.find_one({'user_id':admin_uid})['role']
        if admin=='admin': #if admin user_id available in the database then new profile will be added to the db
            dat={}
            for key,value in dict(data).items():
                if value is None or value=='string' or value=='':
                    raise HTTPException(status_code=404,detail='Field should not be empty')
            else:
                collection.insert_one(dict(data))
                    
        else:       #else it will raise an error
            raise HTTPException(status_code=401,detail='You dont have access to add user')
    except TypeError:
        raise HTTPException(status_code=401,detail='Admin_id does not exist')

@app.put('/admin/updateuser/{admin_uid}/{user_id}')
def update_user(admin_uid,user_id,data:OldData):    #this function is to update the existing profile(manager or user) by admin
    collection=db.users
    try:
        admin=collection.find_one({'user_id':admin_uid})['role']    #check and store if admin user_id is available in the database
        if admin=='admin': #if the admin_id correct then this if statement executes to update the profile data
            if collection.find_one({'user_id':user_id}): #if the user_id exists then it will edit the data
                    dic={}  #create dictionary to store the data
                    for field_name,field_value in dict(data).items():
                        if field_value is not None and field_value!='string' and field_value!='': #add key,value pairs to the dic variable if field_name is not none
                            dic[field_name]=field_value
                    if dic:
                        collection.update_one({'user_id': user_id}, {'$set': dic})  # updating in the respective task_id
                    else:
                        raise HTTPException(status_code=400, detail='No fields to update')
            else:   #if the user_id does not exists then it will raise an error
                raise HTTPException(status_code=401,detail='user_id does not exist')
        else:   #if the role of given user_id is not admin then it will raise an error
            raise HTTPException(status_code=401,detail='You dont have access to edit the profile')
    
    except TypeError:
        raise HTTPException(status_code=401,detail='admin user_id does not exist')

@app.delete('/admin/{admin_uid}/{user_id}')   #delete the profile(user or manager) --admin
def delete_user(admin_uid,user_id):
    collection=db.users
    try:
        admin=collection.find_one({'user_id':admin_uid})['role']
        if admin=='admin':   #if user_id is admin then it will execute
            if collection.find_one({'user_id':user_id}):   #checks if the given user_id is present in the db
                collection.delete_one({'user_id':user_id})
            else:   #if the given user_id not available in the db --> it will raise an error
                raise HTTPException(status_code=400,detail="user_id does not exist")
        else:       #else it will raise an error 
            raise HTTPException(status_code=401,detail='You dont have access to delete the profile')
    except TypeError:
        raise HTTPException(status_code=401,detail='User_id does not exist')

@app.post('/create_tasks/{user_id}')
def create_task(user_id,data:Task):  #task createion 
    collection=db.users           
    access= collection.count_documents({'user_id': user_id,})  #checks whether the given user_id available in db
    if access:
        #storing name and role of the assigning user_id
        assigned_by_name,role=collection.find_one({'user_id':user_id})['name'],collection.find_one({'user_id':user_id})['role'] 
        if db.users.find_one({'user_id':data.assigned_to}): #checks whether the assigned_to user_id is available in the db
            collection=db.task
            if role=='manager': #checks whether role is manager
                if db.users.find_one({'user_id':data.assigned_to})['role']=='admin':  # manager cant assign tasks to admin
                    raise HTTPException(status_code=400,detail='You dont have access to assign tasks to admin')
                else:
                    dic={}
                    for key,value in dict(data).items():
                        if value is None or value=='string' or value=='':
                            raise HTTPException(status_code=404,detail='Field should not be empty')
                    else:
                        collection.insert_one({'task_id':data.task_id,'task':data.task,'deadline':data.deadline,'assigned_to':data.assigned_to,'assigned_by':assigned_by_name,'status':data.status})
            elif role=='user':
                #checks whether the user assigning the task to him
                if db.users.find_one({'user_id':data.assigned_to})['user_id']==user_id:  # regular users can assign task only to them
                    dic={}
                    for key,value in dict(data).items():
                        #if any field value is none or 'string' --> raise an error
                        if value is None or value=='string' or value=='':
                            raise HTTPException(status_code=404,detail='Field should not be empty')
                    else:
                        collection.insert_one({'task_id':data.task_id,'task':data.task,'deadline':data.deadline,'assigned_to':data.assigned_to,'assigned_by':assigned_by_name,'status':data.status})
                #if user assign task to someone else --> raise an error
                else:
                    raise HTTPException(status_code=400,detail='You dont have access to assign tasks to admin/manager')
            #if role is not manager then it is admin     
            else:  
                for key,value in dict(data).items():
                        #if any field value is none or 'string' --> raise an error
                        if value is None or value=='string' or value=='':
                            raise HTTPException(status_code=404,detail='Field should not be empty')
                else:
                    collection.insert_one({'task_id':data.task_id,'task':data.task,'deadline':data.deadline,'assigned_to':data.assigned_to,'assigned_by':assigned_by_name,'status':data.status})
                
        
        else:   #user_id not availabe in db--> raise an error
            raise HTTPException(status_code=401,detail='User_id does not exist') 
    else:   #admin/manager id wrong --> raise an error
        raise HTTPException(status_code=401,detail='admin/manager id does not exist')
    
@app.put('/edit_task/{user_id}/{task_id}')
def edit_task(user_id,task_id,data:EditTask):
    collection=db.task
    profile=db.users.find_one({"user_id":user_id})  #checks whether user_id exists or not
    if profile:
        #check task_id exists
        if collection.find_one({'task_id':task_id}):
            #storing the role of task assigned_to user_id
            assigned_to_role=db.users.find_one({'user_id':collection.find_one({'task_id':task_id})['assigned_to']})['role']

            #if given user_id -- admin
            if profile['role']=='admin':       #checking the role of the user_id
                    dic={}  #create dictionary to store the data
                    for field_name,field_value in dict(data).items():
                        if field_value is not None and field_value!='string': #add key,value pairs to the dic variable if field_name is not none
                            dic[field_name]=field_value
                    if dic:
                        collection.update_one({'task_id': task_id}, {'$set': dic})  # updating in the respective task_id
                    else:
                        raise HTTPException(status_code=400, detail='No fields to update')      
            
            #if given user_id -- manager
            elif profile['role']=='manager':
                    dic={}
                    for field_name,field_value in dict(data).items():
                        if field_value is not None and field_value!='string': #add key,value pairs to the dic variable if field_name is not none,string
                            dic[field_name]=field_value
                    #role= manager or user then update
                    if assigned_to_role=='manager' or assigned_to_role=='user':
                        if dic:
                            collection.update_one({'task_id': task_id}, {'$set': dic})  # updating in the respective task_id
                        else:
                            raise HTTPException(status_code=400, detail='No fields to update')     
                    # if the task_assined to role is admin --> raise an error 
                    else:
                        raise HTTPException(status_code=401,detail='You dont have access to edit admin task')
            
            #if given user_id -- user
            else:
                dic={}
                for field_name,field_value in dict(data).items():
                    if field_value is not None and field_value!='string': #add key,value pairs to the dic variable if field_name is not none,string
                        dic[field_name]=field_value 
                if assigned_to_role=='user':
                    if dic:
                        collection.update_one({'task_id': task_id}, {'$set': dic})  # updating in the respective task_id
                    else:
                        raise HTTPException(status_code=400, detail='No fields to update')   
                else:
                    raise HTTPException(status_code=401,detail='You dont have access to edit this task')                  
        
        #if the task_id does not exist
        else:
            raise HTTPException(status_code=404,detail='task_id does not exist')

    else:
        raise HTTPException(status_code=401,detail='User_id does not exist')


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
                #storing the role of user_id of task assigned_to 
                task_assigned_to_role=db.users.find_one({'user_id':task['assigned_to']})['role']
                if task_assigned_to_role=='user' or task_assigned_to_role=='manager':
                    db.task.delete_one({'task_id':task_id})
                else:
                    raise HTTPException(status_code=404,detail='You dont have access to delete this task')
                
            #admin  
            if role=='admin':   #admin can delete tasks assigned to all (admin,manager,user)
                db.task.delete_one({'task_id':task_id})
        #if task_id not available in db -- raise an error
        else:
            raise HTTPException(status_code=401,detail='task_id does not exist')
    # if user_id not in db -- raise error
    else:
        raise HTTPException(status_code=401,detail='User_id does not exist')
