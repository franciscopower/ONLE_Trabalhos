#!/usr/bin/python

import numpy as np
import interpretGCode
import moveObjects
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import pandas as pd

from FF_3D import fireFly

def objFunction(objs):
    n_layers = [i[1].shape[1] for i in objs]  # numero de camadas de cada objeto

    obj_n = 0  # primeiro objeto a testar
    d_min = np.inf  # distancia para comparacao
    d_total = 0

    # percorrer cada camada
    for l in range(0, max(n_layers)):
        tested = []
        while len(tested)<len(objs)-1:
            tested.append(obj_n)
            
            try:
                out = objs[obj_n][2][:, l]
            except:
                out = objs[obj_n][2][:, l - 1]
            
            for i in range(0, len(objs)):
                if i in tested or l>=n_layers[i]:
                    continue
                
                # get in position of next object
                inn = objs[i][1][:, l]
                # calculate distance
                d = np.sqrt((out[0] - inn[0]) ** 2 + (out[1] - inn[1]) ** 2)

                if d <= d_min:
                    d_min = d
                    obj_n_temp = i
                
            obj_n = obj_n_temp
            d_total += d
            d_min = np.inf
            

    return d_total

# def objFunction(objs):
#     n_layers = [o[1].shape[1] for o in objs]  # numero de camadas de cada objeto

#     total_obj_idx = range(0, len(objs))
#     obj_n = 0  # primeiro objeto a testar
#     d_min = 400  # distancia para comparacao
#     d_total = 0
#     # percorrer cada camada
#     for l in range(0, max(n_layers)):
#         obj_idx = total_obj_idx[:]

#         n_valid_objs = len(total_obj_idx)

#         # comecar no primeiro objeto, ir de objeto em objeto
#         while True:
#             if n_valid_objs <= 1:
#                 break
#             n_valid_objs -= 1
#             try:
#                 obj_idx.pop(obj_idx.index(obj_n))
#             except:
#                 pass
            
#             if not obj_idx:
#                 continue

#             # get out position of current object
#             try:
#                 out = objs[obj_n][2][:, l]
#             except:
#                 out = objs[obj_n][2][:, l - 1]

#             for i in obj_idx:
#                 # check if object has current layer
#                 if objs[i][1].shape[1] >= l + 1:
#                     try:
#                         total_obj_idx.pop(total_obj_idx.index(i))
#                     except:
#                         pass
#                     else:
#                         n_valid_objs -= 1
#                     continue

#                 # get in position of next object
#                 inn = objs[i][1][:, l]
#                 # calculate distance
#                 d = np.sqrt((out[0] - inn[0]) ** 2 + (out[1] - inn[1]) ** 2)

#                 # check if distance is smaller that with the previous object
#                 if d <= d_min:
#                     d_min = d
#                     obj_n_temp = i

#             # update current object and total distance
#             obj_n = obj_n_temp
#             d_total += d_min
#             # print(l, d_min)
#             # reset minimum distance
#             d_min = 400

#     return d_total


def coordsToPoly(objs):
    poly_objs = []
    
    for o in objs:
        polys = []
        poly = []
        n = 0
        
        for i in range(0,o[0].shape[1]):
            
            if o[0][2][i] != o[1][2][n]:
                p = Polygon(poly)
                polys.append(p)
                n += 1
                poly = []
                
            poly.append((o[0][0][i],o[0][1][i]))
        
        p = Polygon(poly)
        polys.append(p)
            
        poly_objs.append(polys)

    return poly_objs


def restrictionMinDist(objs, d_min):
    # points_per_layer = 10 # attention to the interval! This is big right now
    # layer_interval = 10
    #
    # n_layers = [o[1].shape[1] for o in objs] #numero de camadas de cada objeto
    #
    # for l in range(0, max(n_layers), layer_interval):
    #     for i,ob in enumerate(objs):
    #         if i == len(objs)-1 or l>=ob[1].shape[1]:
    #             break
    #
    #         for n in range(i+1, len(objs)):
    #             point_interval1 = int(ob[0].shape[1]/points_per_layer)
    #             for p1_i in range(0,ob[0].shape[1],point_interval1):
    #                 p1 = ob[0][:,p1_i]
    #
    #                 point_interval2 = int(objs[n][1].shape[1]/points_per_layer)
    #                 for p2_i in range(0,objs[n][0].shape[1], point_interval2):
    #                     if l>=objs[n][1].shape[1]:
    #                         break
    #
    #                     p2 = objs[n][0][:,p2_i]
    #
    #                     d = np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
    #                     if d <= d_min:

    #                         return False
    #
    # return True

    poli = coordsToPoly(objs)
    nobj = len(poli)

    # descobre o tamanho de cada obj
    list_size_ogj = []
    list_compre = []
    ariaint = 0
    distsoma = 0

    for u in range(0, nobj):
        list_size_ogj.append(len(poli[u]))
        list_compre.append(True)

    for l in range(0, max(list_size_ogj),7):
        for n in range(0, nobj):
            if l >= list_size_ogj[n]:
                list_compre[n] = False
        for e in range(0, nobj):
            if list_compre[e]:
                for r in range(e + 1, nobj):
                    if list_compre[r]:
                        if poli[e][l].intersects(poli[r][l]):
                            try:
                                ariaint += poli[e][l].intersection(poli[r][l]).area
                            except:
                                ariaint += 1e6

                        if poli[e][l].distance(poli[r][l]) < d_min:
                            distsoma = d_min - poli[e][l].distance(poli[r][l])

    penalizacao = ariaint * 1e6 + distsoma * 1e6

    return penalizacao

