
from matplotlib import image
import matplotlib.pyplot as plt
import caso_veleni
import copy


def cut_ottimo():

    crossovers = [i for i in range(0,16)]
    #fig, ax = plt.subplots()

    energie_medie = []
    goodness_medie = []
    

    for j in crossovers:


        energia_media = [caso_veleni.main(npop = 20, mut_prob = 0.1, ngen =  10, cut_crss = j, ntorte = 60, grafici = False)[0] for i in range(0,50)]
        goodness_media = [caso_veleni.main(npop = 20, mut_prob = 0.1, ngen =  10, cut_crss = j, ntorte = 60, grafici = False)[1] for i in range(0,50)]
        

def correlazione():

    '''studia correlazione tra energia e greed al viariare delle generazioni'''

    energia, greed, fear = caso_veleni.main(npop = 20, mut_prob = 0.1,\
                         ngen = 5000, cut_crss = caso_veleni.CUT_CRSS, ntorte = 20, grafici = False, scritte = False, nvel = 60)

    #normalizzo entrambi i valori di modo che sia più facile vedere che relazione intercorre tra i due
    energy = copy.copy(energia)
    bonta = copy.copy(greed)
    paura = copy.copy(fear)
    energia = [i/10 for i in energy]
    greed = [i/65 for i in bonta]
    fear = [i/65 for i in paura]

    fig, ax = plt.subplots()
    ax.plot(range(1, len(energia)+1), energia, color ='r', label = 'energia')
    ax.set_xlabel('generazioni')
    ax.plot(range(1,len(greed)+1), greed, color = 'g', label = 'greed')
    ax.plot(range(1,len(greed)+1),[0.4153846153846154]*(len(greed)),'b')
    ax.plot(range(1,len(fear)+1),fear, color = 'y', label = 'fear')
    ax.legend()
    plt.show()


def valore_atteso_greed(n):
    """il valore atteso della variabile aleatoria 'greed di una creatura' è 8 (27 per veleno = true), quanta variabilità c'è?
        n numero della popolazione cauale,  visualizza il valore atteso teorico e le greed di ognuna delle n creature"""
    creature = [caso_veleni.Creature() for i in range(n)] 
    greed = [caso_veleni.greed(c.mosse) for c in creature]
    fig, ax = plt.subplots()
    ax.plot(range(1,n+1), greed)
    ax.plot(range(1,n+1), [27]*n)
    ax.set_xlabel('popolazione')
    ax.set_ylabel('greed')
    ax.set_title("variabilità greed iniziale")
    plt.show()


    
def test_rapporto():
    fig, ax = plt.subplots()
    lista_torte = [] #qua ci metto il numero più basso di torte per cui la popolazione di i elementi raggiunge rate 0.6 (oppure arriva alle 90 torte)
    for i in range(20,50):
        '''fisso un numero di creature'''
        rate = 0
        torte = 30
        while rate < 0.6 and torte < 90:
            '''questa è la soglia del rate che vorrei superare, ovvero 6 popolazioni su 10 arrivano alla centesima generazione'''
            rate = 0 #azzero il rate a ogni nuovo ciclo se no ho le informazioni vecchie
            torte +=1
            for _ in range(0,100):
                rate += caso_veleni.main(npop= i, mut_prob=0.1, ngen=100, cut_crss= caso_veleni.CUT_CRSS, ntorte= torte, grafici= False, scritte = False)
            rate = [e/100 for e in rate]
        if rate < 0.6:
            print(f'con {i} individui non si raggiunge mai la soglia minima di rate per arrivare alla 100 esima generazione ')
        else:
            print(f'con {i} individui il rate delle volte in cui si raggiunge la 100 esima generazione è {rate},\
                e il numero minimo di torte con cui ciò accade è {torte}')
        lista_torte += [torte]
        ax.bar(range(20,50), lista_torte)
    plt.show()


if __name__ == '__main__':
    correlazione()
    #valore_atteso_greed(100)