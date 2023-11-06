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
from web3.middleware import geth_poa_middleware


os.getcwd()
os.chdir('C:/Users/jeron/OneDrive/Desktop/Fennec/Accounting') #Your CWD
load_dotenv()

infura_key = os.getenv('INFURA_TOKEN')
MM_Private_Key = os.getenv('ADMIN_MM_PRIVATE_KEY')        #THIS IS ADMINS!  
Admin_Address = os.getenv('ADMIN_ADDRESS')

def send_to(to_adrs, usdt_amt):
        
    w3 = Web3(Web3.HTTPProvider(f'https://polygon-mainnet.infura.io/v3/{infura_key}'))
    
    if w3.isConnected() == True:
        print("You are connected to Polygon!")
    else:
        print("You have not been able to connect to Polygon...")
            
    
    
    #signer = w3.eth.account.from_key('0x' + MM_Private_Key)
    #pub_key = signer.address
    
    
    
    _to = Web3.toChecksumAddress(str(to_adrs))
    _from =Web3.toChecksumAddress(Admin_Address) 
    
    
    
    
    #USDT Token Contract
    with open("./Constants/ERC20.json") as f:
        erc20_abi = json.load(f)
        
        
        
    
    #getting contract instance
    contract_address='0xc2132D05D31c914a87C6611C10748AEb04B58e8F'  #USDT CONTRACT
    erc20_contract =  w3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=erc20_abi)
    
    balance = w3.eth.get_balance(_from)
    usd = erc20_contract.functions.balanceOf(_from).call()
    print("Fennec Admin Wallet has a balance of:\n")
    print("   " + str(round(w3.fromWei(balance, 'ether'),3)) + ' MATIC')
    print("&")
    print("   " + str(round(usd/1e6,3)) + ' USDT ')
    
    #inject middleware
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    
    
    chain_id = 137 # Polygon Mumbai test chain
    nonce = w3.eth.getTransactionCount(_from)
    
    
    
    
    transfer_amt = int(usdt_amt*1e6) #USDT has 6 decimals
    
    
    
    try:
        # creating a transaction                                          #DEPRICATED FOR build_transaction
        transfer_txn = erc20_contract.functions.transfer(_to,transfer_amt).buildTransaction({ "chainId": chain_id,
                                                                                             "from": _from,
                                                                                             "nonce": nonce})
        # signing transaction with pvt key
        signed_tx = w3.eth.account.sign_transaction(transfer_txn, MM_Private_Key)
        # sending the transaction
        txn_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print('Transaction hash:',txn_hash.hex())
        #wait for the transaction to process
        #txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
        
        return "1"
    
    except Exception as err: 
        print('Transaction Error:',err)
        return "0"
    


"""
balAfter = erc20_contract.functions.balanceOf(pub_key).call()
print('ERC20 Balance after:',w3.fromWei(balAfter,'ether'),'tokens')

"""

