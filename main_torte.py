# Esame di Algoritmi Genetici

from ctypes import create_unicode_buffer
import numpy as np
import random
from numpy import NaN
import argparse
import copy


NTORTE = 10
ENERGIA = 10
NGRIGLIA = 10
NMOSSE = 5
'''come in self.mosse, ad esempio, 0101 significa: dx torta, su niente, sx torta, giù nientee'''
POSSIBILITA = [ format(i, "04b") for i in range(0,16)]

class Creature():

    def __init__(self, dizionario = None, x=None, y=None, energia = ENERGIA  ):
        ''' se non do niente genera delle mosse e delle posizioni casualmente con energia quella iniziale (e anche massima) '''
        if dizionario: #gli ho dato qualche dizionario
            self.mosse = dizionario
        else: #genero casualmente
            self.mosse = {i : random.randint(0, 3) for i in POSSIBILITA} #0 è destra, 1 su, 2 sinistra, 3 giù

        if not x: 
            self.x=random.randint(0,NGRIGLIA-1)
            self.y=random.randint(0,NGRIGLIA-1)
        else:
            self.x=x
            self.y=y
        
        self.energia = energia

    def mate(self, other):
        """genera un figlio con dizionario dato da un crossover dei dizionari genitori e con posizioni casuali"""
        mosse_figlio = crossover(self.mosse, other.mosse)
        return Creature(mosse_figlio)


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
    if creatura.energia > 0: #controllo che abbia energia per muoversi

        x=creatura.x
        y=creatura.y
        
        #chiave_list contiene gli elementi limitrofi in ambiente alla posizione che occupa creatura
        chiave_list = [ambiente[(x+1)%10][y], ambiente[x][(y+1)%10], ambiente[(x-1)%10][y], ambiente[x][(y-1)%10]]
        #però a me serve come stringa per accedere agli elementi del dizionario
        chiave = "".join([str(item) for item in chiave_list])

        mossa = creatura.mosse[chiave]

        #ora facciamo spostare la creatura a seconda di quello che ha codificato nel genoma

        if mossa == 0:
            creatura.x = (x+1)%10
        elif mossa == 1:
            creatura.y = (y+1)%10
        elif mossa == 2:
            creatura.x = (x-1)%10
        elif mossa == 3:
            creatura.y = (y-1)%10

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


def crossover(dict1, dict2):
    """ ad una creatura per essere buona basta quasi solo andare verso una torta quando ce n'è una,
        per questo motivo ogni crossover va bene, perchè non distruggono mai 
        l'associazione "se c'è una torta --> ci vado".
        tuttavia una creatura adatta è anche una creatura che esplora più mappa possibile, cioè torna con bassa
        probabilità dove è appena stata, per esempio una creatura che va prevalentemente in due direzioni (e va 
        sulle torte quando ci sono) è migliore di una creatura che quando ci sono più torte si mangia una di queste
        ma nelle varie combinzioni multitorta usa tutte le direzioni.
        per questo motivo prendo un quarto del genoma di un genitore e 3/4 dell'altro. Ripeto: 
        questo perchè se una creatura è buona vuol dire che: va verso le torte quando ci sono (e questo viene
        mantenuto dalla scelta del crossover) e tende a usare 2 direzioni invece di 4 (con questo crossover
        rischio meno di trovarmi con le quattro direzioni ben mischiate) """
    dict_a = { i : dict1[i] for i in POSSIBILITA[0:4] } #il primo quarto da dict1
    dict_b= { i : dict2[i] for i in POSSIBILITA[4:16] } #il resto da dict2

    return {**dict_a,**dict_b}  # accosto i due dictionary e restituisco il risultato


def roulette_sampling(list,fit): #lista di creature e lista di fit corrispondenti
    '''associamo virtualmente all'elemento i-esimo della list la probabilità i-esima di prob'''
    prob=copy.copy(fit)
    prob=prob/np.sum(prob)
    cum=np.cumsum(prob)
    cum=cum.tolist()
    rn=random.random()
    for i in cum:
        if rn<i:
            risultato = list[cum.index(i)]
            return risultato

def get_offsprings(parents, mut_prob): #lista di creature e prob di mutazione
    '''rimpiazzo tutte le creature con i figli di queste, cioè npop nuove creature.
        le creature figlie hanno come energia la media delle energie dei genitori arrotondata per eccesso.
        nel caso in cui tutte le creature abbiano energia 0, la popolazione si estingue:  lo segnalo.
        siccome c'è la possibilità che rimanga solo un genitore con energia non nulla, contemplo la possibilità
        di mating tra una creatura con sè stessa '''
     
    #estraggo i fitness:
    fit = [creat.energia for creat in parents]
    max = max(fit)
    
    #controllo se c'è ancora vita:
    if fit.sum == 0:
        print("La popolazione si è estinta\n")
        quit()
    
    

    off_springs = []
    #se è rimasto solo un genitore devo accettare che si riproduca con sè stesso, cosa che altrimenti evito
    if fit.count(0) == npop -1:
        off_springs = [parents[fit.index(max)] for i in range(0, npop)]
    
    else:
        for i in range(npop):
            
            parent1 = roulette_sampling(parents, fit)
            parent2 = roulette_sampling(parents,fit)
            if parent1.mosse != parent2.mosse:    #se ho preso due parenti diversi li tengo e accoppio
                off_springs.append(parent1.mate(parent2))
            else:           #altrimenti continuo finchè non sono diversi
                while parent1.mosse == parent2.mosse:
                    parent1 = roulette_sampling(parents, fit)
                off_springs.append(parent1.mate(parent2))
            
    return off_springs

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

    creature = [Creature() for i in range(npop)]  #creo prima popolazione con mosse e coord random
    ambiente = Ambiente()                          #creo un ambiente random

    print(ambiente)

    """ci assicuriamo di dare +1 energia alle creature spawnate su una torta"""
    #ciclo sulle creature e controllo se nelle coord c'è un 1 nella griglia ambiente
    for c in creature:
        print(c.x, c.y)
        """if ambiente[c.x][c.y] == 1 :
            c.energia += 1      #incremento energia del fortunato
            ambiente[c.x][c.y] = 0  # tolgo la torta dall'ambiente"""
    
    for i in range(NMOSSE):
        for c in creature:
            movimento(c, ambiente)

   


        
