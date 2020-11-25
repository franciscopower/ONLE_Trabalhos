#!/usr/bin/python

import numpy as np
import cv2 as cv
from functools import partial
import math

import ray_tracer

def objFunction(intensidty, bump_map):
    aria_disponivel=np.sum(bump_map/255)

    intensidade_total=np.sum(intensidty)

    funcao_objtivo=intensidade_total/aria_disponivel
    
    return funcao_objtivo

def restriction_verifice_posicion(bump_map,src_pos):
    # objtivo por os router so na zona premitida

    for poit in src_pos:

        if bump_map[poit[1]][poit[0]] != 250:
            return False

    return True

def restriction_intesity_min(matriz, bump_map, power, value_min):
    # restricao para verificar a intencidade

    _, bump_map = cv.threshold(bump_map, 5, 255, cv.THRESH_BINARY)
    bump_map=bump_map*255*power
    somaMatrix=bump_map+matriz
    somaMatrix
    min=np.amin(somaMatrix)

    return value_min>min


def main():

    bump_map = cv.imread('bump_map1.png', 0)

    src_pos=[(30,10), (50, 50), (100,100)]

    restriction_verifice_posicion(bump_map, src_pos)
    power = 100
    value_min = 0
    scale_factor = 4

    bump_map = cv.resize(bump_map, (int(bump_map.shape[1] / scale_factor), int(bump_map.shape[0] / scale_factor)))
    # devolve a matriz intencidades procesadas pelo algoritemo ray_tracer

    matriz =ray_tracer.intensityMatrix(bump_map, src_pos, power, scale_factor)

    print( restriction_intesity_min(matriz,bump_map, power, value_min))
    _, bump_map_inv = cv.threshold(bump_map, 5, 255, cv.THRESH_BINARY_INV)

    funcao_objtivo = objFunction(matriz,bump_map_inv )


    print (funcao_objtivo)
    
    cv.imshow('tata',bump_map)
    cv.waitKey(0)

if __name__ == "__main__":
    main()









