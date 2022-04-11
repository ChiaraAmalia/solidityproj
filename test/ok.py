from SeederP import Seeder_produttore
from SeederT import Seeder_trasformatore
from SeederC import Seeder_consumatore
import sys

sys.path.insert(0, 'C:/Users/pc/Desktop/Università/SoftwareCyberSecurity/Solidity/src')
import contract as contratto

class ok:

    contratto.current_user = contratto.trasf
    contratto.w3.geth.personal.unlock_account(contratto.account[0], 'trasformatore')
    materia_acquistata = contratto.info_MP_acq('materia010')[2]
    print(materia_acquistata)
    '''seeder = Seeder_produttore('materia01','materia02','materia03','materia04','materia05')
    print("ciao simone")
    print(seeder.getMateria01())'''

    '''listaP = ['materia010','materia021']
    listaQ = [1,1]
    singleP = ['materia032']
    singleQ = [1]
    seederT = Seeder_trasformatore('prodotto01','prodotto02','prodotto03',listaP,listaQ,singleP,singleQ)
    print('sono il prodotto 1 '+str(seederT.getProdotto01()))
    print('sono il prodotto 2 '+str(seederT.getProdotto02()))
    print('sono il prodotto 3 '+str(seederT.getProdotto03()))'''