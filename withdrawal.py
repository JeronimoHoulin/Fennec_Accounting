"""
Created on Wed Feb  8 18:05:50 2023

@author: JerryTheKid
"""
#WEIRD KEY ERROR

#ENV variables
import os

#Mongo
from dotenv import load_dotenv
from pymongo import MongoClient



#Connecting to ENV file
os.getcwd()
os.chdir('C:/Users/jeron/OneDrive/Desktop/Fennec/Accounting') #Your CWD

load_dotenv()


#Connection to the collection
DATABASE_CONNECTION = os.getenv('DATABASE_CONNECTION')
cluster = MongoClient(DATABASE_CONNECTION)

#Getting the tables from our test cluster
db = cluster["test"]

#USERS
users_coll = db["users"]
users = users_coll.find()

for user in users:
    
    if "Withdrawal" in user:
        
        withdraw_amt = user["Withdrawal"]
        
        if(withdraw_amt > 0):
            
            print("User wanting to withdrawal:")
            print(user["username"])
            print("\n")
            print("Does he have sufficient Available ?")
            if(user['Available'] > user["Withdrawal"]):
                print(True)
        
        
        
        
        
        
        
        
        
        
        