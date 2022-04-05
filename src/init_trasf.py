import os
from solcx import compile_source, install_solc
import pickle
import init

install_solc(version='latest')


def compile_source_file(file_path):
    with open(file_path, 'r') as f:
        source = f.read()

        return compile_source(source, output_values=['abi', 'bin'])

path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
data_path = os.path.join(path,'Trasformatore.sol') #viene preso il file magazzino.sol dalla cartella in cui si trovale il file .py in esecuzione
compiled_sol = compile_source_file(data_path)

# prende il bytecode/bin
bytecode = compiled_sol['<stdin>:Trasformatore']['bin']

# prende l'abi
abi = compiled_sol['<stdin>:Trasformatore']['abi']

# crea un istanza di web3.py
w3=init.w3

Trasformatore = w3.eth.contract(abi=abi, bytecode=bytecode)

# Invia la transazione che fa il deploy del contratto
account=init.address[0:4]
trasf=account[0]
prod=account[1]
consum=account[2]
admin=account[3]
consumC=init.address[4]

tx_hash = Trasformatore.constructor(trasf,consumC).transact({'from': admin})
#Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

trasformatore = w3.eth.contract(
    address=tx_receipt['contractAddress'],
    abi=abi
)
print("codice per il trasformatore\n")
print(w3.eth.getCode(tx_receipt['contractAddress']).hex())
print('ABI:')
for el in trasformatore.abi:
    print(el)
#account = trasf+" "+prod+" "+consum+" "+admin
#address = address_string+" "+tx_receipt['contractAddress']
init.address.append(tx_receipt['contractAddress'])
#account_state=open("account.bin",'wb')
#cont_state=open("contractAddress.bin",'wb')
abi_state=open("abi_trasf.bin",'wb')
#address_state=open("address.bin",'wb')
#pickle.dump(tx_receipt['contractAddress'],cont_state)
pickle.dump(abi,abi_state)
#pickle.dump(address,address_state)
#pickle.dump(account,account_state)