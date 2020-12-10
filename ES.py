import numpy as np
from math import gamma, sin, pi

def sphere(x):
    #! so para testar
    return sum(x**2)

def levy(l, varsize):
    xvar = (gamma(1+l) * sin(pi * l / 2) / gamma((1 + l)/2 * l * 2**((l-1)/2)) )**(2/l)
    yvar = 1
    x=np.random.normal(loc=0.0, scale=xvar, size=varsize)
    y=np.random.normal(loc=0.0, scale=yvar, size=varsize)
    v=x/(abs(y)**(1/l))
    
    return v


def eagleStrategy(problem, param):
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
    l = param['lambda']

    if l <= 1 or l > 3:
        raise('=========================================\nParameter for Levy Flight. 1 < alpha <= 3\n=========================================')    
        
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
        pop[i]['pos'] = np.ones(nvar)#np.random.uniform(xmin, xmax, nvar)
        pop[i]['cost'] = func(pop[i]['pos'])
        
        if pop[i]['cost'] < gbest['cost']:
            gbest['pos'] = pop[i]['pos'].copy()
            gbest['cost'] = pop[i]['cost'].copy()
            
    best_cost = []
        
    # main loop
    for _ in range(0, itermax):
        
        # levy flight
        for i in range(0, npop):
            new_pop[i]['pos'] = np.minimum(np.maximum(pop[i]['pos'] + levy(l, nvar), xmin), xmax)
            new_pop[i]['cost'] = func(new_pop[i]['pos'])
            if new_pop[i]['cost'] < pop[i]['cost']:
                pop[i]['pos'] = new_pop[i]['pos'].copy()
                pop[i]['cost'] = new_pop[i]['cost'].copy()
        
        
        for i in range(0, npop):
            new_pop[i]['cost'] = np.inf
            for j in range(0, npop):
                if pop[j]['cost'] < pop[i]['cost']:
                    distance = np.linalg.norm(pop[i]['pos'] - pop[j]['pos'])
                    new['pos'] = np.minimum(np.maximum(pop[i]['pos'] \
                        + b0 * np.exp(-gamma * distance**2) * (pop[j]['pos'] - pop[i]['pos']) \
                        + alpha * scale * np.random.uniform(-1,1,nvar), xmin), xmax)
                    
                    new['cost'] = func(new['pos'])
                    
                    if new['cost'] < new_pop[i]['cost']:
                        new_pop[i]['pos'] = new['pos'].copy()
                        new_pop[i]['cost'] = new['cost'].copy()
                        
                        if new_pop[i]['cost'] < gbest['cost']:
                            gbest['cost'] = new_pop[i]['cost'].copy()
                            gbest['pos'] = new_pop[i]['pos'].copy()

    
        pop = pop + new_pop
        pop = sorted(pop, key=lambda i: i['cost'])
        pop = pop[0:npop]
        
        best_cost.append(gbest['cost'])
        
        alpha = alpha * damp
        
    return gbest, best_cost
    
    
    
#-----------------------------------------------------
problem = {
    'costFunction': sphere,
    'nVar': 5,
    'var_min': -5,
    'var_max': 5,   
}    
param = {
    'itermax': 100,
    'npop': 5,
    'gamma': 1,
    'beta0': 1,
    'alpha': 0.2,
    'damp': 0.9,
    'scale': (problem['var_max'] - problem['var_min']),
    'lambda': 1.5,
}

gbest, best_cost = eagleStrategy(problem, param)
print(best_cost)
print('\nglobal best:')
print(gbest)




