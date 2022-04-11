import unittest
from SeederP import Seeder_produttore



class Test_seederP(unittest.TestCase):

    def testSeederP(self):
        seeder = Seeder_produttore('materia01','materia02','materia03','materia04','materia05')
        self.assertEquals(seeder.getMateria01(),1)
        self.assertEquals(seeder.getMateria02(),1)
        self.assertEquals(seeder.getMateria03(),1)
        self.assertEquals(seeder.getMateria04(),0)
        self.assertEquals(seeder.getMateria05(),1)
