#!/usr/bin/python

import numpy as np
import cv2 as cv
from functools import partial
import math

import ray_tracer

src_pos=[(30,10), (50, 50), (100,100)]
power = 100
bump_map = cv.imread('bump_map1.png', 0)
scale_factor = 4

bump_map = cv.resize(bump_map, (int(bump_map.shape[1] / scale_factor), int(bump_map.shape[0] / scale_factor)))
# devolve a matriz intencidades procesadas pelo algoritemo ray_tracer
matiz =ray_tracer.intensityMatrix(bump_map, src_pos, power, scale_factor)



_,bump_map_ths = cv.threshold(bump_map,5,255,cv.THRESH_BINARY_INV)

aria_disponivel=np.sum(bump_map_ths/255)

intensidade_total=np.sum(matiz)

funcao_objtivo=intensidade_total/aria_disponivel

print (aria_disponivel)
print (intensidade_total)
print (funcao_objtivo)
#cv.imshow('tata',bump_map_ths)
#cv.waitKey(0)







