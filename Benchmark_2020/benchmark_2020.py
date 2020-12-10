#!/usr/bin/python

import numpy as np
import math
import matplotlib.pyplot as plt

from FF import fireFly

def objectiveFunction(x):
    
    x1,x2,x3,x4,x5,x6,x7 = x
    F=0.7854*x1*x2**2*(3.3333*x3**2+14.9334*x3-43.0934)-1.508*x1*(x6**2+x7**2)+0.7854*(x4*x6**2+x5*x7**2)
    
    # aplicar penalizacoes externas
    rg = 10
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
    G=(27/(x1*x2**2*x3))-1
    return G

def G2(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    G=(397.5/(x1*x2**2*x3**2))-1
    return G

def G3(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    G=((1.93*x4**3)/(x2*x3*x6**4))-1
    return G

def G4(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    G=((1.93*x5**3)/(x2*x3*x7**4))-1
    return G

def G5(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    G=((math.sqrt((((745*x4)/(x2*x3))**2)+16.9e6))/110*x6**3)-1
    return G

def G6(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    G=((math.sqrt((((745*x5)/(x2*x3))**2)+157.5e6))/85*x7**3)-1
    return G

def G7(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    G=((x2*x3)/40)-1
    return G

def G8(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    G=((5*x2)/(x1))-1
    return G

def G9(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    G=((x1)/(12*x2))-1
    return G

def G10(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    G=((1.5*x6+1.9)/x4)-1
    return G

def G11(x):
    x1,x2,x3,x4,x5,x6,x7 = x
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
        'itermax': 50,
        'npop': 50,
        'gamma': 1,
        'beta0': 1,
        'alpha': 0.2,
        'damp': 0.9,
        'scale': (np.array(problem['var_max']) - np.array(problem['var_min'])),
        'lambda': 1.5,
    }

    gbest, best_cost = fireFly(problem, param)
    print(best_cost)
    print('\nglobal best:')
    print(gbest)
    
    plt.plot(range(0,param['itermax']), best_cost)
    plt.grid(True)
    plt.show()
    
if __name__ == '__main__':
    main()