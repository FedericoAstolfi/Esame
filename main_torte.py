# Esame di Algoritmi Genetici

import numpy as np
import random
from numpy import NaN
import argparse
import copy
import matplotlib.pyplot as plt


NTORTE = 10
ENERGIA = 10
NGRIGLIA = 10
NMOSSE = 10
'''come in self.mosse, ad esempio, 0101 significa: dx niente, su torta, sx niente, giu torta'''
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

    def mate(self, other, mut_prob):
        """genera un figlio con dizionario dato da un crossover dei dizionari genitori e con posizioni casuali"""
        mosse_figlio = crossover(self.mosse, other.mosse)

        """implemento le mutazioni casuali: con probabilità mut_prob un gene del figlio viene cambiato casualmente
        con distribuzione uniforme tra le 4 possibilità"""
        rn = random.random()        #genero numero casuale
        if rn < mut_prob:
            gene = random.choice(list(mosse_figlio.keys())) #estraggo il gene da modificare
            gene_value = mosse_figlio[gene]                 #la mossa corrispondente al gene
            #non voglio mutare il gene con la stessa mossa:
            r = list(range(0,4))
            r.remove(gene_value)
            mosse_figlio[gene] = random.choice(r)

        return Creature(mosse_figlio)         



'''facciamo che per ora lascio stare la classe ambiente, ma al suo posto uso una semplice
matrice che mi definisco a mano ogni volta nel main: non dovrebbe essere troppo una sbatta'''

class Ambiente(list):

    '''creo ambiente come figlia della classe list, infatti voglio che sia una matrice. quindi non uso __init__ 
    ma posso porre definire direttamente self come una matrice. prima la definisco come piena di zeri, poi ci metto
    degli 1 in posizioni a caso. la condizione sul ciclo è che finchè la sommma di tutti gli elementi non è NTORTE, ovvero
    fino a quando non ci sono NTORTE 1, il ciclo continua.
    definendo ambiente già come lista non c'è bisogno di nessun metodo che acceda agli 0 e 1 della matrice, visto che
    basta fare ambiente[i][j]'''

    def __init__():

        self = [[0 for i in range(0, NGRIGLIA)] for n in range(0, NGRIGLIA)]

        while np.sum(self)<NTORTE:
            self[random.randint(0, NTORTE-1)][random.randint(0, NTORTE-1)]=1
            #randint prende estremo dx incluso

def movimento(creatura, ambiente):

    '''il metodo movimento prende in input la creatura e l'ambiente in cui essa
    si sta muovendo e non returna nulla, ma modifica la posizione e l'energia della
    creatura ed eventualmente rimuove una torta (si potrebbe chiamare moveat)'''
    if creatura.energia > 0: #controllo che abbia energia per muoversi

        x=creatura.x #riga in cui sta creatura
        y=creatura.y #colonna in cui creatura
        
        #chiave_list contiene gli elementi limitrofi in ambiente alla posizione che occupa creatura
        #cerco di fare gli spostamenti nel sistema di coordinate della matrice
        chiave_list = [ambiente[x][(y+1)%10], ambiente[(x-1)%10][y], ambiente[x][(y-1)%10], ambiente[(x+1)%10][y]]
        #però a me serve come stringa per accedere agli elementi del dizionario
        chiave = "".join([str(item) for item in chiave_list])

        mossa = creatura.mosse[chiave]

        #ora facciamo spostare la creatura a seconda di quello che ha codificato nel genoma

        if mossa == 0:
            creatura.y = (y+1)%10
        elif mossa == 1:
            creatura.x = (x-1)%10
        elif mossa == 2:
            creatura.y = (y-1)%10
        elif mossa == 3:
            creatura.x = (x+1)%10

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

def get_offsprings(parents): #lista di creature e prob di mutazione
    '''rimpiazzo tutte le creature con i figli di queste, cioè npop nuove creature.
        le creature figlie hanno come energia la media delle energie dei genitori arrotondata per eccesso.
        nel caso in cui tutte le creature abbiano energia 0, la popolazione si estingue:  lo segnalo.
        siccome c'è la possibilità che rimanga solo un genitore con energia non nulla, contemplo la possibilità
        di mating tra una creatura con sè stessa '''
     
    #estraggo i fitness:
    fit = [creat.energia for creat in parents]
    maxi = max(fit)
    
    #controllo se c'è ancora vita:
    if sum(fit) == 0:
        print("La popolazione si è estinta\n")
        quit()
    
    

    off_springs = []
    #se è rimasto solo un genitore devo accettare che si riproduca con sè stesso, cosa che altrimenti evito
    if fit.count(0) == npop -1:
        off_springs = [parents[fit.index(maxi)] for i in range(0, npop)]
    
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
    
