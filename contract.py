import time
from unittest import result
import pickle
import os
import requests
import web3
from web3 import Web3, geth

from web3.middleware import geth_poa_middleware
abi_state=open("abi.bin",'rb')
#address_state=open("contractAddress.bin",'rb')
#account_state=open("account.bin",'rb')
address_state=open("address.bin",'rb')

abi=pickle.load(abi_state)
#deploy_address=pickle.load(address_state)
#account_string=pickle.load(account_state)
address_string=pickle.load(address_state)

#account=account_string.split()
account=(address_string.split())[0:4]
deploy_address=(address_string.split())[4]


w3 = Web3(web3.HTTPProvider("http://127.0.0.1:22000"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.middleware_onion.add(web3.middleware.http_retry_request_middleware)

trasf=account[0]
prod=account[1]
consum=account[2]
admin=account[3]

magazzino=w3.eth.contract(address=deploy_address,abi=abi)
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
    tx_hash =magazzino.functions.aggiungiProdotto(nomeP,listaLottiMP,listaQuantMP, quantP, footprint).transact({'from': current_user})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])

def acquista_Prod(lottoP,quantP):
    tx_hash =magazzino.functions.acquistaProdotto(lottoP,quantP).transact({'from': current_user})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])

def footprint_Prod(lottoP):
    #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print(tx_receipt['status'])
    return magazzino.functions.vediFootprintProdottoFinito(lottoP).call({'from': current_user})

def lotti_Prod(nomeP):
    #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print(tx_receipt['status'])
    return magazzino.functions.vediLottiProdotto(nomeP).call({'from': current_user})

def tutti_Prod_lotti():
    return magazzino.functions.vediTuttiLottiProdotti().call({'from': current_user})

def lotti_MP(nomeMP):
    #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print(tx_receipt['status'])
    return magazzino.functions.vediLottiMateriaPrima(nomeMP).call({'from': current_user})

def tutti_MP_lotti():
    return magazzino.functions.vediTuttiLottiMateriePrime().call({'from': current_user})

def info_Prod_trasf(lottoP):
    #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print(tx_receipt['status'])
    return magazzino.functions.StampaInforProdTrasf(lottoP).call({'from': current_user})

def info_MP_prod(lottoMP):
    #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print(tx_receipt['status'])
    return magazzino.functions.StampaInforMatPrProd(lottoMP).call({'from': current_user})

def info_MP_acq(lottoMP):
    #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print(tx_receipt['status'])
    return magazzino.functions.StampaMatPrAcq(lottoMP).call({'from': current_user})

def info_Prod_acq(lottoP):
    #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print(tx_receipt['status'])
    return magazzino.functions.StampaInforProdCons(lottoP).call({'from': current_user})












