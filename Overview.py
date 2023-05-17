"""
Created on Sat Feb 18 20:03:56 2023

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


load_dotenv()


#Connection to the collection
DATABASE_CONNECTION = os.getenv('DATABASE_CONNECTION')
cluster = MongoClient(DATABASE_CONNECTION)


###  GENERIC OVERVIEW

#Getting the tables from our test cluster
db = cluster["test"]

#USERS
users_coll = db["users"]
users = users_coll.find()


#Positions
positions_coll = db["positions"]



fennec_total_locked = 0
fennec_total_interest = 0


for user in users:
    
                    
    if len(user["Positions"]) > 0:
                
        users_positions = []
        
        for pos_id in user["Positions"]:
            #print(type(pos_id))
            
            aposition = positions_coll.find_one({"_id": pos_id})
            
            users_positions.append(aposition)


        users_total_locked = 0
        users_total_interest = 0
        
        for i in users_positions:
            
            users_total_locked += i["Capital"]
            users_total_interest += i["Capital"] * i["dir"]/100
            
        
        #print("Total capital : $" + str(users_total_locked))
        #print("Total interest to be paid: $" + str(users_total_interest))

        
        fennec_total_locked += users_total_locked
        fennec_total_interest += users_total_interest

        #print("\n")
        
 


print("Fennec Total Locked: $" + str(fennec_total_locked))





Liquidated_Maturity = '2023-09-29 00:00:00'

print('\n\n\n')
print("To-do at maturity: " + Liquidated_Maturity)
print('--------------------------------------')
print('\n\n\n')







db = cluster["test"]

#USERS
users_coll = db["users"]
users = users_coll.find()


#Positions
positions_coll = db["positions"]



fennec_maturity_locked = 0
fennec_maturity_interest = 0

sell_positions_needed = []

for user in users:
    
                    
    if len(user["Positions"]) > 0:
                
        users_positions = []
        
        for pos_id in user["Positions"]:
            #print(type(pos_id))
            
            aposition = positions_coll.find_one({"_id": pos_id})
            
            users_positions.append(aposition)


        users_maturity_locked = 0
        users_maturity_interest = 0
        
        for i in users_positions:
            
            if str(i["Maturity"]) == Liquidated_Maturity:

                users_maturity_locked += i["Capital"]
                users_maturity_interest += i["Capital"] * i["dir"]/100
                
                symbol = i['Fut_Symb']
                amt = i['Capital']
                
                case = {
                            'symbol': symbol,
                            'amount': amt
                        }
                sell_positions_needed.append(case)
                
        
        if users_maturity_locked > 0:
            print(f'For {user["username"]}:')
            print("Total capital locked at upcoming maturity: $" + str(users_maturity_locked))
            print("Total interest to be paid at upcoming maturity: $" + str(users_maturity_interest))
        
            
            fennec_maturity_locked += users_maturity_locked
            fennec_maturity_interest += users_maturity_interest
        
            print("\n")
        


print("Fennec Total Locked at upcoming maturity: $" + str(fennec_maturity_locked + fennec_maturity_interest))
print('\n')
print("The sell positinos needed to collect interest: ")
uniquesymbols = {}
for i in sell_positions_needed:
    if i['symbol'] not in uniquesymbols.keys():
        uniquesymbols[i['symbol']] = i['amount']
    else:
       uniquesymbols[i['symbol']] += i['amount']

for key, val in uniquesymbols.items():
    print(f"there are ${val} of {key} that need's to be in a sell position.")
    








