import pandas as pd
import numpy as np
import ray_tracer
import cv2 as cv
from InternetObjRestr import objective_function

results = pd.read_csv('internet5G_V3_iteration_cost_3_torres_t1.csv')
x = results.values[0,2:]
x = x.astype(int)
src_pos=x.reshape(x.shape[0]/2,2)

density = 2

# Dados ----------------------
bump_map = cv.imread('Internet5G/bump_map_campusV2.jpg', 0)
restriction_map = cv.imread('Internet5G/restriction_map_campusV2.jpg', 0)

input_maps = np.ndarray((bump_map.shape[0], bump_map.shape[1], 3))
input_maps[:,:,0]=restriction_map - bump_map
input_maps[:,:,1]=0
input_maps[:,:,2]=bump_map

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

intensity_matrix,_,_ = ray_tracer.intensityMatrix(bump_map,src_pos,power, restriction_map, scale_real, density)
# print(intensity_matrix[-1][-3:-1])

funcao_objetivo = objective_function(x, kwargs)
# Print results
print('Objective Function: ' + str(funcao_objetivo))


#visualize result
final_visualization = intensity_matrix * 255 / power *100
final_visualization = cv.resize(final_visualization, (original_size[1], original_size[0]))
# cv.imshow('light_window', final_visualization)

bump_map = cv.resize(bump_map,  (original_size[1], original_size[0]))
# cv.imshow('bump_map_window', bump_map)
restriction_map = cv.resize(restriction_map,  (original_size[1], original_size[0]))
# cv.imshow('restriction_map_window', restriction_map)

heatmap = np.ndarray((bump_map.shape[0], bump_map.shape[1], 3))
heatmap[:,:,2]=bump_map
heatmap[:,:,1]=final_visualization
heatmap[:,:,0]= 0 #restriction_map-bump_map-final_visualization

for pos in src_pos:
    heatmap = cv.circle(heatmap, (pos[0]*scale_factor,pos[1]*scale_factor), 10, (255,255,255), -1)
    
cv.imshow('heatmap', heatmap)
cv.imshow('inputs', input_maps)
cv.imwrite('input_map.png', input_maps)

cv.waitKey(0)