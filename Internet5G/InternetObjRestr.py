#!/usr/bin/python

import numpy as np
import cv2 as cv
from functools import partial
import math
from FF_5g import fireFly
import matplotlib.pyplot as plt
import pandas as pd

import ray_tracer

# original_size = None #! para visualizacao

def objFunction(intensidty, bump_map):
    area_disponivel=np.sum(bump_map/255)

    intensidade_total=np.sum(intensidty)

    funcao_objtivo=intensidade_total/area_disponivel
    
    return funcao_objtivo

def restriction_verify_position(bump_map,src_pos):
    # objtivo por os router so na zona premitida

    for point in src_pos:

        if bump_map[point[1]][point[0]] != 255:
            return False

    return True

def restriction_intesity_min(matriz, bump_map, power, value_min):
    # restricao para verificar a intencidade

    _, bump_map = cv.threshold(bump_map, 5, 255, cv.THRESH_BINARY)
    bump_map=bump_map*255*power
    somaMatrix=bump_map+matriz
    min=np.amin(somaMatrix)

    return value_min>min

def objective_function(x, kwargs):

    bump_map=kwargs["bump_map"]
    restriction_map=kwargs["restriction_map"]
    power=kwargs["power"]
    value_min=kwargs["value_min"]
    scale_real=kwargs["scale_real"]

    # para pasar de lista para array
    x = x.astype(int)
    src_pos=x.reshape(x.shape[0]/2,2)

    # devolve a matriz intencidades procesadas pelo algoritmo ray_tracer
    intensity_matrix = ray_tracer.intensityMatrix(bump_map, src_pos, power, restriction_map, scale_real)
    
    #Calculate objective function
    funcao_objtivo = 1/objFunction(intensity_matrix,restriction_map)

#_______________________________________________________________________________
#
    # # Print results
    # print('Objective Function: ' + str(funcao_objtivo))
    # # print('Minimum intensity restriction: ' + str(restriction_min_intensity))
    # # print('Position restriction: ' + str(restriction_position))
    
    # #visualize result
    # final_visualization = intensity_matrix * 255 / power * 10
    # final_visualization = cv.resize(final_visualization, (original_size[1], original_size[0]))
    # cv.imshow('light_window', final_visualization)
    
    # bump_map = cv.resize(bump_map,  (original_size[1], original_size[0]))
    # cv.imshow('bump_map_window', bump_map)
    
    # cv.waitKey(0)

    return funcao_objtivo

def main():
    
    # global original_size #! para visualizacao
    
    # Dados ----------------------
    bump_map = cv.imread('Internet5G/bump_map1.png', 0)
    restriction_map = cv.imread('Internet5G/bump_map1.png', 0)
    
    # original_size = bump_map.shape #! para visualizacao
    
    scale_factor = 4
    scale_real = scale_factor
    bump_map = cv.resize(bump_map, (int(bump_map.shape[1] / scale_factor), int(bump_map.shape[0] / scale_factor)))
    
    restriction_map = cv.resize(restriction_map, (int(restriction_map.shape[1] / scale_factor), int(restriction_map.shape[0] / scale_factor)))
    
    power = 100
    value_min = 0
    ntorre=5

    problem = {
        'costFunction': objective_function,
        'nVar': 2*ntorre,
        'var_min': [0.0, 0.0]*ntorre,
        'var_max': [bump_map.shape[1], bump_map.shape[0]]*ntorre
    }
    param = {
        'itermax': 10,
        'npop': 50,
        'gamma': 1, #1
        'beta0': 1.8,
        'alpha': 0.1, #0.2
        'damp': 0.4,
        'scale': (np.array(problem['var_max']) - np.array(problem['var_min'])),
    }

    
    best_cost_total = []
    best_global_best = [np.inf]*param['itermax']
    gbest_value = np.inf

    for _ in range(1):
        
        gbest, iter_best, eval_cost = fireFly(problem, param, bump_map=bump_map, restriction_map=restriction_map, power=power, value_min=value_min, scale_real=scale_real)
        
        best_cost_total.append(iter_best['cost'])
        
        if gbest_value > gbest['cost']:
            gbest_value = gbest['cost']
            gbest_pos = gbest['pos']
            best_global_best = iter_best['cost']
        
        
        print(iter_best)
        print('\nGlobal best in test:')
        print(gbest)
        
        # plt.plot(eval_cost)
        
    print('\n----------------------------------\n')
    print('Global best cost: ' + str(gbest_value))
    print('Global best position: ')
    print(gbest_pos)
        
    average_best = [0]*len(iter_best['cost'])
    for i in range(0,len(best_cost_total)):
        for j in range(0, len(iter_best['cost'])):
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
    
    
    eval_cost_df = pd.DataFrame({"evaluation_cost":eval_cost})
    eval_cost_df.to_csv('internet5G_eval_cost.csv')
    
    columns = ['x'+str(n+1) for n in range(problem['nVar'])]
    columns = ['cost'] + columns
    
    data = np.zeros((param['itermax'],problem["nVar"]+1))
    for l in range(param['itermax']):
        data[l][0] = iter_best['cost'][l]
        data[l][1:] = iter_best['pos'][l]
            
    iter_cost_df = pd.DataFrame(data, columns=columns)
    iter_cost_df.to_csv('internet5G_iteration_cost.csv')


if __name__ == '__main__':
    main()
    
    # # Dados para testar funcao objetivo----------------------
    # bump_map = cv.imread('Internet5G/bump_map1.png', 0)
    # restriction_map = cv.imread('Internet5G/bump_map1.png', 0)

    # x = np.array([50, 50, 120, 30])
    
    # power = 100
    # value_min = 0
    
    # kwargs = {'bump_map':bump_map, 'restriction_map': restriction_map, 'power':power, 'value_min':value_min}
    
    # custo = objective_function(x, kwargs)







