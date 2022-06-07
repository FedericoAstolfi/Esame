import unittest
import main_torte

POSSIBILITA = [ format(i, "04b") for i in range(0,16)]

class TestMain_Torte(unittest.TestCase):

    def setUp(self):
        print('before')

    def tearDown(self):
        print('after')

    def test_movimento(self):

        '''cerchiamo di testare in più step tutte le cose che fa movimento'''

        #creo una matrice che faccia da ambiente

        griglia = [[0 for i in range(0,10)] for n in range(0,10)]

        #metto una torta nella posizione (5,9):

        griglia[5][9]=1

        #creiamo una creatura

        diz = {i : 1 for i in POSSIBILITA} #la creatura va sempre su (0dx 1 su 2 sx 3giu)
        creatura = main_torte.Creature(dizionario = diz, x = 5, y = 8)

        '''facciamola muovere: dovremmo star lasciando invariata l'energia, cambiando l'ambiente 
        e la posizione della creatura'''

        main_torte.movimento(creatura, griglia)

        #verifichiamo che si sia spostata

        self.assertEqual([5,9], [creatura.x, creatura.y])

        #verifichiamo che l'energia sia invariata

        self.assertEqual(10, creatura.energia)

        #verifichiamo che non ci sia più la torta

        self.assertEqual(griglia[5][9], 0)

        '''ho verificato che con questi parametri tutto funziona, proviamo ora a fare spostare
        ancora una volta la creatura: visto che griglia contiene tutti zeri ( e quindi nessuna torta ),
        la creatura dovrebbe perdere un punto energia spostandosi al punto '''

        main_torte.movimento(creatura, griglia)

        self.assertEqual([5,0], [creatura.x, creatura.y])

        self.assertEqual(9, creatura.energia)

        self.assertEqual(griglia[5][0], 0)

        '''anche questo funziona, DA PENSARE SE PUO' AVERE SENSO FARE DEI TEST PIU' MIRATI'''



if __name__ == '__main__':
    unittest.main()

