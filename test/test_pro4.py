import unittest
from SeederC import Seeder_consumatore

class Test_seederC(unittest.TestCase):

    def testSeederC(self):
        seederC = Seeder_consumatore('prodotto010','prodotto021',2)
        self.assertEquals(seederC.getAcquisto01(),1)
        self.assertEquals(seederC.getAcquisto02(),0)