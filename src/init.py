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
data_path = os.path.join(path,'Consumatore.sol') #viene preso il file magazzino.sol dalla cartella in cui si trovale il file .py in esecuzione
compiled_sol = compile_source_file(data_path)

# recupera l'interfaccia del contratto
contract_id, contract_interface = compiled_sol.popitem()

# prende il bytecode/bin
bytecode = contract_interface['bin']

# prende l'abi
abi = contract_interface['abi']
print("\n")
print("  ______          _   _____      _       _       ".center(101))
print(" |  ____|        | | |  __ \    (_)     | |      ".center(101,'*'))
print(" | |__ ___   ___ | |_| |__) | __ _ _ __ | |_     ".center(101,'*'))
print(" |  __/ _ \ / _ \| __|  ___/ '__| | '_ \| __|    ".center(101,'*'))
print(" | | | (_) | (_) | |_| |   | |  | | | | | |_     ".center(101,'*'))
print(" |_|__\___/ \___/ \__|_|   |_|  |_|_| |_|\__|    ".center(101,'*'))
print("  / ____|    | |          | |     | |            ".center(101,'*'))
print(" | |     __ _| | ___ _   _| | __ _| |_ ___  _ __ ".center(101,'*'))
print(" | |    / _` | |/ __| | | | |/ _` | __/ _ \| '__|".center(101,'*'))
print(" | |___| (_| | | (__| |_| | | (_| | || (_) | |   ".center(101,'*'))
print("  \_____\__,_|_|\___|\__,_|_|\__,_|\__\___/|_|   ".center(101,'*'))
print("\n")
print("Ti chiediamo un attimo di pazienza, il nostro programma sta effettuando il deploy dei contratti")


# crea un istanza di web3.py
w3 = Web3(web3.HTTPProvider("http://127.0.0.1:22000"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.middleware_onion.add(web3.middleware.http_retry_request_middleware)

print(Web3.toChecksumAddress(w3.eth.accounts[0])+" è il consumatore")
print(Web3.toChecksumAddress(w3.eth.accounts[1])+" è il produttore")
print(Web3.toChecksumAddress(w3.eth.accounts[2])+" è il trasformatore")

print("Sto lavorando...")

#Esegue il deploy dello Smart Contract riguardante il consumatore
Consumatore = w3.eth.contract(abi=abi, bytecode=bytecode)

# Invia la transazione che fa il deploy del contratto
consum=Web3.toChecksumAddress(w3.eth.accounts[0])
w3.geth.personal.unlock_account(w3.eth.accounts[0], 'consumatore')
prod=Web3.toChecksumAddress(w3.eth.accounts[1])
w3.geth.personal.unlock_account(w3.eth.accounts[1], 'produttore')
trasf=Web3.toChecksumAddress(w3.eth.accounts[2])
w3.geth.personal.unlock_account(w3.eth.accounts[2], 'trasformatore')
admin=Web3.toChecksumAddress(w3.eth.accounts[3])
w3.geth.personal.unlock_account(w3.eth.accounts[3], '')

tx_hash = Consumatore.constructor(consum).transact({'from': admin})
#Aspetta che la transazione avvenga e prende la ricevuta della transazione
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

consumatore = w3.eth.contract(
    address=tx_receipt['contractAddress'],
    abi=abi
)

address=[trasf,prod,consum,admin, tx_receipt['contractAddress']]

abi_state=open("abi_consum.bin",'wb')

pickle.dump(abi,abi_state)
print("")
print("Fatto: 1/3")
print("Il contratto del consumatore è pronto!")
