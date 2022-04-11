import sys
import unittest

sys.path.insert(0, 'C:/Users/pc/Desktop/Università/SoftwareCyberSecurity/Solidity/src')

import contract as contratto

class Test_info(unittest.TestCase):

    def AllInfoMP(self):
        contratto.current_user = contratto.trasf
        lista = contratto.tutti_MP_lotti()
        self.assertEquals(len(lista),5)

    

    