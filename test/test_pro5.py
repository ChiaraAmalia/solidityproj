
import unittest
import sys

sys.path.insert(0, 'C:/Users/pc/Desktop/Università/SoftwareCyberSecurity/Solidity/src')
import contract as contratto

# In questa classe andiamo a chiamare direttamente i metodi dello smart contract, in questo caso non facciamo
# operazioni di inserimento o acquisto, ma andiamo a controllare tutti i metodi che restituiscono delle informazioni
#  sullo stato dello smart contract

class Test_info2(unittest.TestCase):

    def testInfoAllP(self):
        contratto.current_user = contratto.consum
        contratto.w3.geth.personal.unlock_account(contratto.account[2], 'consumatore')
        lista = contratto.tutti_Prod_lotti()
        self.assertEquals(len(lista),2)

    def testInfoP(self):
        contratto.current_user = contratto.consum
        contratto.w3.geth.personal.unlock_account(contratto.account[2], 'consumatore')
        prodotto = contratto.info_Prod_trasf('prodotto021')[5]
        self.assertEquals(prodotto,5)

    def testInfoPAcquistato(self):
        contratto.current_user = contratto.consum
        contratto.w3.geth.personal.unlock_account(contratto.account[2], 'consumatore')
        materia_acquistata = contratto.info_Prod_acq('prodotto010')[2]
        self.assertEquals(materia_acquistata,2)

    def testInfoLottiP(self):
        contratto.current_user = contratto.consum
        contratto.w3.geth.personal.unlock_account(contratto.account[2], 'consumatore')
        lista = contratto.lotti_Prod('prodotto01')
        res = list(filter(None, lista))
        self.assertEquals(len(res),1)

    def testInfoCarbonFootPrint(self):
        contratto.current_user = contratto.consum
        contratto.w3.geth.personal.unlock_account(contratto.account[2], 'consumatore')
        valore = contratto.footprint_Prod('prodotto010').split(' ')
        self.assertEquals(valore[-1],'12')