
from matplotlib import image
import matplotlib.pyplot as plt
import main_torte


def cut_ottimo():

    crossovers = [i for i in range(0,16)]
    #fig, ax = plt.subplots()

    energie_medie = []
    goodness_medie = []
    

    for j in crossovers:

        energia_media = []

        for i in range(0,10):

            energia_media += [main_torte.main(npop = 20, mut_prob = 0.1, ngen =  10, cut_crss = j, ntorte = 80, grafici = False, scritte = True)]

        energie_medie += [sum(energia_media)/len(energia_media)]


    print(energie_medie)
   # ax.scatter(crossovers, energie_medie)

    #plt.show()


if __name__ == '__main__':

    cut_ottimo()