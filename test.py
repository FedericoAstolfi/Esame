import unittest
import main_torte
import random

POSSIBILITA = [ format(i, "04b") for i in range(0,16)]

class TestMain_Torte(unittest.TestCase):

    """def setUp(self):
        print('before')

    def tearDown(self):
        print('after')"""

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
    
    def test_crossover(self):
        
        """test del crossover 1/4 + 3/4"""
        #genero due dict casualmente {i : random.randint(0, 4) for i in POSSIBILITA}
        dict1  = {'0000': 4, '0001': 2, '0010': 1, '0011': 1, '0100': 2, '0101': 4, '0110': 0, '0111': 4, '1000': 2, '1001': 4, '1010': 0, '1011': 4, '1100': 4, '1101': 4, '1110': 1, '1111': 0}
        dict2 = {'0000': 3, '0001': 4, '0010': 1, '0011': 3, '0100': 0, '0101': 0, '0110': 3, '0111': 4, '1000': 1, '1001': 4, '1010': 3, '1011': 2, '1100': 2, '1101': 1, '1110': 1, '1111': 2}
        hand_made = {'0000': 4, '0001': 2, '0010': 1, '0011': 1, '0100': 0, '0101': 0, '0110': 3, '0111': 4, '1000': 1, '1001': 4, '1010': 3, '1011': 2, '1100': 2, '1101': 1, '1110': 1, '1111': 2}
        self.assertEqual(hand_made, main_torte.crossover(dict1, dict2))
    
    def test_roulette_sampling(self):
        #genero una lista di tre creature di cui due con energia nulla e controllo che mi estragga il terzo
        lista = [main_torte.Creature(),main_torte.Creature(), main_torte.Creature()]
        #metto l'energia a 0 dei primi due, poi provo anche mettendo molto alta la prima aspettandomi che il test fallisca
        lista[0].energia = 0
        lista[1].energia = 0
        fit = [c.energia for c in lista]
        self.assertEqual(lista[2], main_torte.roulette_sampling(lista, fit))
    
    """def test_mate(self):
        #genero due dict casualmente {i : random.randint(0, 4) for i in POSSIBILITA}
        dict1 = {'0000': 0, '0001': 0, '0010': 2, '0011': 1, '0100': 4, '0101': 2, '0110': 0, '0111': 2, '1000': 1, '1001': 1, '1010': 0, '1011': 2, '1100': 2, '1101': 2, '1110': 3, '1111': 1}
        dict2 = {'0000': 3, '0001': 0, '0010': 3, '0011': 0, '0100': 2, '0101': 3, '0110': 1, '0111': 2, '1000': 4, '1001': 4, '1010': 0, '1011': 2, '1100': 3, '1101': 2, '1110': 1, '1111': 2}
        c1 = main_torte.Creature(dict1)
        c2 = main_torte.Creature(dict2)
        #controllo di aver costruito bene le creature:
        self.assertEqual(dict1, c1.mosse)
        self.assertEqual(dict2, c2.mosse)
        dic_figlio = {'0000': 0, '0001': 0, '0010': 2, '0011': 1, '0100': 2, '0101': 3, '0110': 1, '0111': 2, '1000': 4, '1001': 4, '1010': 0, '1011': 2, '1100': 3, '1101': 2, '1110': 1, '1111': 2}
        figlio = main_torte.Creature(dic_figlio, 2, 2)
        ris = c1.mate(c2)
        ris.x= 2
        ris.y= 2
        self.assertEqual(figlio, ris)"""        



if __name__ == '__main__':
    unittest.main()

