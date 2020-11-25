#!/usr/bin/python

import numpy as np
import cv2 as cv
from functools import partial
import math

import ray_tracer

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


def main():

    # Dados ---------------------- 
    bump_map = cv.imread('bump_map1.png', 0)
    src_pos=[(0,0), (50, 50), (100,100)]
    #allowed_position = cv.imread('allowed_position.png', 0)
    # _, allowed_position = cv.threshold(allowed_position, 5, 255, cv.THRESH_BINARY)
    power = 100
    value_min = 0
    #-----------------------------
    
    #reduce size of bump map for faster analisis
    original_size = bump_map.shape
    scale_factor = 4
    bump_map = cv.resize(bump_map, (int(bump_map.shape[1] / scale_factor), int(bump_map.shape[0] / scale_factor)))
    
    # devolve a matriz intencidades procesadas pelo algoritmo ray_tracer
    intensity_matrix = ray_tracer.intensityMatrix(bump_map, src_pos, power, scale_factor)

    # Check restrictions
    restriction_min_intensity = restriction_intesity_min(intensity_matrix,bump_map, power, value_min)
    
    _, bump_map_inv = cv.threshold(bump_map, 5, 255, cv.THRESH_BINARY_INV)
    restriction_position = restriction_verify_position(bump_map_inv, src_pos) #! aqui sera usada uma imagem propria, allowed_position, nao o inverso do bump_map
    
    #Calculate objective function
    funcao_objtivo = objFunction(intensity_matrix,bump_map_inv)

    # Print results
    print('Objective Function: ' + str(funcao_objtivo))
    print('Minimum intensity restriction: ' + str(restriction_min_intensity))
    print('Position restriction: ' + str(restriction_position))
    
    #visualize result
    final_visualization = intensity_matrix * 255 / power * 10
    final_visualization = cv.resize(final_visualization, (original_size[1], original_size[0]))
    cv.imshow('light_window', final_visualization)
    
    bump_map = cv.resize(bump_map,  (original_size[1], original_size[0]))
    cv.imshow('bump_map_window', bump_map)
    
    cv.waitKey(0)

if __name__ == "__main__":
    main()









