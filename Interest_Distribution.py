"""
Created on Mon Dec 26 14:04:30 2022

This script's purpose is to move fund's from Fennec's' admin wallet to users 
personal Web3 wallet.

@author: jeron
"""


from web3 import Web3
import os
import json
from dotenv import load_dotenv

os.getcwd()
#os.chdir('C:\\Users\\jeron\\OneDrive\\Desktop\\Fennec\\Accounting') #Your CWD
load_dotenv()


#All keys
infura_key = os.getenv('INFURA_TOKEN')
MM_Private_Key = os.getenv('ADMIN_MM_PRIVATE_KEY')

#Addresses
Admin_Address = '0xaCd29F685C3bDf33588Aa90Bb65A69B4b098e62F'


w3 = Web3(Web3.HTTPProvider(f'https://polygon-mainnet.infura.io/v3/{infura_key}'))
if w3.isConnected() == True:
    print("You are connected to Polygon!")
else:
        print("You have not been able to connect to Polygon...")
        
        

#USDC Token Contract
with open("USDC.json") as f:
    erc20_abi = json.load(f)
    
usdc_contract = w3.eth.contract(address=Web3.toChecksumAddress(
"0x2791bca1f2de4661ed88a30c99a7a9449aa84174"), abi=erc20_abi)  ##USDC comtract address



balance = w3.eth.get_balance('0xbF14e7d2Adb75066cc008fF1DCeb03F15B6eD74c')
print("Admin has a balance of: $" + str(balance/1e18))


#Addresses

_to = Web3.toChecksumAddress(Admin_Address) # To address
_from =Web3.toChecksumAddress('0xbF14e7d2Adb75066cc008fF1DCeb03F15B6eD74c') # From address


nonce = w3.eth.get_transaction_count(_from)

"""
tx = {
      'nonce': nonce,
      'to': _to,
      'value': w3.toWei(1, 'ether'),
      'gas': 21000,
      'gasPrice': w3.toWei(40, 'gwei')
  }

signed_tx = w3.eth.account.signTransaction(tx, MM_Private_Key)

tx_sent = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
"""


transfer_txn = usdc_contract.functions.transferFrom(_from ,_to, 2).buildTransaction({
'chainId': 137,
'gas': 5000,
'gasPrice': w3.toWei('60', 'gwei'),
'nonce': nonce,})


#sining txn


signed_txn = w3.eth.account.sign_transaction(transfer_txn,
private_key = bytearray.fromhex(MM_Private_Key.replace("0x", ""))) # sender's private key
rawTxn = signed_txn.rawTransaction





tx_hash=w3.eth.send_raw_transaction(rawTxn)
w3.eth.wait_for_transaction_receipt(tx_hash)












