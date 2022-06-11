
from matplotlib import image
import matplotlib.pyplot as plt
import main_torte

if __name__ == '__main__':

    crossovers = [i for i in range(0,16)]
    fig, ax = plt.subplots()

    energie_medie = []

    for j in crossovers:

        energia_media = []

        for i in range(0,100):

            energia_media += [main_torte.main(npop = 20, mut_prob = 0.1, ngen =  100, cut_crss = j, ntorte = 60, grafici = False)]

        energie_medie += sum(energia_media)/len(energia_media)


    ax = plt.hist(crossovers, energie_medie)

    plt.show()