
from unittest import result
import os
import requests
import web3
from pkg_resources import require
from web3 import Web3, geth, exceptions
import json as JSON
from web3.middleware import geth_poa_middleware

w3 = Web3(web3.HTTPProvider("http://127.0.0.1:22000"))
#use the existing Member1 account address or make a new account
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.middleware_onion.add(web3.middleware.http_retry_request_middleware)


if len(w3.eth.accounts) == 1:
    w3.geth.personal.new_account('trasformatore')
    w3.geth.personal.new_account('produttore')
    w3.geth.personal.new_account(('consumatore'))

#-----------------STAMPE INUTILI-------------------------------------
print(w3.geth.personal.list_accounts())
print(Web3.toChecksumAddress(w3.eth.accounts[0])+" è il trasformatore")
print(Web3.toChecksumAddress(w3.eth.accounts[1])+" è il produttore")
print(Web3.toChecksumAddress(w3.eth.accounts[2])+" è il consumatore")
#--------------------------------------------------------------------
trasf=Web3.toChecksumAddress(w3.eth.accounts[0])
w3.geth.personal.unlock_account(w3.eth.accounts[0], 'trasformatore')
prod=Web3.toChecksumAddress(w3.eth.accounts[1])
w3.geth.personal.unlock_account(w3.eth.accounts[1], 'produttore')
consum=Web3.toChecksumAddress(w3.eth.accounts[2])
w3.geth.personal.unlock_account(w3.eth.accounts[2], 'consumatore')
admin=Web3.toChecksumAddress(w3.eth.accounts[3])

fs = require('fs-extra')
path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
contractJsonPath = os.path.join(path,'Consumatore.json')

contractJson = JSON.parse(fs.readFileSync(contractJsonPath))
contractAbi = contractJson.abi
contractByteCode = contractJson.evm.bytecode.object

async def createContract(host, contractAbi, contractByteCode, contractInit, fromAddress):
    w3 = Web3(web3.HTTPProvider("http://127.0.0.1:22000"))
    contractInstance = w3.eth.Contract(contractAbi);
    ci = await contractInstance.deploy(data='0x'+contractByteCode, arguments= [contractInit]).send_transaction({ 'from': fromAddress, 'gasLimit': "0x24A22" }).on('transactionHash', print("The transaction hash is: " + hash))
    return ci


# create the contract
createContract("http://localhost:20000", contractAbi, contractByteCode, 47, admin)
