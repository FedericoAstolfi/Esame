# Esame di Algoritmi Genetici

from matplotlib import image
import numpy as np
import random
from numpy import NaN
import argparse
import copy
import matplotlib.pyplot as plt
import itertools

SIMBOLI = [2, 0, 1]     #rappresenteranno: prensenza di veleno, nulla, presenza di torta

#al posto di mettere un parametro in più nel main, lo metto qui manualmente
SWITCH_VELENO = True                #!!!!!!!!! interruttore !!!!!!!!!!!!!!!!

if SWITCH_VELENO:
    LEN_GENOMA = 3**4
    POSSIBILITA = ["".join([str(value) for value in p]) for p in itertools.product(SIMBOLI, repeat=4)]
else:
    LEN_GENOMA = 2**4
    POSSIBILITA = [format(i, "04b") for i in range(0,16)]

CUT_CRSS = int(LEN_GENOMA/2) #tengo il taglio in mezzo per non dimenticarmi (se taglio al 4 in un genoma da 81 probabilmente non avrò conv)
NTORTE = 60
NVELENO = 60
ENERGIA = 10
NGRIGLIA = 15
NMOSSE = 5

'''come in self.mosse, ad esempio, 0101 significa: dx niente, su torta, sx niente, giu torta'''

 




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
        con distribuzione uniforme tra le 3 possibilità rimanenti"""
        rn = random.random()        #genero numero casuale
        if rn < mut_prob:
            gene = random.choice(list(mosse_figlio.keys())) #estraggo il gene da modificare
            gene_value = mosse_figlio[gene]                 #la mossa corrispondente al gene
            #non voglio mutare il gene con la stessa mossa:
            r = list(range(0,4))
            r.remove(gene_value)
            mosse_figlio[gene] = random.choice(r)
        
        c = Creature(mosse_figlio)
        #arrotondo per eccesso l'energia del figlio
        a = round(((self.energia + other.energia)*0.5)+0.1)  # vista la natura del problema aggiungere 0.1 mi assicura di arrotondare per eccesso
        c.energia = int(a)  #converto in int per sicurezza
        return c    


def movimento(creatura, ambiente):

    '''il metodo movimento prende in input la creatura e l'ambiente in cui essa
    si sta muovendo e non returna nulla, ma modifica la posizione e l'energia della
    creatura ed eventualmente rimuove una torta (si potrebbe chiamare moveat)'''
    if creatura.energia > 0: #controllo che abbia energia per muoversi

        x=creatura.x #riga in cui sta creatura
        y=creatura.y #colonna in cui creatura
        
        #chiave_list contiene gli elementi limitrofi in ambiente alla posizione che occupa creatura
        #cerco di fare gli spostamenti nel sistema di coordinate della matrice
        chiave_list = [ambiente[x][(y+1)%NGRIGLIA], ambiente[(x-1)%NGRIGLIA][y], ambiente[x][(y-1)%NGRIGLIA], ambiente[(x+1)%NGRIGLIA][y]]
        #però a me serve come stringa per accedere agli elementi del dizionario
        chiave = "".join([str(item) for item in chiave_list])

        mossa = creatura.mosse[chiave]

        #ora facciamo spostare la creatura a seconda di quello che ha codificato nel genoma

        if mossa == 0:
            creatura.y = (y+1)%NGRIGLIA
        elif mossa == 1:
            creatura.x = (x-1)%NGRIGLIA
        elif mossa == 2:
            creatura.y = (y-1)%NGRIGLIA
        elif mossa == 3:
            creatura.x = (x+1)%NGRIGLIA

        #ora che la creatura si è spostata, vediamo di fare le modifiche opportune:

        x_new = creatura.x
        y_new = creatura.y

        #togliamo o lasciamo invariata l'energia e togliamo eventualmente le torte e veleni:

        if ambiente[x_new][y_new] == 0:
            creatura.energia -= 1
            #non modifico ambiente

        elif ambiente[x_new][y_new] == 1:
            #non modifico energia
            #creatura.energia +=1
            ambiente[x_new][y_new] = 0

        elif ambiente[x_new][y_new] == 2: #veleno
            if creatura.energia == 1:
                creatura.energia = 0  #questo per evitare che si abbia energia -1
                ambiente[x_new][y_new] = 0
            else:
                creatura.energia -= 2
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
    dict_a = { i : dict1[i] for i in POSSIBILITA[0:CUT_CRSS] } #il primo quarto da dict1
    dict_b= { i : dict2[i] for i in POSSIBILITA[CUT_CRSS: LEN_GENOMA] } #il resto da dict2

    return {**dict_a,**dict_b}  # accosto i due dictionary e restituisco il risultato


def roulette_sampling(list,fit): #lista di creature e lista di fit corrispondenti
    '''associamo virtualmente all'elemento i-esimo della list la probabilità i-esima di prob'''
    if sum(fit) != 0:
        prob = copy.copy(fit)
        massa = sum(prob)
        proba = [ i / massa for i in prob]
        cum=np.cumsum(proba)
        cum=cum.tolist()
        rn=random.random()
        for i in cum:
            if rn<i:
                risultato = list[cum.index(i)]
                return risultato
    else:
        print("i fit sono tutti zero")

#scritte gestisce i print, di default è True
#NON CONTROLLA che parents sia tutto nullo, lo facciamo nel main
def get_offsprings(parents, npop, mut_prob, scritte): #lista di creature e prob di mutazione
    '''rimpiazzo tutte le creature con i figli di queste, cioè npop nuove creature.
        le creature figlie hanno come energia la media delle energie dei genitori arrotondata per eccesso.
        nel caso in cui tutte le creature abbiano energia 0, la popolazione si estingue:  lo segnalo.
        siccome c'è la possibilità che rimanga solo un genitore con energia non nulla, contemplo la possibilità
        di mating tra una creatura con sè stessa '''
     
    #estraggo i fitness:
    fit = [creat.energia for creat in parents]
    #fit = [greed(creat.mosse) for creat in parents]
    maxi = max(fit)
    
    off_springs = []
    #se è rimasto solo un genitore devo accettare che si riproduca con sè stesso, cosa che altrimenti evito
    if fit.count(0) == npop -1:
        off_springs = [parents[fit.index(maxi)] for i in range(0, npop)]
    
    else:
        for i in range(npop):
            
            parent1 = roulette_sampling(parents, fit)
            parent2 = roulette_sampling(parents,fit)
            if parent1.mosse != parent2.mosse:    #se ho preso due parenti diversi li tengo e accoppio
                off_springs.append(parent1.mate(parent2, mut_prob))

            else:           #altrimenti continuo finchè non sono diversi DA VALUTARE QUESTO WHILE

                '''l'idea è che possiamo usare un contatore da aggiungere come condizione del while
                affinchè non vada avanti all'infinito:'''
                contatore = 0
                while parent1.mosse == parent2.mosse and parent1.x == parent2.x and parent1.y == parent2.y and contatore <=100:
                    parent1 = roulette_sampling(parents, fit)
                    contatore += 1
                    #print("qui") #questo while viene ripetuto molte volte in alcune situazioni (per esempio se rimangono solo due creature, una con energia 1 e l'altra con energia 0.0001)

                '''se a questo punto sono uscito dal while solo a causa del contatore, allora mi riproduco con lo stesso elemento'''    
                off_springs.append(parent1.mate(parent2, mut_prob))
            
    return off_springs

'''COMMENTI PER AVERE UN'IDEA DI COSA FARE
-creo la prima generazione di creature
-creo il primo ambiente
-faccio muovere le creature (come? creo tipo un metodo move() ?)
-definisco qualcosa che rimuove gli 1 delle torte quando una creatura ci passa
-definisco qualcosa che a ogni mossa toglie 1 di energia oppure non toglie nulla alla creatura
- '''
    
def plot_creature(popolazione, ambiente, ax):
    
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

    #coordinate sulla matrice delle torte
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
    
    veleno_x = []
    veleno_y = []
    for i in range(NGRIGLIA):
        for j in range(NGRIGLIA):
            if ambiente[i][j] == 2:
                '''scambio le coordinate perchè la prima mi dà la riga e la seconda la colonna
                quindi la prima mi dà l'ordinata e la seconda l'ascissa
                inoltre devo stare attento perchè gli elementi in teoria sono distribuiti così:
                [0][0] [0][1] [0][2]
                [1][0] [1][1] [1][2]
                [2][0] [2][1] [2][2]'''

                veleno_x += [j]
                veleno_y += [NGRIGLIA -1 - i]

    ax.set_xlim(-0.5, NGRIGLIA)
    ax.set_ylim(-0.5, NGRIGLIA )
    my_ticks = range(NGRIGLIA) #crea degli sticker che sotto appiccico sull'asse delle x e delle y
    plt.xticks(my_ticks)
    plt.yticks(my_ticks)
    '''sta boomerata degli sticker l'ho fatta perchè altrimenti python è stupido e mi mette il reticolo della griglia 
    a  0 2 4 6 8, mentre io voglio che mi metta una linea per ogni numero 0 1 2 3 4 5 ...
    se non mi sono spiegato prova a commentare momentaneamente myticks e plt.xtricks plt.yticks'''
    ax.scatter(torta_x, torta_y, color = 'b') #plotto i punti con scatter
    ax.scatter(veleno_x, veleno_y, color = 'r', marker = 'x') #plotto i punti con scatter
    plt.grid(linewidth=0.5, color = 'g', linestyle = '--') #tiro su una griglia 

    for i in range(len(popolazione)): #printo tutte le creature, che vengono messe nella loro posizione iniziale giusta
        ax.scatter(popolazione[i].y, NGRIGLIA -1 - popolazione[i].x, color = 'y', edgecolor = 'r', marker = 'o', s = 200)
        

            
def greed(dict):
    """dato il dizionario di una creatura conta in quante delle 15 (o 65 con il veleno) possibilità essa vada su una torta quando c'è"""
    count = 0
    chiavi = list(dict.keys())
    for k in chiavi: #scorro sulle chiavi
        for i in range(0,4): #scorro sui 4 bit
            if int(k[i]) == 1 and dict[k] == i:
                count += 1
                break
    return count

