import sys
from web3 import exceptions

sys.path.insert(0, 'C:/Users/pc/Desktop/Università/SoftwareCyberSecurity/Solidity/src')

import contract as contratto

class Seeder_consumatore:

    contratto.current_user = contratto.consum
    contratto.w3.geth.personal.unlock_account(contratto.account[2], 'consumatore')
    __acquisto01: int
    __acquisto02: int

    def __init__(self,prod01,prod02,quan01):
        try:
            self.__acquisto01 = contratto.acquista_Prod(prod01,quan01)
        except exceptions.SolidityError as error:
            self.__acquisto01 = 0
        try:
            self.__acquisto02 = contratto.acquista_Prod(prod02,100)
        except exceptions.SolidityError as error:
            self.__acquisto02 = 0

    def getAcquisto01(self):
        return self.__acquisto01

    def getAcquisto02(self):
        return self.__acquisto02