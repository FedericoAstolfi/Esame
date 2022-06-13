
from matplotlib import image
import matplotlib.pyplot as plt
import main_torte
import copy


def cut_ottimo():

    crossovers = [i for i in range(0,16)]
    #fig, ax = plt.subplots()

    energie_medie = []
    goodness_medie = []
    

    for j in crossovers:


        energia_media = [main_torte.main(npop = 20, mut_prob = 0.1, ngen =  10, cut_crss = j, ntorte = 60, grafici = False)[0] for i in range(0,50)]
        goodness_media = [main_torte.main(npop = 20, mut_prob = 0.1, ngen =  10, cut_crss = j, ntorte = 60, grafici = False)[1] for i in range(0,50)]
        

def correlazione():

    '''studia correlazione tra energia e greed al viariare delle generazioni'''

    energia, greed = main_torte.main(npop = 30, mut_prob = 0.1,\
                         ngen = 1000, cut_crss = main_torte.CUT_CRSS, ntorte = 75, grafici = False, scritte = False)

    #normalizzo entrambi i valori di modo che sia più facile vedere che relazione intercorre tra i due
    energy = copy.copy(energia)
    bonta = copy.copy(greed)
    energia = [i/10 for i in energy]
    greed = [i/15 for i in greed]

    fig, ax = plt.subplots()
    ax.plot(range(1, len(energia)+1), energia, color ='r', label = 'energia')
    ax.set_xlabel('generazioni')
    ax.plot(range(1,len(greed)+1), greed, color = 'g', label = 'greed')
    ax.legend()
    plt.show()


def valore_atteso_greed(n):
    """il valore atteso della variabile aleatoria 'greed di una creatura' è 8 (27 per veleno = true), quanta variabilità c'è?
        n numero della popolazione cauale,  visualizza il valore atteso teorico e le greed di ognuna delle n creature"""
    creature = [main_torte.Creature() for i in range(n)] 
    greed = [main_torte.greed(c.mosse) for c in creature]
    fig, ax = plt.subplots()
    ax.plot(range(1,n+1), greed)
    ax.plot(range(1,n+1), [27]*n)
    ax.set_xlabel('popolazione')
    ax.set_ylabel('greed')
    ax.set_title("variabilità greed iniziale")
    plt.show()


def rapporto_minimo():

    for i in range(20,50): #ciclo da 20 individui a 50
        for j in range(30,90,3): #aumento le torte
            rate = 0
            for _ in range(100): #eseguo 100 volte il main
                rate += main_torte.main(npop = i, mut_prob= 0.1, ngen = 100, \
                                        cut_crss = 8, ntorte = j, grafici = False, scritte = False)
            rate = rate/100 #si può fare con gli interi?

if __name__ == '__main__':
    valore_atteso_greed(100)


