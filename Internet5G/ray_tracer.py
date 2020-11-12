#!/usr/bin/python

import numpy as np
import cv2 as cv
from functools import partial
import math

                            
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

def intensityMatrix():

    light_window = "Light"
    bump_map_window = "Bump Map"
    #load windows
    bump_map = cv.imread('bump_map1.png', 0)
    #show bumpmap
    cv.imshow(bump_map_window, bump_map)
    #downscale bumpmap
    original_size = bump_map.shape
    scale_factor = 4
    bump_map = cv.resize(bump_map, (int(bump_map.shape[1] / scale_factor), int(bump_map.shape[0] / scale_factor)))
    
    density=1
    intensity_values = np.zeros(bump_map.shape)

    #router properties
    power = 100
    # list of position of router
    src_pos=[(30,10), (50, 50), (100,100)]
    # src_pos=[(30,10)]


    # calculate intensity matrix
    for l in range(0, bump_map.shape[0] - 1, density):
        for c in range(0, bump_map.shape[1] - 1, density):
            intensity = calculateIntensity(src_pos,(c,l), power, bump_map)
            intensity_values[l][c] = intensity

    #visualize result
    final_visualization = intensity_values * 255 / power * 10
    final_visualization = cv.resize(final_visualization, (original_size[1], original_size[0]))
    cv.imshow(light_window, final_visualization)

    cv.waitKey(0)

        
        


if __name__ == '__main__':
    intensityMatrix()
