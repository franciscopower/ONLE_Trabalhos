#!/usr/bin/python

import math
from functools import partial

import ray_tracer
from InternetObjRestr import objective_function

import cv2 as cv
import numpy as np

src_pos = [(5, 5), (80,80)]
moving1 = False
moving2 = False
density = 1

def onClick(event, x, y, flags, param):
    global moving1, moving2, src_pos, density
    if event == cv.EVENT_LBUTTONDOWN:
        src_pos[0] = (x,y)
        moving1 = True
    elif event == cv.EVENT_LBUTTONUP:
        src_pos[0] = (x,y)
        density = 1
        moving1 = False
        
    if event == cv.EVENT_RBUTTONDOWN:
        src_pos[1] = (x,y)
        moving2 = True
    elif event == cv.EVENT_RBUTTONUP:
        src_pos[1] = (x,y)
        density = 1
        moving2 = False
    
    if event == cv.EVENT_MOUSEMOVE:
        if moving1:
            src_pos[0] = (x,y)
            density = 2
        elif moving2:
            src_pos[1] = (x,y)
            density = 2
        
        
                            
def calculateIntensity(src_pos, point, power, bump_map):

    # analise das distacias ao scr
    pt_dist = np.zeros((len(src_pos),3))

    #add distances to points
    for i,t in enumerate(src_pos):
        pt_dist[i,:] = [t[0], t[1], ((t[0]-point[0])**2 + (t[1]-point[1])**2)]
        
    # sort distances and points:
    pt_dist = pt_dist[np.lexsort((pt_dist[:,2], ))]


    for d in range(0,pt_dist.shape[0]):
        x = int(pt_dist[d][0])
        y = int(pt_dist[d][1])

        #check for obstacles
        line = np.zeros(bump_map.shape)
        line = cv.line(line, (x,y), point, (255), 1)
        intersection_check = line + bump_map
        line_of_sight = intersection_check[:, :].max() <= 255

        if (x,y) == (point):
            intensity = power
        elif bump_map[point[1],point[0]] != 0:
            intensity = 0
        elif line_of_sight:
            intensity = power / ( 4 * math.pi * pt_dist[d][2] )
            break
        else:
            intensity = 0

    return intensity

def result_objctive_function(bump_map,matiz):
    _, bump_map_ths = cv.threshold(bump_map, 5, 255, cv.THRESH_BINARY_INV)

    aria_disponivel = np.sum(bump_map_ths / 255)

    intensidade_total = np.sum(matiz)

    funcao_objtivo = intensidade_total / aria_disponivel

    return funcao_objtivo

def intensityMatrix():
    light_window = "Light"
    bump_map_window = "Bump Map"
    
    # Dados ----------------------
    bump_map = cv.imread('Internet5G/bump_map_campusV2.jpg', 0)
    restriction_map = cv.imread('Internet5G/restriction_map_campusV2.jpg', 0)

    # input_maps = np.ndarray((bump_map.shape[0], bump_map.shape[1], 3))
    # input_maps[:,:,0]=restriction_map - bump_map
    # input_maps[:,:,1]=0
    # input_maps[:,:,2]=bump_map

    original_size = bump_map.shape

    scale_factor = 4
    scale_real = scale_factor*0.5409 # m/px
    bump_map = cv.resize(bump_map, (int(bump_map.shape[1] / scale_factor), int(bump_map.shape[0] / scale_factor)))

    restriction_map = cv.resize(restriction_map, (int(restriction_map.shape[1] / scale_factor), int(restriction_map.shape[0] / scale_factor)))

    power = 0.5 # mW 
    value_min = 0.000000121
    kwargs = {'bump_map': bump_map,
            'restriction_map': restriction_map,
            'power': power,
            'value_min': value_min,
            'scale_real': scale_real}

    # print(intensity_matrix[-1][-3:-1])
      
    k = ''
    while k != ord('q'):
                
        cv.setMouseCallback(light_window, onClick)
        
        
        src_pos_scaled = [(int(src_pos[0][0]/scale_factor),int(src_pos[0][1]/scale_factor)),(int(src_pos[1][0]/scale_factor),int(src_pos[1][1]/scale_factor))]
        

        intensity_matrix,_,_ = ray_tracer.intensityMatrix(bump_map,src_pos,power, restriction_map, scale_real, density)
                
        final_visualization = intensity_matrix*255/power *10

        final_visualization = cv.resize(final_visualization, (original_size[1], original_size[0]))

        cv.imshow(light_window, final_visualization) 
        
        if k == ord('r'):
            print(objective_function(x, kwargs))

        k = cv.waitKey(1)

        


if __name__ == '__main__':
    intensityMatrix()
