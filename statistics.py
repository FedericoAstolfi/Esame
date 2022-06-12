
from matplotlib import image
import matplotlib.pyplot as plt
import main_torte


def cut_ottimo():

    crossovers = [i for i in range(0,16)]
<<<<<<< HEAD
    fig, (ax1, ax2) = plt.subplots(1,2)
=======
    #fig, ax = plt.subplots()
>>>>>>> 5b176e285c8ce12b17e09c50911b365cace017b6

    energie_medie = []
    goodness_medie = []
    

    for j in crossovers:

<<<<<<< HEAD
        energia_media = [main_torte.main(npop = 20, mut_prob = 0.1, ngen =  10, cut_crss = j, ntorte = 60, grafici = False)[0] for i in range(0,50)]
        goodness_media = [main_torte.main(npop = 20, mut_prob = 0.1, ngen =  10, cut_crss = j, ntorte = 60, grafici = False)[1] for i in range(0,50)]
        
        energie_medie += [sum(energia_media)/len(energia_media)]
        goodness_medie += [sum(goodness_media)/len(goodness_media)]
        


    ax1.bar(crossovers, energie_medie)
    ax1.set_title('relazione crossover/energia media')
    ax2.bar(crossovers, goodness_medie)
    ax2.set_title('relazione crossover/bontà media')
    
=======
        energia_media = []

        for i in range(0,10):

            energia_media += [main_torte.main(npop = 20, mut_prob = 0.1, ngen =  10, cut_crss = j, ntorte = 80, grafici = False, scritte = True)]

        energie_medie += [sum(energia_media)/len(energia_media)]


    print(energie_medie)
   # ax.scatter(crossovers, energie_medie)
>>>>>>> 5b176e285c8ce12b17e09c50911b365cace017b6

    #plt.show()


if __name__ == '__main__':

    cut_ottimo()