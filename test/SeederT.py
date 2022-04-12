import string
import sys
from warnings import catch_warnings
from web3 import exceptions

sys.path.insert(0, 'C:/Users/pc/Desktop/Università/SoftwareCyberSecurity/Solidity/src')

import contract as contratto

# Classe usata per eseguire i test sul trasformatore

class Seeder_trasformatore:

    contratto.current_user = contratto.trasf
    contratto.w3.geth.personal.unlock_account(contratto.account[0], 'trasformatore')
    __prodotto01: int
    __prodotto02: int
    __prodotto03: int
    __acquisto01: int
    __acquisto02: int
    __acquisto03: int
    __acquisto04: int

    # Qui vengono chiamati i metodi del contratto che andranno a valorizzare gli attributi della classe

    def __init__(self,prod01,prod02,prod03,listaP,listaQ,singleP,singleQ):
        try:
            self.__acquisto01 = contratto.acquista_MP('materia010',5)
        except exceptions.SolidityError as error:
            self.__acquisto01 = 0

        try:
            self.__acquisto02 = contratto.acquista_MP('materia021',5)
        except exceptions.SolidityError as error:
            self.__acquisto02 =0

        try:
            self.__acquisto03 = contratto.acquista_MP('materia032',5)
        except exceptions.SolidityError as error:
            self.__acquisto03 =0

        try:
            self.__acquisto04 = contratto.acquista_MP('materia043',5) # input non valido, verrà generata un'eccezione 
        except exceptions.SolidityError as error:
            self.__acquisto04 =0

        try:
            self.__prodotto01 = contratto.inserisci_Prod(prod01, listaP,listaQ,5,5)
        except exceptions.SolidityError as error:
            self.__prodotto01 = 0

        try:
            self.__prodotto02 = contratto.inserisci_Prod(prod02, singleP,singleQ,5,5)
        except exceptions.SolidityError as error:
            self.__prodotto02 = 0
            
        try:
            singleQ[0] = 100
            self.__prodotto03 = contratto.inserisci_Prod(prod03, singleP,singleQ,10,5)  # input non valido, verrà generata un'eccezione 
        except exceptions.SolidityError as error:
            self.__prodotto03 = 0

    def getAcquisto01(self):
        return self.__acquisto01

    def getAcquisto02(self):
        return self.__acquisto02

    def getAcquisto03(self):
        return self.__acquisto03

    def getAcquisto04(self):
        return self.__acquisto04

    def getProdotto01(self):
        return self.__prodotto01

    def getProdotto02(self):
        return self.__prodotto02
    
    def getProdotto03(self):
        return self.__prodotto03