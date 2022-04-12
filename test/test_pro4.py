import unittest
from SeederC import Seeder_consumatore

# In questa classe andiamo a creare una istanza del consumatore, chiamando i metodi GET possiamo verificare se le chiamate
# allo smart contract sono andate a buon fine

class Test_seederC(unittest.TestCase):

    def testSeederC(self):
        seederC = Seeder_consumatore('prodotto010','prodotto021',2)
        self.assertEquals(seederC.getAcquisto01(),1)
        self.assertEquals(seederC.getAcquisto02(),0)