
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

    energia, greed = main_torte.main(npop = 20, mut_prob = 0.1, ngen = 10000, cut_crss = main_torte.CUT_CRSS, ntorte = 75, grafici = False, scritte = False)

    #normalizzo entrambi i valori di modo che sia più facile vedere che relazione intercorre tra i due
    energy = copy.copy(energia)
    bonta = copy.copy(greed)
    energia = [i/10 for i in energy]
    greed = [i/65 for i in greed]

    fig, ax = plt.subplots()
    ax.plot(range(1, len(energia)+1), energia, color ='r', label = 'energia')
    ax.set_xlabel('generazioni')
    ax.plot(range(1,len(greed)+1), greed, color = 'g', label = 'greed')
    ax.legend()
    plt.show()

if __name__ == '__main__':
    correlazione()


