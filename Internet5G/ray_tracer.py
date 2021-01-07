#!/usr/bin/python

import numpy as np
import cv2 as cv
from functools import partial
import math

                            
def calculateIntensity(src_pos, point, power, bump_map, restriction_map, scale_real):

    # analise das distacias ao scr
    pt_dist = np.zeros((len(src_pos),3))

    #add distances to points
    for i,t in enumerate(src_pos):
        if restriction_map[t[1],t[0]] != 255:
            pt_dist[i,:] = [t[0], t[1], ((t[0]-point[0])**2 + (t[1]-point[1])**2)*scale_real] #! avaliar o efeito do scale factor
        else:
            pt_dist[i,:] = [t[0], t[1], np.inf] #caso a torre esteja em area proibida

        
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

def intensityMatrix(bump_map,src_pos,power, restriction_map, scale_real):
    
    density=2
    intensity_values = np.zeros(bump_map.shape)

    # calculate intensity matrix
    for l in range(0, bump_map.shape[0] - 1, density):
        for c in range(0, bump_map.shape[1] - 1, density):
            intensity = calculateIntensity(src_pos,(c,l), power, bump_map, restriction_map, scale_real)
            intensity_values[l][c] = intensity

    return (intensity_values)