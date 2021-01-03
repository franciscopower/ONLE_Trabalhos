#!/usr/bin/python

import numpy as np
import math
import matplotlib.pyplot as plt
from FF import fireFly
import json
import pylab

def objectiveFunction(x):
    
    x1,x2,x3,x4,x5,x6,x7 = x
    x3 = round(x3)
    F=0.7854*x1*x2**2*(3.3333*x3**2+14.9334*x3-43.0934)-1.508*x1*(x6**2+x7**2)+0.7854*(x4*x6**2+x5*x7**2) + 7.4777*(x6**3 + x7**3)
    
    # aplicar penalizacoes externas
    rg = 1e10
    gamma = 2
    F = F + rg*max(0, G1(x))**gamma \
        + rg*max(0, G2(x))**gamma \
        + rg*max(0, G3(x))**gamma \
        + rg*max(0, G4(x))**gamma \
        + rg*max(0, G5(x))**gamma \
        + rg*max(0, G6(x))**gamma \
        + rg*max(0, G7(x))**gamma \
        + rg*max(0, G8(x))**gamma \
        + rg*max(0, G9(x))**gamma \
        + rg*max(0, G10(x))**gamma \
        + rg*max(0, G11(x))**gamma
        
    return F

def G1(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    x3 = round(x3)
    G=(27/(x1*x2**2*x3))-1
    return G

def G2(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    x3 = round(x3)
    G=(397.5/(x1*x2**2*x3**2))-1
    return G

def G3(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    x3 = round(x3)
    G=((1.93*x4**3)/(x2*x3*x6**4))-1
    return G

def G4(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    x3 = round(x3)
    G=((1.93*x5**3)/(x2*x3*x7**4))-1
    return G

def G5(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    x3 = round(x3)
    G=((math.sqrt((((745*x4)/(x2*x3))**2)+16.9e6))/(110*x6**3))-1
    return G

def G6(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    x3 = round(x3)
    G=((math.sqrt((((745*x5)/(x2*x3))**2)+157.5e6))/(85*x7**3))-1
    return G

def G7(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    x3 = round(x3)
    G=((x2*x3)/40)-1
    return G

def G8(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    x3 = round(x3)
    G=((5*x2)/(x1))-1
    return G

def G9(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    x3 = round(x3)
    G=((x1)/(12*x2))-1
    return G

def G10(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    x3 = round(x3)
    G=((1.5*x6+1.9)/x4)-1
    return G

def G11(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    x3 = round(x3)
    G=((1.1*x7+1.9)/(x5))-1
    return G

def main():
    problem = {
        'costFunction': objectiveFunction,
        'nVar': 7,
        'var_min': [2.6, 0.7, 17.0, 7.3, 7.8, 2.9, 5.0],
        'var_max': [3.6, 0.8, 28.0, 8.3, 8.3, 3.9, 5.5],   
    }    
    param = {
        'itermax': 10,
        'npop': 100,
        'gamma': 1, #1
        'beta0': 1.8,
        'alpha': 0.1, #0.2
        'damp': 0.4,
        'scale': (np.array(problem['var_max']) - np.array(problem['var_min'])),
    }
    
    best_cost_total = []
    best_global_best = [np.inf]*param['itermax']
    gbest_value = np.inf

    fig1 = plt.figure()
    
    for _ in range(1):
        
        gbest, best_cost, eval_cost = fireFly(problem, param)
        
        best_cost_total.append(best_cost)
        
        if gbest_value > gbest['cost']:
            gbest_value = gbest['cost']
            gbest_pos = gbest['pos']
            best_global_best = best_cost
        
        
        # print(best_cost)
        print('\nglobal best:')
        print(gbest)
        
        print('Restricoes')
        print(G1(gbest['pos']),G2(gbest['pos']),G3(gbest['pos']),G4(gbest['pos']),G5(gbest['pos']),G6(gbest['pos']),G7(gbest['pos']),G8(gbest['pos']),G9(gbest['pos']),G10(gbest['pos']),G11(gbest['pos']),)
        
        # plt.plot(eval_cost)
        
    print('\n----------------------------------\n')
    print('Global best cost: ' + str(gbest_value))
    print('Global best position: ')
    print(gbest_pos)
        
    average_best = [0]*len(best_cost)
    for i in range(0,len(best_cost_total)):
        for j in range(0, len(best_cost)):
            average_best[j] += best_cost_total[i][j]
    average_best = [i/(len(best_cost_total)) for i in average_best]
    plt.plot(range(0, param['itermax']), average_best, label='Curva media de convergencia')
    plt.plot(range(0, param['itermax']), best_global_best, label='Melhor curva de convergencia')
    
    plt.title("Evolucao do custo da funcao objetivo")
    plt.xlabel("Avaliacao")
    plt.ylabel("Custo")
    plt.legend(loc="upper left")
    plt.grid(True)
    plt.yscale("log",basey=10)
    plt.show()
    
    results = {'gbest':gbest, 'best_cost':best_cost, 'eval_cost':eval_cost}
    

def analise_sensibilidada():

    problem = {
        'costFunction': objectiveFunction,
        'nVar': 7,
        'var_min': [2.6, 0.7, 17.0, 7.3, 7.8, 2.9, 5.0],
        'var_max': [3.6, 0.8, 28.0, 8.3, 8.3, 3.9, 5.5],
    }
    # valor medio quando nao esta a ser usada
    mx1=(problem['var_min'][0]+problem['var_max'][0])/2
    mx2 = (problem['var_min'][1] + problem['var_max'][1]) / 2
    mx3 = (problem['var_min'][2] + problem['var_max'][2]) / 2
    mx4 = (problem['var_min'][3] + problem['var_max'][3]) / 2
    mx5 = (problem['var_min'][4] + problem['var_max'][4]) / 2
    mx6 = (problem['var_min'][5] + problem['var_max'][5]) / 2
    mx7 = (problem['var_min'][6] + problem['var_max'][6]) / 2

    # sensibilidade X1

    x11=[]
    y11=[]
    for mv in np.linspace(problem['var_min'][0],problem['var_max'][0],10):
        xf=[mv,mx2,mx3, mx4, mx5, mx6, mx7]

        x1, x2, x3, x4, x5, x6, x7 = xf
        y11.append(0.7854 * x1 * x2 ** 2 * (3.3333 * x3 ** 2 + 14.9334 * x3 - 43.0934) - 1.508 * x1 * (x6 ** 2 + x7 ** 2) + 0.7854 * (x4 * x6 ** 2 + x5 * x7 ** 2) + 7.4777 * (x6 ** 3 + x7 ** 3))
        x11.append(mv)

    x22 = []
    y22 = []
    for mv in np.linspace(problem['var_min'][1], problem['var_max'][1], 10):
        xf = [mx1, mv, mx3, mx4, mx5, mx6, mx7]

        x1, x2, x3, x4, x5, x6, x7 = xf
        y22.append(0.7854 * x1 * x2 ** 2 * (3.3333 * x3 ** 2 + 14.9334 * x3 - 43.0934) - 1.508 * x1 * (
                    x6 ** 2 + x7 ** 2) + 0.7854 * (x4 * x6 ** 2 + x5 * x7 ** 2) + 7.4777 * (x6 ** 3 + x7 ** 3))
        x22.append(mv)

    x33 = []
    y33 = []
    for mv in np.linspace(problem['var_min'][2], problem['var_max'][2], 10):
        xf = [mx1, mx2, mv, mx4, mx5, mx6, mx7]

        x1, x2, x3, x4, x5, x6, x7 = xf
        y33.append(0.7854 * x1 * x2 ** 2 * (3.3333 * x3 ** 2 + 14.9334 * x3 - 43.0934) - 1.508 * x1 * (
                    x6 ** 2 + x7 ** 2) + 0.7854 * (x4 * x6 ** 2 + x5 * x7 ** 2) + 7.4777 * (x6 ** 3 + x7 ** 3))
        x33.append(mv)

    x44 = []
    y44 = []
    for mv in np.linspace(problem['var_min'][3], problem['var_max'][3], 10):
        xf = [mx1, mx2, mx3, mv, mx5, mx6, mx7]

        x1, x2, x3, x4, x5, x6, x7 = xf
        y44.append(0.7854 * x1 * x2 ** 2 * (3.3333 * x3 ** 2 + 14.9334 * x3 - 43.0934) - 1.508 * x1 * (
                    x6 ** 2 + x7 ** 2) + 0.7854 * (x4 * x6 ** 2 + x5 * x7 ** 2) + 7.4777 * (x6 ** 3 + x7 ** 3))
        x44.append(mv)

    x55 = []
    y55 = []
    for mv in np.linspace(problem['var_min'][4], problem['var_max'][4], 10):
        xf = [mx1, mx2, mx3, mx4, mv, mx6, mx7]

        x1, x2, x3, x4, x5, x6, x7 = xf
        y55.append(0.7854 * x1 * x2 ** 2 * (3.3333 * x3 ** 2 + 14.9334 * x3 - 43.0934) - 1.508 * x1 * (
                    x6 ** 2 + x7 ** 2) + 0.7854 * (x4 * x6 ** 2 + x5 * x7 ** 2) + 7.4777 * (x6 ** 3 + x7 ** 3))
        x55.append(mv)

    x66 = []
    y66 = []
    for mv in np.linspace(problem['var_min'][5], problem['var_max'][5], 10):
        xf = [mx1, mx2, mx3, mx4, mx5, mv, mx7]

        x1, x2, x3, x4, x5, x6, x7 = xf
        y66.append(0.7854 * x1 * x2 ** 2 * (3.3333 * x3 ** 2 + 14.9334 * x3 - 43.0934) - 1.508 * x1 * (
                    x6 ** 2 + x7 ** 2) + 0.7854 * (x4 * x6 ** 2 + x5 * x7 ** 2) + 7.4777 * (x6 ** 3 + x7 ** 3))
        x66.append(mv)
    x77 = []
    y77 = []
    for mv in np.linspace(problem['var_min'][6], problem['var_max'][6], 10):
        xf = [mx1, mx2, mx3, mx4, mx5, mx6, mv]

        x1, x2, x3, x4, x5, x6, x7 = xf
        y77.append(0.7854 * x1 * x2 ** 2 * (3.3333 * x3 ** 2 + 14.9334 * x3 - 43.0934) - 1.508 * x1 * (
                x6 ** 2 + x7 ** 2) + 0.7854 * (x4 * x6 ** 2 + x5 * x7 ** 2) + 7.4777 * (x6 ** 3 + x7 ** 3))
        x77.append(mv)








    fig, axs = plt.subplots(3)
    axs[0].plot(x77, y77,'k' ,label='sensibilidade x7')
    axs[0].set(xlabel='X7', ylabel='F')
    axs[0].legend(loc="upper left")
    axs[1].plot(x55, y55, 'm', label='sensibilidade x5')
    axs[1].set(xlabel='X5', ylabel='F')
    axs[1].legend(loc="upper left")
    #axs[1].set_title('Sensibilidade X2')
    axs[2].plot(x66, y66, 'y', label='sensibilidade x6')
    axs[2].set(xlabel='X6', ylabel='F')
    axs[2].legend(loc="upper left")
    #axs[2].set_title('Sensibilidade x3')
    # axs[1, 1].plot(x44,y44, 'tab:red')
    # #axs[1, 1].set_title('Sensibilidade x4')
    # axs[2, 0].plot(x55, y55, 'm')
    # #axs[2, 0].set_title('Sensibilidade x5')
    # axs[2, 1].plot(x66, y66, 'c')
    # #axs[2, 1].set_title('Sensibilidade x6')
    # axs[3, 0].plot(x77, y77, 'tab:red')
    # #axs[3, 0].set_title('Sensibilidade x7')




    # for ax in axs.flat:
    #     ax.set(xlabel='x-label', ylabel='y-label')

    # # Hide x labels and tick labels for top plots and y ticks for right plots.
    # for ax in axs.flat:
    #     ax.label_outer()

    plt.show()

    
if __name__ == '__main__':
    main()
    # analise_sensibilidada()
    # print(objectiveFunction(np.array([3.499999, 0.7, 17.0, 7.3, 7.8, 3.350215, 5.286683])))
    
    