def checkInHotBed(objs, hot_bed_size_x, hot_bed_size_y):
    fator_penalizacao = 1e6
    penalizacao_x = 0
    penalizacao_y = 0
    penalizacao_t = 0

    for o in objs:
        x_max = max(o[0][0, :])
        x_min = min(o[0][0, :])
        y_max = max(o[0][1, :])
        y_min = min(o[0][1, :])

        if x_max > hot_bed_size_x / 2:
            penalizacao_x = fator_penalizacao * (x_max - hot_bed_size_x / 2)
        elif x_min < -hot_bed_size_x / 2:
            penalizacao_x = fator_penalizacao * (-x_min - hot_bed_size_x / 2)

        if y_min > hot_bed_size_y / 2:
            penalizacao_y = fator_penalizacao * (y_max - hot_bed_size_x / 2)
        elif y_min < -hot_bed_size_y / 2:
            penalizacao_y = fator_penalizacao * (-y_min - hot_bed_size_x / 2)

        penalizacao_t += (penalizacao_x + penalizacao_y)

    return penalizacao_t


def objFunctionComplete(x, kwargs):
    # so para testar ----------------------
    # objs = interpretGCode.getObjectsPts('Impressao3D/GCode/')
    # trans_list = [
    #     [20,50,0],
    #     [20,60,0],
    #     [-40,50,np.pi/4],
    #     [-20,-20,0],
    # ]
    # --------------------------------------
    
    trans_list = x.reshape(x.shape[0] / 3, 3)

    objs = kwargs['objs']

    # create copy of objs
    new_objs = []
    temp_list = []
    for l in objs:
        for item in l:
            temp_list.append(np.copy(item))
        new_objs.append(temp_list)
        temp_list = []

    new_objs = moveObjects.moveObjects(new_objs, trans_list)
    
    cost = objFunction(new_objs) + checkInHotBed(new_objs, 200, 200) + restrictionMinDist(new_objs, 3)
    
    # print(objFunction(new_objs))
    # print(restrictionMinDist(new_objs, 3))
    # print(checkInHotBed(new_objs, 200, 200))
    # moveObjects.showObjects(new_objs)
    
    return cost


def main():
    objs = interpretGCode.getObjectsPts('Impressao3D/GCode/')

    problem = {
        'costFunction': objFunctionComplete,
        'nVar': 3*len(objs),
        'var_min': [-100, -100, 0]*len(objs),
        'var_max': [100, 100, 2*np.pi]*len(objs),
    }
    param = {
        'itermax': 10,
        'npop': 100,
        'gamma': 1,  # 1
        'beta0': 1.8,
        'alpha': 0.1,  # 0.2
        'damp': 0.4,
        'scale': (np.array(problem['var_max']) - np.array(problem['var_min'])),
    }  
    
    
    best_cost_total = []
    best_global_best = [np.inf]*param['itermax']
    gbest_value = np.inf

    for _ in range(1):
        
        gbest, iter_best, eval_cost = fireFly(problem, param, objs=objs)
        
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
    eval_cost_df.to_csv('impressao3D_eval_costv3_100.csv')
    
    columns = ['x'+str(n+1) for n in range(problem['nVar'])]
    columns = ['cost'] + columns
    
    data = np.zeros((param['itermax'],problem["nVar"]+1))
    for l in range(param['itermax']):
        data[l][0] = iter_best['cost'][l]
        data[l][1:] = iter_best['pos'][l]

    iter_cost_df = pd.DataFrame(data, columns=columns)
    iter_cost_df.to_csv('impressao3D_iteration_costv3_100.csv')


if __name__ == "__main__":
    main()
    # objFunctionComplete(0,0)
