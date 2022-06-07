# Esame di Algoritmi Genetici

import random
from numpy import NaN
import argparse
import numpy as np

NTORTE = 10
ENERGIA = 10
NGRIGLIA = 10
NMOSSE = 5
'''come in self.mosse, ad esempio, 0101 significa: dx torta, su niente, sx torta, giù niente'''
POSSIBILITA = [ format(i, "04b") for i in range(0,16)]

class Creature():

    def __init__(self, dizionario = None, x=None, y=None, energia = ENERGIA  ):
        ''' se non do niente genera delle mosse e delle posizioni casualmente con energia quella iniziale (e anche massima) '''
        if dizionario: #gli ho dato qualche dizionario
            self.mosse = dizionario
        else: #genero casualmente
            self.mosse = {i : random.randint(0, 4) for i in POSSIBILITA} #0 è destra, 1 su, 2 sinistra, 3 giù

        if x==None & y==None: 
            self.x=random.randint(0,NGRIGLIA)
            self.y=random.randint(0,NGRIGLIA)
        else:
            self.x=x
            self.y=y
        
        self.energia = energia


class Ambiente(list):

    '''creo ambiente come figlia della classe list, infatti voglio che sia una matrice. quindi non uso __init__ 
    ma posso porre definire direttamente self come una matrice. prima la definisco come piena di zeri, poi ci metto
    degli 1 in posizioni a caso. la condizione sul ciclo è che finchè la sommma di tutti gli elementi non è NTORTE, ovvero
    fino a quando non ci sono NTORTE 1, il ciclo continua.
    definendo ambiente già come lista non c'è bisogno di nessun metodo che acceda agli 0 e 1 della matrice, visto che
    basta fare ambiente[i][j]'''

    self = [[0 for i in range(0,NGRIGLIA)] for n in range(0,NGRIGLIA)]

    while np.sum(self)<NTORTE:
        self[random.randint(0,NTORTE-1)][random.randint(0,NTORTE-1)]=1
        #randint prende estremo dx incluso

def movimento(creatura, ambiente):

    '''il metodo movimento prende in input la creatura e l'ambiente in cui essa
    si sta muovendo e non returna nulla, ma modifica la posizione e l'energia della
    creatura ed eventualmente rimuove una torta (si potrebbe chiamare moveat)'''

    x=creatura.x
    y=creatura.y
    
    #chiave_list contiene gli elementi limitrofi in ambiente alla posizione che occupa creatura
    chiave_list = [ambiente[x+1%10][y], ambiente[x][y+1%10], ambiente[x-1%10][y], ambiente[x][y-1%10]]
    #però a me serve come stringa per accedere agli elementi del dizionario
    chiave = "".join([str(item) for item in chiave_list])

    mossa = creatura.mosse[chiave]

    #ora facciamo spostare la creatura a seconda di quello che ha codificato nel genoma

    if mossa == 0:
        creatura.x = x+1%10
    elif mossa == 1:
        creatura.y = y+1%10
    elif mossa == 2:
        creatura.x = x-1%10
    elif mossa == 3:
        creatura.y = y-1%10

    #ora che la creatura si è spostata, vediamo di fare le modifiche opportune:

    x_new = creatura.x
    y_new = creatura.y

    #togliamo o lasciamo invariata l'energia e togliamo eventualmente le torte:

    if ambiente[x_new][y_new] == 0:
        creatura.energia -=1
        #non modifico ambiente
    else:
        #non modifico energia
        ambiente[x_new][y_new] = 0



'''COMMENTI PER AVERE UN'IDEA DI COSA FARE
-creo la prima generazione di creature
-creo il primo ambiente
-faccio muovere le creature (come? creo tipo un metodo move() ?)
-definisco qualcosa che rimuove gli 1 delle torte quando una creatura ci passa
-definisco qualcosa che a ogni mossa toglie 1 di energia oppure non toglie nulla alla creatura
- '''
    

# PROGRAMMA PRINCIPALE

if __name__=='__main__':

    parser = argparse.ArgumentParser(description = "Istinto di sopravvivenza con algoritmi genetici")
    parser.add_argument('popsize', help= "Numero di creature", type=int)
    parser.add_argument('mut_prob', help= "Probabilità di mutazione", type=float)
    parser.add_argument('ngen', help= "Numero di generazioni", type=int)
    parser.add_argument('--no_plots', help="does not show plots", default=False, action='store_true')
    args = parser.parse_args()

    print(args)

    npop = args.popsize
    mut_prob = args.mut_prob
    ngen = args.ngen

    creature = [Creature() for i in range(npop)]
    ambiente = Ambiente()


        