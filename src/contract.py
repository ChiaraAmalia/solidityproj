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

cons = os.path.join(path,'abi_consum.bin')
trasf = os.path.join(path,'abi_trasf.bin')
prod = os.path.join(path,'abi_prod.bin')
state = os.path.join(path,'address.bin')

#vengono aperti in lettura i vari file
abi_state_cons=open(cons,'rb')
abi_state_trasf=open(trasf,'rb')
abi_state_prod=open(prod,'rb')
address_state=open(state,'rb')


#leggendo dai file vengono valorizzati i seguenti oggetti
abi_cons=pickle.load(abi_state_cons)
abi_trasf=pickle.load(abi_state_trasf)
abi_prod=pickle.load(abi_state_prod)
address_string=pickle.load(address_state)

#viene creato l'array contenente gli indirizzi
account=address_string[0:4]
deploy_address_cons=address_string[4]
deploy_address_trasf=address_string[5]
deploy_address_prod=address_string[6]

#Ci si connette alla blockchain
w3 = Web3(web3.HTTPProvider("http://127.0.0.1:22000"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.middleware_onion.add(web3.middleware.http_retry_request_middleware)

trasf=account[0]
prod=account[1]
consum=account[2]
admin=account[3]

#vengono istanziati i vari Smart Contract
consumatore=w3.eth.contract(address=deploy_address_cons,abi=abi_cons)
trasformatore=w3.eth.contract(address=deploy_address_trasf,abi=abi_trasf)
produttore=w3.eth.contract(address=deploy_address_prod,abi=abi_prod)

#Viene impostato un utente di default
current_user = '0x00000000000000000000000000000'


#Si "mappano" le diverse funzioni degli Smart Contract:

#Funzione per l'inserimento di una materia prima
def inserisci_MP(nomeMP,quantMP,footprint):
    tx_hash = produttore.functions.aggiungiMateriaPrima(nomeMP, quantMP, footprint).transact({'from': current_user})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])
    return(tx_receipt['status'])

#Funzione per l'acquisto di una materia prima
def acquista_MP(lottoMP,quantMP):
    print(current_user)
    tx_hash = produttore.functions.acquistaMateriaPrima(lottoMP,quantMP).transact({'from': current_user})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])
    return(tx_receipt['status'])

#Funzione per l'inserimento di un prodotto finito
def inserisci_Prod(nomeP,listaLottiMP,listaQuantMP,quantP,footprint):
    tx_hash =produttore.functions.aggiungiProdotto(nomeP,listaLottiMP,listaQuantMP, quantP, footprint).transact({'from': current_user})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])
    return(tx_receipt['status'])

#Funzione per l'acquisto di un prodotto finito
def acquista_Prod(lottoP,quantP):
    tx_hash =trasformatore.functions.acquistaProdotto(lottoP,quantP).transact({'from': current_user})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt['status'])
    return(tx_receipt['status'])

#Funzione per vedere il footprint di un prodotto finito
def footprint_Prod(lottoP):
    return trasformatore.functions.vediFootprintProdottoFinito(lottoP).call({'from': current_user})

#Funzione per vedere tutti i lotti di un prodotto finito, conoscendo il suo nome
def lotti_Prod(nomeP):
    return trasformatore.functions.vediLottiProdotto(nomeP).call({'from': current_user})

#Funzione per vedere tutti i lotti di tutti i prodotti finiti
def tutti_Prod_lotti():
    return trasformatore.functions.vediTuttiLottiProdotti().call({'from': current_user})

#Funzione per vedere tutti i lotti di una materia prima, conoscendo il suo nome
def lotti_MP(nomeMP):
    return produttore.functions.vediLottiMateriaPrima(nomeMP).call({'from': current_user})

#Funzione per vedere tutti i lotti di tutte le materie prime
def tutti_MP_lotti():
    return produttore.functions.vediTuttiLottiMateriePrime().call({'from': current_user})

#Funzione per vedere tutte le informazioni di un prodotto finito
def info_Prod_trasf(lottoP):
    return trasformatore.functions.StampaInforProdTrasf(lottoP).call({'from': current_user})

#Funzione per vedere tutte le informazioni di una materia prima
def info_MP_prod(lottoMP):
    return produttore.functions.StampaInforMatPrProd(lottoMP).call({'from': current_user})

#Funzione per vedere tutte le informazioni di una materia prima acquistata
def info_MP_acq(lottoMP):
    return trasformatore.functions.StampaMatPrAcq(lottoMP).call({'from': current_user})

#Funzione per vedere tutte le informazioni di un prodotto finito acquistato
def info_Prod_acq(lottoP):
    return consumatore.functions.StampaInforProdCons(lottoP).call({'from': current_user})












