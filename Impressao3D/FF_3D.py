import numpy as np
from math import gamma, sin, pi
import matplotlib.pyplot as plt

def fireFly(problem, param, **kwargs):
    func = problem['costFunction']
    xmin = problem['var_min']
    xmax = problem['var_max']
    nvar = problem ['nVar']
        
    itermax = param['itermax']
    npop = param['npop']
    gamma = param['gamma']
    b0 = param['beta0']
    alpha = param['alpha']
    damp = param['damp']
    scale = param['scale']

    gbest = {
        'pos': None,
        'cost': np.inf,
    }
    
    empty_particle = {
        'pos': None,
        'cost': None,
    }        
    new_pop = [empty_particle.copy() for _ in range(0, npop)]
    new = empty_particle.copy()
    
    #initialize population
    pop = []
    for i in range(0, npop):
        pop.append(empty_particle.copy())


        pop[i]['pos'] = np.random.uniform(xmin, xmax, nvar)

        pop[i]['cost'] = func(pop[i]['pos'], kwargs)
        
        if pop[i]['cost'] < gbest['cost']:
            gbest['pos'] = pop[i]['pos'].copy()
            gbest['cost'] = pop[i]['cost'].copy()
            
    iter_best = {'pos':[],'cost':[]}
    eval_cost = []
        
    # main loop
    for _ in range(0, itermax):
        
        for i in range(0, npop):
            new_pop[i]['cost'] = np.inf
            for j in range(0, npop):
                if pop[j]['cost'] < pop[i]['cost']:
                    distance = np.linalg.norm(pop[i]['pos'] - pop[j]['pos'])
                    position = pop[i]['pos'] \
                        + b0 * np.exp(-gamma * distance**2) * (pop[j]['pos'] - pop[i]['pos']) \
                        + alpha * scale * np.random.uniform(-1,1,nvar)
                    new['pos'] = np.minimum(np.maximum(position, xmin), xmax)
                    
                    new['cost'] = func(new['pos'], kwargs)
                    eval_cost.append(new['cost'])
                    
                    if new['cost'] < new_pop[i]['cost']:
                        new_pop[i]['pos'] = new['pos'].copy()
                        new_pop[i]['cost'] = new['cost'].copy()
                        
                        if new_pop[i]['cost'] < gbest['cost']:
                            gbest['cost'] = new_pop[i]['cost'].copy()
                            gbest['pos'] = new_pop[i]['pos'].copy()

    
        pop = pop + new_pop
        pop = sorted(pop, key=lambda i: i['cost'])
        pop = pop[0:npop]
        
        iter_best['cost'].append(gbest['cost'])
        iter_best['pos'].append(gbest['pos'])
        
        alpha = alpha * damp
        print("ole")
        
    return gbest, iter_best, eval_cost
    


