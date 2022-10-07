import pymongo
import os
import time
import hmac

from dotenv import load_dotenv
from pymongo import MongoClient
from requests import Request, Session


#Connecting to ENV file
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

#POSITIONS... note that FTX has an endpoint in Account=> GetPositions
positions_coll = db["positions"]
positions = positions_coll.find()

"""
for user in users:
    #print(len(user["Positions"]))
    if(len(user["Positions"])) > 0:
        print("Your users: \n")
        print(user["_id"])
"""


ALL_POSITIONS = []

for position in positions:
    #print(position)
    ALL_POSITIONS.append({
        'User': position["user"],
        'Capital': position["Capital"],
        'dir': position["dir"]
    })
    
    
    
#print(ALL_POSITIONS)


#GETTING MAX EXTRACTABLE VLAUE
MAX_EXTRACTABLE = 0
for i in ALL_POSITIONS:
    #print(i["Capital"] * (1+(i['dir'])/100))
    MAX_EXTRACTABLE += i["Capital"] * (1+(i['dir']/100))








#Connecting to FTX API
FTX_API_KEY = os.getenv('FTX_API_KEY')
FTX_API_SECRET = os.getenv(('FTX_API_SECRET'))
BASE_URL = "https://ftx.com/api"

ts = int(time.time() * 1000)

s = Session()

request = Request('GET', F"{BASE_URL}/wallet/balances")
prepared = request.prepare()
signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
signature = hmac.new(FTX_API_SECRET.encode(), signature_payload, 'sha256').hexdigest()

prepared.headers['FTX-KEY'] = FTX_API_KEY
prepared.headers['FTX-SIGN'] = signature
prepared.headers['FTX-TS'] = str(ts)

# Only include line if you want to access a subaccount. Remember to URI-encode the subaccount name if it contains special characters!
prepared.headers['FTX-SUBACCOUNT'] = 'JerryFut'

response = s.send(prepared)
data = response.json()
coins = data["result"]


#GETTING CURRENT USD VALUE
USD_VALUE = 0
for obj in coins:
    #print(obj)
    if(obj["coin"] == "USD"):
        #print(obj["availableForWithdrawal"])
        USD_VALUE = obj["availableForWithdrawal"]
        """COMMENT THIS OUT!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
        #USD_VALUE = 15.046












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





difference_lost = MAX_EXTRACTABLE - NEW_EXTRACTABLE

print("Users are owed a total of: " + str(MAX_EXTRACTABLE) +"\n")

print("FTX account has a total of: " + str(USD_VALUE) +"\n")


print("In this example, we have failed to generate a total of: " + str(difference_lost))

print("Fennec can charge the above (in case it's negative)")





for i in ALL_POSITIONS:
    i["FinalBalance"] = i["Capital"] * ( 1 + ( (i['dir']/100) * (1-CUT_PRCT) ) )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#MODIFY USERS table in mongo db BY FinalBalnace !!!!!!!


"""
users_coll = db["users"]
users = users_coll.find()

    
for user in users:
    #print(len(user["Positions"]))
    if(len(user["Positions"])) > 0:
        print("User ID: " + str(user["_id"]))
        
        for pos in ALL_POSITIONS:
            if(user["_id"] == pos["User"]):
                print("Found a position of his !")
                
                
                #ADDING THE AVAILABLE + INTERESTS
                
                users_coll.update_one(
                    {'_id': user["_id"] },
                    {'$inc': 
                     {'Available': pos["FinalBalance"]}
                    }
                )
                
                    
                #DELETING ALL POSITIONS IN THE MARKET
                users_coll.update_one(
                    {'_id': user["_id"] },
                    {'$set': 
                     {'Positions':[]}
                    }
                )
                
    
"""
    
    





#DELETE ALL POSITIONS

"""
positions_coll = db["positions"]


results = positions_coll.delete_many({})


"""























