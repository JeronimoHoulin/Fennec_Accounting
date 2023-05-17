"""
Created on Wed Feb  8 18:05:50 2023

@author: JerryTheKid
"""

#ENV variables
import os

#Mongo
from dotenv import load_dotenv
from pymongo import MongoClient


#Connecting to ENV file
os.getcwd()
os.chdir('C:/Users/jeron/OneDrive/Desktop/Fennec/Accounting') #Your CWD

#USDT Sending function
from USDT_Sender import send_to


load_dotenv()


#Connection to the collection
DATABASE_CONNECTION = os.getenv('DATABASE_CONNECTION')
cluster = MongoClient(DATABASE_CONNECTION)

#Getting the tables from our test cluster
db = cluster["test"]

#USERS
users_coll = db["users"]
users = users_coll.find()

Total_to_Withdraw = 0

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
                
                #Add total to withdraw
                
                Total_to_Withdraw += withdraw_amt
        

print("Total Withdrawal Amount : $" + str(Total_to_Withdraw))
        
##############################################################################
"""
Once withdrawed from OKX into Fennec Account, run this:
"""
##############################################################################

users_coll = db["users"]
users = users_coll.find()

"""
for user in users:
    
    if "Withdrawal" in user:
        
        withdraw_amt = user["Withdrawal"]
        
        if(withdraw_amt > 0):
            
            if(user['Available'] > user["Withdrawal"]):

                #Send USDT
                
                recipt = send_to(to_adrs=user["Wallet"], usdt_amt=withdraw_amt)
                
                if(recipt == "1"):
                    print("User " + user["username"] + " got paid!")
                    #Account for paid txn in mongo

                    users_coll.update_one(
                        {'_id': user["_id"] },
                        {'$inc': 
                         {'Available': - withdraw_amt}
                        }
                    )
                        
                    users_coll.update_one(
                        {'_id': user["_id"] },
                        {'$set': 
                         {'Withdrawal': 0}
                        }
                    )
                        
                    print("User updated in mongo")
                    
                else:
                    print("problem sending  " + user["username"] + " his funds.")
                
"""
        
        
        
        