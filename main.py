import pymongo
import os

from dotenv import load_dotenv
from pymongo import MongoClient

#Connecting to ENV file
load_dotenv()
DATABASE_CONNECTION = os.getenv('DATABASE_CONNECTION')

cluster = MongoClient(DATABASE_CONNECTION)

db = cluster["test"]

collection = db["users"]


results = collection.find({"username":"jero"})

#print(results)  #PyMongo cursos object!

for result in results:
    print(result)