'''def fear(dict): #maggiore è fear migliore è la creatura
    """conta quante volte la creatura EVITA il veleno quando c'è: minimo 1 max 65"""
    count = 0
    chiavi = list(dict.keys())

    for k in chiavi: #scorro sulle chiavi
        vel = [i for i in range(len(k)) if k[i] == '2'] #estraggo gli indici dei veleni
        if int(dict[k]) in vel:
            count += 1 
    return count'''
        
def fear(dict):
    '''notare che in questo caso il massimo di fear è 64, perchè 0000 e 2222 non mi danno +1 nel count'''
    count = 0
    chiavi = list(dict.keys())
    for k in chiavi:
        if '2' in k:    
            for i in range(0,4):
                if dict[k]==i and int(k[i]) != 2:
                    count +=1
                    break
    return count





# PROGRAMMA PRINCIPALE

def main(npop, mut_prob, ngen, cut_crss = CUT_CRSS, ntorte = 60, grafici = True, scritte = True):

    #parser = argparse.ArgumentParser(description = "Istinto di sopravvivenza con algoritmi genetici")
    #parser.add_argument('popsize', help= "Numero di creature", type=int)
    #parser.add_argument('mut_prob', help= "Probabilità di mutazione", type=float)
    #parser.add_argument('ngen', help= "Numero di generazioni", type=int)
    #parser.add_argument('--no_plots', help="does not show plots", default=False, action='store_true')
    #args = parser.parse_args()

    #print(args)

    #npop = args.popsize
    #mut_prob = args.mut_prob
    #ngen = args.ngen

    if grafici:
        fig, ax = plt.subplots() #creo la mia lista di plot

    #creo la prima e unica popolazione casuale
    creature = [Creature() for i in range(npop)] 

    NTORTE = ntorte
    CUT_CRSS = cut_crss

    gen_media_greed = []  #questi voglio poi plottarli in STATISTICS per vedere eventuali correlazioni
    gen_media_energia = []
    gen_media_fear = []
    contatore = 0

    for n in range(ngen): 

        #creo un ambiente random:
        ambiente = [[0 for i in range(0, NGRIGLIA)] for n in range(0, NGRIGLIA)]
        
        #aggiungo delle torte
        while np.sum(ambiente)<NTORTE:
            ambiente[random.randint(0, NGRIGLIA-1)][random.randint(0, NGRIGLIA-1)]= 1

        #aggiungo veleni, posso mettere veleno se le torte lasciano spazio!
        #per questo motivo metto max(NVELENO, NGRIGLIA**2 - NTORTE)
        if SWITCH_VELENO:
            indici = []
            for i in range(NGRIGLIA):
                for j in range(NGRIGLIA):
                    if ambiente[i][j] == 0: #dove non ci sono torte o veleni
                        indici += [[i, j]]
            pos_veleno = random.sample(indici, min(NVELENO, NGRIGLIA**2 - NTORTE))
            for i in pos_veleno:
                ambiente[i[0]][i[1]] = 2 #codice per il veleno
       

        media_energia_iniziale = sum([c.energia for c in creature]) / len(creature)

        """ci assicuriamo di dare +1 energia alle creature spawnate su una torta e -1 a quelle sul veleno"""
        #ciclo sulle creature e controllo se nelle coord c'è un 1 nella griglia ambiente
        for c in creature:
            if ambiente[c.x][c.y] == 1 :
                c.energia += 1      #incremento energia del fortunato
                ambiente[c.x][c.y] = 0  # tolgo la torta dall'ambiente

            elif ambiente[c.x][c.y] == 2 :
                if c.energia == 1:
                    c.energia = 0
                    ambiente[c.x][c.y] = 0
                else:
                    c.energia -= 1      #decremento energia dello sfortunato
                    ambiente[c.x][c.y] = 0  # tolgo il veleno dall'ambiente

        if grafici:

            plot_creature(creature, ambiente, ax)
            plt.title(f' generazione numero {n+1}')

        for i in range(NMOSSE): #faccio muovere le creature della stessa generazione
            
            for c in creature:

                movimento(c, ambiente)

            if grafici:

                plt.pause(.5) #questo aspetta un secondo prima di visualizzare lo step successivo nel grafico

                plt.draw() #questo aggiorna il grafico con i nuovi dati di creatura e ambiente che sono stati modificati da movimento

                plot_creature(creature, ambiente, ax)
                plt.title(f' generazione numero {n+1}')

        energie = [c.energia for c in creature]
        best_en = max(energie)
        media_energia = sum(energie) / len(creature)
        media_greed = sum([greed(c.mosse) for c in creature])/ len(creature) #media delle bontà di ogni creatura
        media_fear = sum([fear(c.mosse) for c in creature])/ len(creature)

        '''in STATISTICS vorrei studiare la correlazione tra energia e greed:'''
        #########################################################################
        gen_media_greed += [media_greed]
        gen_media_energia += [media_energia]
        gen_media_fear += [media_fear]
        #########################################################################
        '''                                                                   '''


        if scritte:
            print(f"energia, greed e fear medie, gen numero {n+1}:\
                {round(media_energia,2), round(media_greed,2), round(media_fear,2)} \
                 \t differenza tra medie prima a e dopo il movimento: {round(media_energia_iniziale - media_energia, 2)}")

        '''generazione successiva EVOLUTIVA:''' 
        
        if sum([c.energia for c in creature])==0:
            print("estinzione")
            break
        creature = get_offsprings(creature, npop, mut_prob, scritte) #commentando questa linea tolgo tutto lo sforzo darwiniano
        #per come funziona get_offspring ora è una lista vuota se non c'è più vita, in questo caso termino

        """generazione successiva CASUALE:
            tenere il successivo blocco commentato, serve per apprezzare la differenza tra evoluzione che premia
            i più adatti e evoluzione completamente casuale. Utile per discriminare i set di parametri troppo permissivi
            (cioè quelli in cui anche un approccio casuale basterebbe).
            Scelgo di dare a tutti i figli casuali addirittura l'energia del migliore dei genitori (altrimenti
            hanno sempre energia 10 e non muoiono mai)"""
        #creature = [Creature(energia=best_en) for i in range(npop)] 
        

        if n == ngen-1:
            contatore = 1

    '''abbiamo ngen generazioni, con la prima indicizzata dallo 0 e lultima indicizzata da ngen-1'''

    
    if grafici:
        plt.show()

    '''questa è lenergia dell'ultima generazione, quella che in realtà non abbiamo considerato'''
    media = sum([c.energia for c in creature])/len(creature)
    greed_media = sum([greed(c.mosse) for c in creature])/len(creature)
    fear_media = sum([fear(c.mosse) for c in creature])/len(creature)

    
    #return media, greed_media, fear_media
    return gen_media_energia, gen_media_greed, gen_media_fear
    
    #return 1 se è arrivato alla ngen generazione altrimenti 0
    #return contatore


"""risultati interssanti con 20 pop_size 0.4 mut_prob (anche con 0.1 si ottengono risultati simili di crescita
    dell'energia, ma meno velocemente. nonostante questo una mutazione bassa mi sembra comunque da preferire nell'ottica
    di ottenere, con abbastanza generazioni la creatura quasi perfetta) 
    (100 generazione per esempio) e con 40 torte, 10 griglia
    10 energia e 5 mosse: recuperano energia se riescono a superare la prima decina di generazioni e quindi imparare,
    raggiungono in 100 generazioni anche picchi di 5 di energia media dopo essere stati a 0.5 inizialmente"""

""" al momento, dagli esperimenti, non mi sembra evidente l'importanza delle mutazioni: anche azzerandole c'è progresso.
    rischi di massimi locali però?"""

if __name__ == '__main__':

    main(npop= 20, mut_prob=0.1, ngen=50, cut_crss= CUT_CRSS, ntorte= 10, grafici= True, scritte = True)
