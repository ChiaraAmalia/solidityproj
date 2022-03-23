import time
from unittest import result

import os

import requests
import web3
from web3 import Web3, geth
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
w3.middleware_onion.add(web3.middleware.http_retry_request_middleware)

#accountProd = w3.eth.account.create()
#accountTrasf = w3.eth.account.create()
#accountCons = w3.eth.account.create()

#print(Web3.toChecksumAddress(w3.eth.accounts[0])+" è l'amministratore del nodo")
#print(Web3.toChecksumAddress(accountProd.address)+" è il produttore")
#print(Web3.toChecksumAddress(accountTrasf.address)+" è il trasformatore")
#print(Web3.toChecksumAddress(accountCons.address)+" è il consumatore")

if len(w3.eth.accounts)<4:
    w3.geth.personal.new_account('trasformatore')
    w3.geth.personal.new_account('produttore')
    w3.geth.personal.new_account(('consumatore'))

print(w3.geth.personal.list_accounts())


print(Web3.toChecksumAddress(w3.eth.accounts[0])+" è il trasformatore")
#w3.geth.personal.unlock_account(w3.eth.accounts[0],'trasformatore')
print(Web3.toChecksumAddress(w3.eth.accounts[1])+" è il produttore")
#w3.geth.personal.unlock_account(w3.eth.accounts[1],'produttore')
print(Web3.toChecksumAddress(w3.eth.accounts[2])+" è il consumatore")


MagazzinoProdotti = w3.eth.contract(abi=abi, bytecode=bytecode)

# Invia la transazione che fa il deploy del contratto
#admin=Web3.toChecksumAddress(w3.eth.accounts[0])
#prod=Web3.toChecksumAddress(accountProd.address)
#trasf=Web3.toChecksumAddress(accountTrasf.address)
#consum=Web3.toChecksumAddress(accountCons.address)
trasf=Web3.toChecksumAddress(w3.eth.accounts[0])
prod=Web3.toChecksumAddress(w3.eth.accounts[1])
consum=Web3.toChecksumAddress(w3.eth.accounts[2])
admin=Web3.toChecksumAddress(w3.eth.accounts[3])
#tx_hash = MagazzinoProdotti.constructor(prod, trasf, consum).transact({'from': admin})
tx_hash = MagazzinoProdotti.constructor(prod, trasf, consum).transact({'from': admin})
#Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

magazzino = w3.eth.contract(
    address=tx_receipt['contractAddress'],
    abi=abi
)

current_user = '0x00000000000000000000000000000'

def inserisci_MP(nomeMP,quantMP,footprint):
    tx_hash = magazzino.functions.aggiungiMateriaPrima(nomeMP, quantMP, footprint).transact({'from': current_user})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])

def acquista_MP(lottoMP,quantMP):
    print(current_user)
    tx_hash = magazzino.functions.acquistaMateriaPrima(lottoMP,quantMP).transact({'from': current_user})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])

def inserisci_Prod(nomeP,listaLottiMP,listaQuantMP,quantP,footprint):
    magazzino.functions.aggiungiProdotto(nomeP,listaLottiMP,listaQuantMP, quantP, footprint).transact({'from': current_user})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])

def acquista_Prod(lottoP,quantP):
    magazzino.functions.acquistaProdotto(lottoP,quantP).transact({'from': current_user})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])

def footprint_Prod(lottoP):
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])
    return magazzino.functions.vediFootprintProdottoFinito(lottoP).call({'from': current_user})

def lotti_Prod(nomeP):
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])
    return magazzino.functions.vediLottiProdotto(nomeP).call({'from': current_user})

def tutti_Prod_lotti():
    return magazzino.functions.vediTuttiLottiProdotti().call({'from': current_user})

def lotti_MP(nomeMP):
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])
    return magazzino.functions.vediLottiMateriaPrima(nomeMP).call({'from': current_user})

def tutti_MP_lotti():
    return magazzino.functions.vediTuttiLottiMateriePrime().call({'from': current_user})

def info_Prod_trasf(lottoP):
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])
    return magazzino.functions.StampaInforProdTrasf(lottoP).call({'from': current_user})

def info_MP_prod(lottoMP):
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])
    return magazzino.functions.StampaInforMatPrProd(lottoMP).call({'from': current_user})

def info_MP_acq(lottoMP):
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])
    return magazzino.functions.StampaMatPrAcq(lottoMP).call({'from': current_user})

def info_Prod_acq(lottoP):
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])
    return magazzino.functions.StampaInforProdCons(lottoP).call({'from': current_user})

def handle_event(event):
    receipt = w3.eth.waitForTransactionReceipt(event['transactionHash'])
    print(result[0]['args'])

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(poll_interval)










