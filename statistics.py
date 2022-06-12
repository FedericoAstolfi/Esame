
from matplotlib import image
import matplotlib.pyplot as plt
import main_torte

if __name__ == '__main__':

    crossovers = [i for i in range(0,16)]
    fig, (ax1, ax2) = plt.subplots(1,2)

    energie_medie = []
    goodness_medie = []
    

    for j in crossovers:

        energia_media = [main_torte.main(npop = 20, mut_prob = 0.1, ngen =  10, cut_crss = j, ntorte = 60, grafici = False)[0] for i in range(0,50)]
        goodness_media = [main_torte.main(npop = 20, mut_prob = 0.1, ngen =  10, cut_crss = j, ntorte = 60, grafici = False)[1] for i in range(0,50)]
        
        energie_medie += [sum(energia_media)/len(energia_media)]
        goodness_medie += [sum(goodness_media)/len(goodness_media)]
        


    ax1.bar(crossovers, energie_medie)
    ax1.set_title('relazione crossover/energia media')
    ax2.bar(crossovers, goodness_medie)
    ax2.set_title('relazione crossover/bontà media')
    

    plt.show()