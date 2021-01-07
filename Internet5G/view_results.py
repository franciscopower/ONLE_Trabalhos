import pandas as pd
import numpy as np
import ray_tracer
import cv2 as cv

results = pd.read_csv('internet5G_iteration_cost_5_torres.csv')
x = results.values[1,2:]
x = x.astype(int)
src_pos=x.reshape(x.shape[0]/2,2)

density = 1

# Dados ----------------------
bump_map = cv.imread('Internet5G/bump_map_campus.jpg', 0)
restriction_map = cv.imread('Internet5G/restriction_map_campus.jpg', 0)

original_size = bump_map.shape

scale_factor = 4
scale_real = scale_factor*0.5409 # m/px
bump_map = cv.resize(bump_map, (int(bump_map.shape[1] / scale_factor), int(bump_map.shape[0] / scale_factor)))

restriction_map = cv.resize(restriction_map, (int(restriction_map.shape[1] / scale_factor), int(restriction_map.shape[0] / scale_factor)))

power = 0.5 # mW
value_min = 0.000000121
ntorre=3

intensity_matrix = ray_tracer.intensityMatrix(bump_map,src_pos,power, restriction_map, scale_real, density)

# Print results
# print('Objective Function: ' + str(funcao_objtivo))
# print('Minimum intensity restriction: ' + str(restriction_min_intensity))
# print('Position restriction: ' + str(restriction_position))

#visualize result
final_visualization = intensity_matrix * 255 / power * 10
final_visualization = cv.resize(final_visualization, (original_size[1], original_size[0]))
cv.imshow('light_window', final_visualization)

bump_map = cv.resize(bump_map,  (original_size[1], original_size[0]))
cv.imshow('bump_map_window', bump_map)

cv.waitKey(0)