import unittest
from SeederT import Seeder_trasformatore

# In questa classe andiamo a creare una istanza del trasformatore, chiamando i metodi GET possiamo verificare se le chiamate
# allo smart contract sono andate a buon fine

class Test_seederT(unittest.TestCase):

    def testSeederT(self):
        listaP = ['materia010','materia021']
        listaQ = [4,5]
        singleP = ['materia032']
        singleQ = [5]
        seederT = Seeder_trasformatore('prodotto01','prodotto02','prodotto03',listaP,listaQ,singleP,singleQ)
        self.assertEquals(seederT.getAcquisto01(),1)
        self.assertEquals(seederT.getAcquisto02(),1)
        self.assertEquals(seederT.getAcquisto03(),1)
        self.assertEquals(seederT.getAcquisto04(),0)
        self.assertEquals(seederT.getProdotto01(),1)
        self.assertEquals(seederT.getProdotto02(),1)
        self.assertEquals(seederT.getProdotto03(),0)
        
