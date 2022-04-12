import sys
from web3 import exceptions

sys.path.insert(0, 'C:/Users/pc/Desktop/Università/SoftwareCyberSecurity/Solidity/src')

import contract as contratto

# Classe usata per eseguire i test sul produttore

class Seeder_produttore:

    contratto.current_user = contratto.prod
    contratto.w3.geth.personal.unlock_account(contratto.account[1], 'produttore')
    __materiaPrima01: int
    __materiaPrima02: int
    __materiaPrima03: int
    __materiaPrima04: int
    __materiaPrima05: int

    # Qui vengono chiamati i metodi del contratto che andranno a valorizzare gli attributi della classe

    def __init__(self,mat01,mat02,mat03,mat04,mat05):
        try:
            self.__materiaPrima01 = contratto.inserisci_MP(mat01,20,3)
        except exceptions.SolidityError as error:
            self.__materiaPrima01 =0
        try:
            self.__materiaPrima02 = contratto.inserisci_MP(mat02,25,4)
        except exceptions.SolidityError as error:
            self.__materiaPrima02 =0
        try:
            self.__materiaPrima03 = contratto.inserisci_MP(mat03,30,2)
        except exceptions.SolidityError as error:
            self.__materiaPrima03 =0
        try:
            self.__materiaPrima04 = contratto.inserisci_MP(mat04,8,0) # input non valido, verrà generata un'eccezione 
        except exceptions.SolidityError as error:
            self.__materiaPrima04 =0
        try:
            self.__materiaPrima05 = contratto.inserisci_MP(mat05,10,1)
        except exceptions.SolidityError as error:
            self.__materiaPrima05 =0


    def getMateria01(self):
        return self.__materiaPrima01

    def getMateria02(self):
        return self.__materiaPrima02

    def getMateria03(self):
        return self.__materiaPrima03

    def getMateria04(self):
        return self.__materiaPrima04

    def getMateria05(self):
        return self.__materiaPrima05

