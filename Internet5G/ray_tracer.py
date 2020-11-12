#!/user/bin/python

import numpy as np
import cv2 as cv
from functools import partial
import math

p1 = None
p2 = None
drawing = False
point = (200,200)
                            
def calculateIntensity(src_pos, point, power, bump_map):
    
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
        intensity = power / ( 4 * math.pi * ((src_pos[0]-point[0])**2 + (src_pos[1]-point[1])**2) )
    else:
        intensity = 0
        
    return intensity

def main():
    window_name = "window"
    
    bump_map = cv.imread('teste.png',0)
    bump_map = cv.resize(bump_map, (100,100))
    
    final_visualization = np.zeros(bump_map.shape)
    intensity_values = np.zeros(bump_map.shape)
    
    power = 10000
    src_pos = (bump_map.shape[1]/2,bump_map.shape[0]/2)
    density = 1
    
    cv.imshow(window_name, bump_map)
    
    for l in range(0,bump_map.shape[0],density):
        for c in range(0,bump_map.shape[1],density):
            intensity = calculateIntensity(src_pos, (c,l), power, bump_map)
            intensity_values[l][c] = intensity
            
    final_visualization = intensity_values*255*4*math.pi/power
    
    bump_map = cv.resize(bump_map, (500,500))
    final_visualization = cv.resize(final_visualization, (500,500))
    cv.imshow(window_name, final_visualization)    
    cv.imshow('bump map', bump_map)
    
    # cv.imwrite('Ray_tracer_test', final_visualization)
    # cv.resizeWindow('bump map', 600,600)
    
      
    cv.waitKey(0)

        
        


if __name__ == '__main__':
    main()
