import time
from unittest import result

import os
from eth_utils import to_dict
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
tx_hash = MagazzinoProdotti.constructor(prod, trasf, consum).transact({'from': prod})

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

magazzino = w3.eth.contract(
    address=tx_receipt['contractAddress'],
    abi=abi
)


def inserisci_MP(nomeMP,quantMP,footprint):
    magazzino.functions.aggiungiMateriaPrima(nomeMP, quantMP, footprint).transact({'from': prod})

def acquista_MP(lottoMP,quantMP):
    magazzino.functions.acquistaMateriaPrima(lottoMP,quantMP).transact({'from': trasf})

def inserisci_Prod(nomeP,listaLottiMP,listaQuantMP,quantP,footprint):
    magazzino.functions.aggiungiProdotto(nomeP,listaLottiMP,listaQuantMP, quantP, footprint).transact({'from': trasf})

def acquista_Prod(lottoP,quantP):
    magazzino.functions.acquistaProdotto(lottoP,quantP).transact({'from': consum})

def footprint_Prod(lottoP):
    return magazzino.functions.vediFootprintProdottoFinito(lottoP).call()

def lotti_Prod(nomeP):
    return magazzino.functions.vediLottiProdotto(nomeP).call()

def tutti_Prod_lotti():
    return magazzino.functions.vediTuttiLottiProdotti().call()

def lotti_MP(nomeMP):
    return magazzino.functions.vediLottiMateriaPrima(nomeMP).call()

def tutti_MP_lotti():
    return magazzino.functions.vediTuttiLottiMateriePrime().call()

def info_Prod_trasf(lottoP):
    return magazzino.functions.StampaInforProdTrasf(lottoP).call()

def info_MP_prod(lottoMP):
    return magazzino.functions.StampaInforMatPrProd(lottoMP).call()

def info_MP_acq(lottoMP):
    return magazzino.functions.StampaMatPrAcq(lottoMP).call()

def info_Prod_acq(lottoP):
    return magazzino.functions.StampaInforProdCons(lottoP).call()

def handle_event(event):
    receipt = w3.eth.waitForTransactionReceipt(event['transactionHash'])
    print(result[0]['args'])

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(poll_interval)









