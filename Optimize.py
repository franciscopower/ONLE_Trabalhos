from FF import fireFly
from Benchmark_2020 import benchmark_2020



problem = {
    'costFunction': objectiveFunction,
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
    'lambda': 1.5,
}

gbest, best_cost = fireFly(problem, param)
print(best_cost)
print('\nglobal best:')
print(gbest)