import numpy as np
from math import gamma, sin, pi
import matplotlib.pyplot as plt

def sphere(x):
    #! so para testar
    s = sum(x**2)
    return s

def rosenBrock(X, a=1, b=100):
    x,y=X
    return ((a-x)**2+b*(y-x**2)**2)

def fireFly(problem, param):
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

        pop[i]['cost'] = func(pop[i]['pos'])
        
        if pop[i]['cost'] < gbest['cost']:
            gbest['pos'] = pop[i]['pos'].copy()
            gbest['cost'] = pop[i]['cost'].copy()
            
    best_cost = []
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
                    
                    new['cost'] = func(new['pos'])
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
        
        best_cost.append(gbest['cost'])
        # best_cost.append(gbest)
        
        alpha = alpha * damp
        
    return gbest, best_cost, eval_cost
    
    
    
# #-----------------------------------------------------
def test():
    problem = {
        'costFunction': sphere,
        'nVar': 2,
        'var_min': -5,
        'var_max': 5,   
    }    
    param = {
        'itermax': 50,
        'npop': 20,
        'gamma': 1,
        'beta0': 1,
        'alpha': 0.2,
        'damp': 0.9,
        'scale': (problem['var_max'] - problem['var_min']),
    }

    gbest, best_cost = fireFly(problem, param)
    print(best_cost)
    print('\nglobal best:')
    print(gbest)

    plt.plot(range(0,param['itermax']), best_cost)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    test()



