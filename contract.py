from unittest import result

import os
import web3
from web3 import Web3
from solcx import compile_source, install_solc
from web3.middleware import geth_poa_middleware

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
print(Web3.toChecksumAddress(w3.eth.accounts[0])+" è il produttore")
print(Web3.toChecksumAddress(Web3(web3.HTTPProvider("http://127.0.0.1:22001")).eth.accounts[0])+" è il trasformatore")
print(Web3.toChecksumAddress(Web3(web3.HTTPProvider("http://127.0.0.1:22002")).eth.accounts[0])+" è il consumatore")


MagazzinoProdotti = w3.eth.contract(abi=abi, bytecode=bytecode)

# Invia la transazione che fa il deploy del contratto
prod=Web3.toChecksumAddress(w3.eth.accounts[0])
trasf=Web3.toChecksumAddress(Web3(web3.HTTPProvider("http://127.0.0.1:22001")).eth.accounts[0])
consum=Web3.toChecksumAddress(Web3(web3.HTTPProvider("http://127.0.0.1:22002")).eth.accounts[0])
tx_hash = MagazzinoProdotti.constructor(trasf, prod, consum).transact({'from': prod})

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

magazzino = w3.eth.contract(
    address=tx_receipt['contractAddress'],
    abi=abi
)

def inserisci_MP(nomeMP,quantMP,footprint):
    magazzino.functions.aggiungiMP(nomeMP, quantMP, footprint).transact({'from': prod})

def elenco_MP_nome(nome):
    elencoMAT=[]
    TotMP = int(magazzino.functions.numeroMatPrim().call())
    for i in range(TotMP):
        elencoMAT.append(magazzino.functions.vediMPNome(nome,i).call())
    print(elencoMAT)
    print(TotMP)

def inserisci_Prod(nomeP,quantP,footprint):
    magazzino.functions.aggiungiProd(nomeP, quantP, footprint).transact({'from': trasf})

def elenco_Prod_nome(nome):
    elencoPROD=[]
    TotProd = int(magazzino.functions.numeroProd().call())
    for i in range(TotProd):
        elencoPROD.append(magazzino.functions.vediProdNome(nome,i).call())
    print(elencoPROD)
    print(TotProd)
#print(magazzino.functions.prova().call())

nomeMP = input("Inserisci il nome della materia prima: ")
quantMP = int(input("Inserisci la quantità della materia prima: "))
fpMP = int(input("Inserisci il footprint della materia prima: "))



magazzino.functions.aggiungiMP(nomeMP,quantMP,fpMP).transact({'from': prod})
magazzino.functions.aggiungiMP(nomeMP,quantMP,fpMP).transact({'from': prod})
magazzino.functions.aggiungiMP(nomeMP,quantMP,fpMP).transact({'from': prod})
magazzino.functions.aggiungiMP(nomeMP,quantMP,fpMP).transact({'from': prod})


#print(str(magazzino.functions.vediMPNome(nomeMP).call()))

elenco_MP_nome(nomeMP)






