"""
Code revamped to OKX; 
unlike backend app that trades on official OKX API, this accounting uses the CCXT
client for a simple connection. 

Author: @JerryTheKid

"""

#ENV variables
import os

#CCXT
import ccxt

#Mongo
from dotenv import load_dotenv
from pymongo import MongoClient





#MATURITY THAT HAS BEEN REACHED AND LIQUIDATED COMPLETELY:
    
Liquidated_Maturity = '2023-09-29 00:00:00'




#Connecting to ENV file
os.getcwd()
#os.chdir('OneDrive/Desktop/Fennec/Accounting') #Your CWD

load_dotenv()


#Connection to the collection
DATABASE_CONNECTION = os.getenv('DATABASE_CONNECTION')
cluster = MongoClient(DATABASE_CONNECTION)

#Getting the tables from our test cluster
db = cluster["test"]

#USERS
users_coll = db["users"]
users = users_coll.find()
#print(users)  #PyMongo cursos object.

#POSITIONS... note that OKX has an endpoint in Account=> GetPositions
positions_coll = db["positions"]
positions = positions_coll.find()


ALL_POSITIONS = []

for position in positions:
    if Liquidated_Maturity == str(position["Maturity"]):
        
        #print(position)
        ALL_POSITIONS.append({
            'User': position["user"],
            'Capital': position["Capital"],
            'dir': position["dir"],
            'Maturity': position["Maturity"],
            '_id': position["_id"]
        })
    
    
    


#GETTING MAX EXTRACTABLE VLAUE
MAX_EXTRACTABLE = 0
for i in ALL_POSITIONS:
    #print(i["Capital"] * (1+(i['dir'])/100))
    MAX_EXTRACTABLE += i["Capital"] * (1+(i['dir']/100))








#Connecting to OKX API through CCXT

OKX_API_KEY = os.getenv('OKX_API_KEY')
OKX_API_SECRET = os.getenv(('OKX_API_SECRET'))
OKX_PASSPHRASE = os.getenv(('OKX_PASSPHRASE'))

exchange = ccxt.okx()

exchange.apiKey = OKX_API_KEY
exchange.secret = OKX_API_SECRET
exchange.password = OKX_PASSPHRASE

trading_balance = exchange.fetch_balance()

#GETTING CURRENT USD VALUE
USD_VALUE = 0

for i in trading_balance["info"]["data"][0]["details"]:
    if i["ccy"] == "USDT":
        #print("USD!")
        USD_VALUE = float(i["availBal"])







#DEFINING THE CUT APERCENTAGE
CUT_PRCT = 0

NEW_EXTRACTABLE = MAX_EXTRACTABLE


while NEW_EXTRACTABLE > USD_VALUE:
    
    CUT_PRCT += 0.000001
    
    
    MOD_EXTRACTABLE = 0

    for i in ALL_POSITIONS:
        #print(i["Capital"] * (1+(i['dir'])/100))
        MOD_EXTRACTABLE += i["Capital"] * ( 1 + ( (i['dir']/100) * (1-CUT_PRCT) ) )
        
        
    #print(CUT_PRCT)
        
    NEW_EXTRACTABLE = MOD_EXTRACTABLE





difference_lost = MAX_EXTRACTABLE - USD_VALUE

print("Users are owed a total of: $" + str(round(MAX_EXTRACTABLE, 2)) +"\n")

print("OKX account has a total of: $" + str(round(USD_VALUE,2)) +"\n")

if difference_lost > 0:
    print("We have failed to generate a total of: " + str(round(difference_lost, 2)))
else:
    print("Fennec can charge a total of: $" + str(-round(difference_lost,2)))
#this not working for 

print("(If = 0.0 then make sure all positions are closed and proceed with acounting.)")





#THIS SETS THE CUT PERCENTAGE TO EACH USER.. DONT USE UNLESS AT A PROFIT OR VERY LOW LOSS AND PRINT RSTS

if CUT_PRCT > 0:
    for i in ALL_POSITIONS:
        print(i["Capital"] * ( 1 + ( (i['dir']/100) * (1-CUT_PRCT) ) ))
        i["FinalBalance"] = i["Capital"] * ( 1 + ( (i['dir']/100) * (1-CUT_PRCT) ) )
    
else:
    for i in ALL_POSITIONS:
        i["FinalBalance"] = i["Capital"] * ( 1 + ( (i['dir']/100) ) )
    

    
    
    
    
    
    
    
    
    
    
#MODIFY USERS table in mongo db BY FinalBalnace                                   <=           DANGEOURUS


"""


users_coll = db["users"]
users = users_coll.find()

    
for user in users:
    #print(user["Available"])
    alread_available = user["Available"]
    if(len(user["Positions"])) > 0:
        print("User ID: " + str(user["_id"]))
        
        for pos in ALL_POSITIONS:
            if(user["_id"] == pos["User"]):
                print("Found a position of his !")
                
                
                #ADDING THE AVAILABLE + INTERESTS
                
                users_coll.update_one(
                    {'_id': user["_id"] },
                    {'$inc': 
                     {'Available': alread_available + pos["FinalBalance"]}
                    }
                )
                
                    
                pos_del = users_coll.update_one( 
                    { "_id": user["_id"] },
                    { "$pull":
                     { "Positions": pos["_id"] } 
                     } 
                )


#DELETE POSITIONS
positions_coll = db["positions"]
positions = positions_coll.find()

for y in positions:
    for pos in ALL_POSITIONS:
        if y['_id'] == pos["_id"]:
            #print(y['_id'])
                            
            pos_del = positions_coll.delete_one( 
                { "_id": y["_id"] }
            )
    





"""





