
import unittest
import sys

sys.path.insert(0, 'C:/Users/pc/Desktop/Università/SoftwareCyberSecurity/Solidity/src')
import contract as contratto

class Test_info(unittest.TestCase):

    def testInfoAllMP(self):
        contratto.current_user = contratto.trasf
        contratto.w3.geth.personal.unlock_account(contratto.account[0], 'trasformatore')
        lista = contratto.tutti_MP_lotti()
        self.assertEquals(len(lista),4)

    def testInfoMP(self):
        contratto.current_user = contratto.trasf
        contratto.w3.geth.personal.unlock_account(contratto.account[0], 'trasformatore')
        materia = contratto.info_MP_prod('materia021')[4]
        self.assertEquals(materia,20)

    def testInfoMPAcquistata(self):
        contratto.current_user = contratto.trasf
        contratto.w3.geth.personal.unlock_account(contratto.account[0], 'trasformatore')
        materia_acquistata = contratto.info_MP_acq('materia010')[2]
        self.assertEquals(materia_acquistata,1)

    def testInfoLottiMP(self):
        contratto.current_user = contratto.trasf
        contratto.w3.geth.personal.unlock_account(contratto.account[0], 'trasformatore')
        lista = contratto.lotti_MP('materia01')
        res = list(filter(None, lista))
        self.assertEquals(len(res),1)