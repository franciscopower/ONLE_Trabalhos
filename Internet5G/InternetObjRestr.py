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

def restriction():
    pass

def main():
    src_pos=[(30,10), (50, 50), (100,100)]
    power = 100
    bump_map = cv.imread('bump_map1.png', 0)
    scale_factor = 4

    bump_map = cv.resize(bump_map, (int(bump_map.shape[1] / scale_factor), int(bump_map.shape[0] / scale_factor)))
    # devolve a matriz intencidades procesadas pelo algoritemo ray_tracer
    matriz =ray_tracer.intensityMatrix(bump_map, src_pos, power, scale_factor)

    _,bump_map_ths = cv.threshold(bump_map,5,255,cv.THRESH_BINARY_INV)

    funcao_objtivo = objFunction(matriz, bump_map_ths)

    print (funcao_objtivo)
    
    #cv.imshow('tata',bump_map_ths)
    #cv.waitKey(0)

if __name__ == "__main__":
    main()









