from constants import *
import subprocess
import json
import os
from web3 import Web3
from dotenv import load_dotenv
from eth_account import Account
from web3.middleware import geth_poa_middleware


load_dotenv()

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


mnemonic = os.getenv('MNEMONIC', 'erase spare bulk brisk climb pudding elevator frozen mesh valley economy affair short subject innocent')

coin = BTCTEST, ETH
def derive_wallets(coin):
    coins = {}
    for crypto in coin:
        command = f'/Users/dhruvmudambi/Desktop/wallet/./derive -g --mnemonic="erase spare bulk brisk climb pudding elevator frozen mesh valley economy affair short subject innocent" --coin={crypto} --numderive=3 --cols=path,address,privkey,pubkey --format=json'

        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        p_status = p.wait()

        keys = json.loads(output)
        keys = {crypto: keys}
        coins.update(keys)
    return coins

coins = derive_wallets(coin)
print(coins)

account_eth = Account.from_key(coins[ETH][2]['privkey'])
account_btctest = Account.from_key(coins[BTCTEST][1]['privkey'])

def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        priv_key = coins[ETH][2]['privkey']
        return Account.privateKeyToAccount(priv_key)
    else:
        priv_key = coins[BTCTEST][1]['privkey']
        return PrivateKeyTestnet(priv_key) 

def create_tx(coin, account, to, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": recipient, "value": amount}
    )
        return {
        "to": recipient,
        "from": account.address,
        "value": amount,
        "gas": gasEstimate,
        "gasPrice": w3.eth.gasPrice,
        "nonce": w3.eth.getTransactionCount(account.address), 
        "ChainID" : ChainID 
        }   
    else:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

def send_tx(coin, account, to, amount):
    raw_tx = create_raw_tx(coin, account, to, amount)
    signed_tx = account.sign_transaction(raw_tx)
    result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    if coin == ETH:
        return w3.eth.sendRawTransaction(signed.rawTransaction)
    else:
        return NetworkAPI.broadcast_tx_testnet(signed)

