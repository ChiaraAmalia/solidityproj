import time
from unittest import result
import pickle
import os
import requests
import web3
from web3 import Web3, geth

from web3.middleware import geth_poa_middleware
path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
#data_path = os.path.join(path,'Consumatore.sol') #viene preso il file magazzino.sol dalla cartella in cui si trovale il file .py in esecuzione
cons = os.path.join(path,'abi_consum.bin')
trasf = os.path.join(path,'abi_trasf.bin')
prod = os.path.join(path,'abi_prod.bin')
state = os.path.join(path,'address.bin')
abi_state_cons=open(cons,'rb')
abi_state_trasf=open(trasf,'rb')
abi_state_prod=open(prod,'rb')
address_state=open(state,'rb')

#abi_state_cons=open("abi_consum.bin",'rb')
#abi_state_trasf=open("abi_trasf.bin",'rb')
#abi_state_prod=open("abi_prod.bin",'rb')
#address_state=open("contractAddress.bin",'rb')
#account_state=open("account.bin",'rb')
#address_state=open("address.bin",'rb')

abi_cons=pickle.load(abi_state_cons)
abi_trasf=pickle.load(abi_state_trasf)
abi_prod=pickle.load(abi_state_prod)
#deploy_address=pickle.load(address_state)
#account_string=pickle.load(account_state)
address_string=pickle.load(address_state)

#account=account_string.split()
account=address_string[0:4]
deploy_address_cons=address_string[4]
deploy_address_trasf=address_string[5]
deploy_address_prod=address_string[6]


w3 = Web3(web3.HTTPProvider("http://127.0.0.1:22000"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.middleware_onion.add(web3.middleware.http_retry_request_middleware)

trasf=account[0]
prod=account[1]
consum=account[2]
admin=account[3]

consumatore=w3.eth.contract(address=deploy_address_cons,abi=abi_cons)
trasformatore=w3.eth.contract(address=deploy_address_trasf,abi=abi_trasf)
produttore=w3.eth.contract(address=deploy_address_prod,abi=abi_prod)

current_user = '0x00000000000000000000000000000'

def inserisci_MP(nomeMP,quantMP,footprint):
    tx_hash = produttore.functions.aggiungiMateriaPrima(nomeMP, quantMP, footprint).transact({'from': current_user})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])
    return(tx_receipt['status'])

def acquista_MP(lottoMP,quantMP):
    print(current_user)
    tx_hash = produttore.functions.acquistaMateriaPrima(lottoMP,quantMP).transact({'from': current_user})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])

def inserisci_Prod(nomeP,listaLottiMP,listaQuantMP,quantP,footprint):
    tx_hash =produttore.functions.aggiungiProdotto(nomeP,listaLottiMP,listaQuantMP, quantP, footprint).transact({'from': current_user})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])

def acquista_Prod(lottoP,quantP):
    tx_hash =trasformatore.functions.acquistaProdotto(lottoP,quantP).transact({'from': current_user})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])

def footprint_Prod(lottoP):
    #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print(tx_receipt['status'])
    return trasformatore.functions.vediFootprintProdottoFinito(lottoP).call({'from': current_user})

def lotti_Prod(nomeP):
    #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print(tx_receipt['status'])
    return trasformatore.functions.vediLottiProdotto(nomeP).call({'from': current_user})

def tutti_Prod_lotti():
    return trasformatore.functions.vediTuttiLottiProdotti().call({'from': current_user})

def lotti_MP(nomeMP):
    #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print(tx_receipt['status'])
    return produttore.functions.vediLottiMateriaPrima(nomeMP).call({'from': current_user})

def tutti_MP_lotti():
    return produttore.functions.vediTuttiLottiMateriePrime().call({'from': current_user})

def info_Prod_trasf(lottoP):
    #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print(tx_receipt['status'])
    return trasformatore.functions.StampaInforProdTrasf(lottoP).call({'from': current_user})

def info_MP_prod(lottoMP):
    #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print(tx_receipt['status'])
    return produttore.functions.StampaInforMatPrProd(lottoMP).call({'from': current_user})

def info_MP_acq(lottoMP):
    #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print(tx_receipt['status'])
    return trasformatore.functions.StampaMatPrAcq(lottoMP).call({'from': current_user})

def info_Prod_acq(lottoP):
    #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print(tx_receipt['status'])
    return consumatore.functions.StampaInforProdCons(lottoP).call({'from': current_user})












