import subprocess
import json
from web3 import Web3
from web3.auto.gethdev import w3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from pathlib import Path
from getpass import getpass
from bit import wif_to_key
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from dotenv import load_dotenv
import os
load_dotenv()
from constants import *
import bit


mnemonic = os.getenv('MNEMONIC')

def derive_wallets(coin):
    command = f'./derive -g --mnemonic="{mnemonic}"--cols=path,address,privkey,pubkey --format=json --coin="{coin}" --numderive=3'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return keys

coins = {
    ETH: derive_wallets(ETH),
    BTCTEST: derive_wallets(BTCTEST)
}    
print(coins)

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


def priv_key_to_account(coin, priv_key):
    if coin == BTCTEST:
        return bit.PrivateKeyTestnet(priv_key) 
    elif coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    else:
        print('Must use either BTCTEST or ETH')


def create_tx(coin,account,to,amount):
    if coin == BTCTEST:
        return bit.PrivateKeyTestnet.prepare_transaction(account.address, [(to,amount,BTC)])
    elif coin == ETH:
        
        
        gas_estimate = w3.eth.estimateGas(
            {'from': account.address,'to': to, 'value': amount}
            )
        
        return {
            'from': account.address,
            'to': to,
            'value': amount,
            'gasPrice': w3.eth.gasPrice,
            'gas': gas_estimate,
            'nonce':w3.eth.get.getTransactionCount(account.address)
        }
    
    else:
        print('Must use either BTCTEST or ETH')

def send_tx(coin, account,to,amount):
    if coin == BTCTEST:
        raw_tx = create_tx(coin,account,to,amount)
        signed = account.sign_transaction(raw_tx)
        return NetworkAPI.broadcast_tx_testnet(signed)
    elif coin == ETH:
        raw_tx = create_tx(coin,account,to,amount)
        signed = account.signTransaction(raw_tx)
        return w3.eth.sendRawTransaction(signed.rawTransaction)
    else:
        print('Must use either BTCTEST or ETH')
    



   


owner_account_priv_key = os.getenv('key1'))
key2 = wif_to_key(os.getenv('key2'))  

     
    
currency_to_transact = BTCTEST
owner_account_priv_key = coins[currency_to_transact][0]['privkey']
receiver_account = coins[currency_to_transact][1]['address']
ETH_to_send = 10000000000000000000
BTCTEST_to_send = 0.00001

account = priv_key_to_account(currency_to_transact, owner_account_priv_key)


if currency_to_transact == ETH:
    send_tx(currency_to_transact,account,receiver_account,ETH_to_send)
elif currency_to_transact == BTCTEST:
    send_tx(currency_to_transact,account,receiver_account,BTCTEST_to_send)
else:
    print('You can only use ETH or BTCTEST to transact')
    
send_tx(currency_to_transact,account,receiver_account,BTCTEST_to_send)