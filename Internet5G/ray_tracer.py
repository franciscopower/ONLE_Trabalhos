#!/usr/bin/python

import numpy as np
import cv2 as cv
from functools import partial
import math

                            
def calculateIntensity(src_pos, point, power, bump_map):

    # analise das distacias ao scr
    dist=[]



    #???? tem que se corrigir de forma a organizar os vetores d por ordem decresente e que atulize tambem as cordenadas
    for t in range(0, len(src_pos)):
        des=src_pos(t)
        dist.append((des[0]-point[0])**2 + (des[1]-point[1])**2)

        for r in range(0,t):
            if dist[r]<dist[t]:
                dist[r]=dist[t]
                break



    for d in dist:

        #check for obstacles
        line = np.zeros(bump_map.shape)
        line = cv.line(line, src_pos, point, (255), 1)
        intersection_check = line + bump_map
        line_of_sight = intersection_check[:, :].max() <= 255


        if src_pos == point:
            intensity = power
        elif bump_map[point[1],point[0]] != 0:
            intensity = 0
        elif line_of_sight:
            intensity = power / ( 4 * math.pi * d )
            break
        else:
            intensity = 0

    return intensity

def main():

    density=1

    light_window = "Light"
    bump_map_window = "Bump Map"

    bump_map = cv.imread('bump_map2.png', 0)

    cv.imshow(bump_map_window, bump_map)
    original_size = bump_map.shape
    scale_factor = 4

    bump_map = cv.resize(bump_map, (bump_map.shape[1] / scale_factor, bump_map.shape[0] / scale_factor))

    final_visualization = np.zeros(bump_map.shape)
    intensity_values = np.zeros(bump_map.shape)

    power = 100
    # src_pos = (bump_map.shape[1]/2,bump_map.shape[0]/2)
    # density = 2

    # list of position of router

    src_pos=[(30,10), (20, 20), (39,59)]




    intensity_values = np.zeros(bump_map.shape)

    for l in range(0, bump_map.shape[0] - 1, density):
        for c in range(0, bump_map.shape[1] - 1, density):
            intensity = calculateIntensity(src_pos,(c,l), power, bump_map)
            intensity_values[l][c] = intensity

    final_visualization = intensity_values * 255 / power * 10

    final_visualization = cv.resize(final_visualization, (original_size[1], original_size[0]))

    cv.imshow(light_window, final_visualization)

    k = cv.waitKey(0)


cv.waitKey(0)

        
        


if __name__ == '__main__':
    main()
