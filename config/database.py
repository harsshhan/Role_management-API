from pymongo import MongoClient

client=MongoClient("mongodb+srv://harshan:harshanmathi@role-management.a68cz.mongodb.net/?retryWrites=true&w=majority&appName=role-management")
db=client['role_management']

# collection_name=db.users