def plot_creature(popolazione, ambiente):
    
    '''
    -come lo zaro ha fatto in gencolors, mi sembrava sensato usare un metodo che si occupasse dei plot
    -chiamo questo metodo dopo che ho creato fig, ax = plt.subplot(), che in sostanza è una lista di grafici.
    la prima azione che fa è pulire la lista, altrimenti ogni volta che la creatura fa una mossa, nel plot rimane 
    anche il percorso che ha fatto.
    -i pallini sono le torte e le x le creature
    -quello che inizia a fare è creare delle liste con ascisse e ordinate delle torte per poi plottarle (QUESTO LO FA GIUSTO, PERO' 
    NOTA CHE HO SOSTITUITO LA ORDINATA DELLE TORTE CON (NGRIGLIA - ORDINATA) PERCHE' ALTRIMENTI TUTTA LA PRIMA RIGA DELLA 
    MATRICE (CHE IN AMBIENTE DOVREBBE ESSERE MESSA AL LIVELLO DI ORDINATA 9) VERRREBBE MESSA AL LIVELLO DI ORDINATA 0, LA SECONDA RIGA
    VERREBBE MESSA AL LIVELLO 1 INVECE CHE ALL'8 E COSI VIA...)
    -
    '''

    ax.clear()

    torta_x = []
    torta_y = []
    for i in range(NGRIGLIA):
        for j in range(NGRIGLIA):
            if ambiente[i][j] == 1:
                '''scambio le coordinate perchè la prima mi dà la riga e la seconda la colonna
                quindi la prima mi dà l'ordinata e la seconda l'ascissa
                inoltre devo stare attento perchè gli elementi in teoria sono distribuiti così:
                [0][0] [0][1] [0][2]
                [1][0] [1][1] [1][2]
                [2][0] [2][1] [2][2]'''

                torta_x += [j]
                torta_y += [NGRIGLIA -1 - i]

    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 9.5)
    my_ticks = range(10) #crea degli sticker che sotto appiccico sull'asse delle x e delle y
    plt.xticks(my_ticks)
    plt.yticks(my_ticks)
    '''sta boomerata degli sticker l'ho fatta perchè altrimenti python è stupido e mi mette il reticolo della griglia 
    a  0 2 4 6 8, mentre io voglio che mi metta una linea per ogni numero 0 1 2 3 4 5 ...
    se non mi sono spiegato prova a commentare momentaneamente myticks e plt.xtricks plt.yticks'''
    ax.scatter(torta_x, torta_y, color = 'b') #plotto i punti con scatter
    plt.grid(linewidth=0.5, color = 'g', linestyle = '--') #tiro su una griglia 

    for i in range(len(popolazione)): #printo tutte le creature, che vengono messe nella loro posizione iniziale giusta
        ax.scatter(popolazione[i].y, NGRIGLIA -1 - popolazione[i].x, color = 'y', edgecolor = 'r', marker = 'o', s = 200)
        
    


    



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

    fig, ax = plt.subplots() #creo la mia lista di plot

    #creo la prima e unica popolazione casuale
    creature = [Creature() for i in range(npop)] 

    for n in range(ngen): 

        #creo un ambiente random:
        ambiente = [[0 for i in range(0, NGRIGLIA)] for n in range(0, NGRIGLIA)]
        while np.sum(ambiente)<NTORTE:
            ambiente[random.randint(0, NGRIGLIA-1)][random.randint(0, NGRIGLIA-1)]=1

        """ci assicuriamo di dare +1 energia alle creature spawnate su una torta"""
        #ciclo sulle creature e controllo se nelle coord c'è un 1 nella griglia ambiente
        for c in creature:
            if ambiente[c.x][c.y] == 1 :
                c.energia += 1      #incremento energia del fortunato
                ambiente[c.x][c.y] = 0  # tolgo la torta dall'ambiente

        plot_creature(creature, ambiente)
        plt.title(f' generazione numero {n+1}')

        for i in range(NMOSSE): #faccio muovere le creature della stessa generazione
            
            for c in creature:

                movimento(c, ambiente)

            plt.pause(1) #questo aspetta un secondo prima di visualizzare lo step successivo nel grafico

            plt.draw() #questo aggiorna il grafico con i nuovi dati di creatura e ambiente che sono stati modificati da movimento

            plot_creature(creature, ambiente)
            plt.title(f' generazione numero {n+1}')

        '''generazione successiva:'''
        fantoccio = get_offsprings(creature)
        creature = fantoccio

    '''abbiamo ngen generazioni, con la prima indicizzata dallo 0 e l'ultima indicizzata da ngen-1'''

    

    plt.show()


        
'''dobbiamo ricordarci di assicurarci che le creature non possano avere energia negativa'''

'''DOBBIAMO CAMBIARE UNA COSA IMPORTANTE: NELLA CHIAVE DELLE MOSSE
DELLA CREATURA NON ABBIAMO TENUTO CONTO CHE IN UNA MATRICE, SE PRENDO
[I][J], ALLORA I INDICA L'ORDINATA E J L'ASCISSA. NE HO TENUTO CONTO PER
PLOTTRE LE TORTE E LA POSIZIONE INIZIALE DELLA CREATURA, MA NEL METODO 
MOVIMENTO NON NE AVEVO TENUTO CONTO, QUINDI PER VEDERE COSA C'è AD ESEMPIO
A DX DELLA CREATURA DEVO GUARDARE L'ELEMENTO [I][J+1], NON IL [I+1][J]
IN MODO SIMILE RAGIONIAMO SUL FATTO CHE HO 'RIBALTATO' LE COORDINATE DELLA 
MATRICE PER METTERLA BENE ALL'INTERNO DEL GRAFICO E CHE QUINDI FORSE DOBBIAMO
RIBALTARE ANCHE I MOVIMENTI SU E GIU DELLA CREATURA'''