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
    scale_factor = 4
    bump_map = cv.resize(bump_map, (int(bump_map.shape[1] / scale_factor), int(bump_map.shape[0] / scale_factor)))
    
    # devolve a matriz intencidades procesadas pelo algoritmo ray_tracer
    intensity_matrix = ray_tracer.intensityMatrix(bump_map, src_pos, power, scale_factor)

    # Check restrictions
    restriction_min_intensity = restriction_intesity_min(intensity_matrix,bump_map, power, value_min)
    
    _, bump_map_inv = cv.threshold(bump_map, 5, 255, cv.THRESH_BINARY_INV)
    restriction_position = restriction_verify_position(bump_map_inv, src_pos)
    
    #Calculate objective function
    funcao_objtivo = objFunction(intensity_matrix,bump_map_inv)

    # Print results
    print('Objective Function: ' + str(funcao_objtivo))
    print('Minimum intensity restriction: ' + str(restriction_min_intensity))
    print('Position restriction: ' + str(restriction_position))
    
    #Show image
    cv.imshow('tata',bump_map)
    cv.imshow('tata2',bump_map_inv)

    cv.waitKey(0)

if __name__ == "__main__":
    main()









