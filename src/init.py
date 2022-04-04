import pickle
import time
from unittest import result
import os
import requests
import web3
from web3 import Web3, geth, exceptions
from solcx import compile_source, install_solc
from web3.middleware import geth_poa_middleware
import pickle

install_solc(version='latest')


def compile_source_file(file_path):
    with open(file_path, 'r') as f:
        source = f.read()

        return compile_source(source, output_values=['abi', 'bin'])

path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
data_path = os.path.join(path,'magazzino.sol') #viene preso il file magazzino.sol dalla cartella in cui si trovale il file .py in esecuzione
compiled_sol = compile_source_file(data_path)

# recupera l'interfaccia del contratto
contract_id, contract_interface = compiled_sol.popitem()

# prende il bytecode/bin
bytecode = contract_interface['bin']

# prende l'abi
abi = contract_interface['abi']


# crea un istanza di web3.py
w3 = Web3(web3.HTTPProvider("http://127.0.0.1:22000"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.middleware_onion.add(web3.middleware.http_retry_request_middleware)


if len(w3.eth.accounts) == 1:
    w3.geth.personal.new_account('trasformatore')
    w3.geth.personal.new_account('produttore')
    w3.geth.personal.new_account(('consumatore'))

print(w3.geth.personal.list_accounts())


print(Web3.toChecksumAddress(w3.eth.accounts[0])+" è il trasformatore")
print(Web3.toChecksumAddress(w3.eth.accounts[1])+" è il produttore")
print(Web3.toChecksumAddress(w3.eth.accounts[2])+" è il consumatore")


MagazzinoProdotti = w3.eth.contract(abi=abi, bytecode=bytecode)

# Invia la transazione che fa il deploy del contratto
trasf=Web3.toChecksumAddress(w3.eth.accounts[0])
prod=Web3.toChecksumAddress(w3.eth.accounts[1])
consum=Web3.toChecksumAddress(w3.eth.accounts[2])
admin=Web3.toChecksumAddress(w3.eth.accounts[3])

tx_hash = MagazzinoProdotti.constructor(prod, trasf, consum).transact({'from': admin})
#Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

magazzino = w3.eth.contract(
    address=tx_receipt['contractAddress'],
    abi=abi
)

#account = trasf+" "+prod+" "+consum+" "+admin
address = trasf+" "+prod+" "+consum+" "+admin+" "+tx_receipt['contractAddress']
#account_state=open("account.bin",'wb')
#cont_state=open("contractAddress.bin",'wb')
abi_state=open("abi.bin",'wb')
address_state=open("address.bin",'wb')
#pickle.dump(tx_receipt['contractAddress'],cont_state)
pickle.dump(abi,abi_state)
pickle.dump(address,address_state)
#pickle.dump(account,account_state)
