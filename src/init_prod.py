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
import init_trasf

install_solc(version='latest')

def compile_source_file(file_path):
    with open(file_path, 'r') as f:
        source = f.read()

        return compile_source(source, output_values=['abi', 'bin'])

path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
data_path = os.path.join(path,'Produttore.sol') #viene preso il file magazzino.sol dalla cartella in cui si trovale il file .py in esecuzione
compiled_sol = compile_source_file(data_path)

# prende il bytecode/bin
bytecode = compiled_sol['<stdin>:Magazzino']['bin']

# prende l'abi
abi = compiled_sol['<stdin>:Magazzino']['abi']

# crea un istanza di web3.py
w3=init_trasf.init.w3

Produttore = w3.eth.contract(abi=abi, bytecode=bytecode)

# Invia la transazione che fa il deploy del contratto
account=init_trasf.init.address[0:4]
trasf=account[0]
prod=account[1]
consum=account[2]
admin=account[3]
consumC=init_trasf.init.address[4]
trasfC=init_trasf.init.address[5]

tx_hash = Produttore.constructor(prod,trasfC).transact({'from': admin})
#Aspetta che la transazione avvenga e prende la ricevuta della transazione
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

produttore = w3.eth.contract(
    address=tx_receipt['contractAddress'],
    abi=abi
)

init_trasf.init.address.append(tx_receipt['contractAddress'])
address=init_trasf.init.address

abi_state=open("abi_prod.bin",'wb')
address_state=open("address.bin",'wb')

pickle.dump(abi,abi_state)
pickle.dump(address,address_state)
init_trasf.init.w3.geth.personal.lock_account(account[0])
init_trasf.init.w3.geth.personal.lock_account(account[1])
init_trasf.init.w3.geth.personal.lock_account(account[2])

print("")
print("Fatto: 3/3")
print("Il contratto del produttore è pronto!")
print("Finito!\nOra puoi eseguire il programma!")
print("Per farlo basta scrivere:\npython \path\\to\\file\main.py")