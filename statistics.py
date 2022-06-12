
from matplotlib import image
import matplotlib.pyplot as plt
import main_torte


def cut_ottimo():

    crossovers = [i for i in range(0,16)]
    #fig, ax = plt.subplots()

    energie_medie = []
    goodness_medie = []
    

    for j in crossovers:


        energia_media = [main_torte.main(npop = 20, mut_prob = 0.1, ngen =  10, cut_crss = j, ntorte = 60, grafici = False)[0] for i in range(0,50)]
        goodness_media = [main_torte.main(npop = 20, mut_prob = 0.1, ngen =  10, cut_crss = j, ntorte = 60, grafici = False)[1] for i in range(0,50)]
        

