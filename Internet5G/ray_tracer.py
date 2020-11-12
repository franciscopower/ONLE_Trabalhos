#!/user/bin/python

import numpy as np
import cv2 as cv
from functools import partial
import math

src_pos = (5, 5)
moving = False
density = 1

def onClick(event, x, y, flags, param):
    global moving, src_pos, density
    if event == cv.EVENT_LBUTTONDOWN:
        src_pos = (x,y)
        moving = True
    elif event == cv.EVENT_LBUTTONUP:
        src_pos = (x,y)
        density = 1
        moving = False
    
    if event == cv.EVENT_MOUSEMOVE and moving:
        src_pos = (x,y)
        density = 2
        
                            
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
    light_window = "Light"
    bump_map_window = "Bump Map"
    
    bump_map = cv.imread('bump_map2.png',0)
    
    cv.imshow(bump_map_window, bump_map)
    original_size = bump_map.shape
    scale_factor = 4
    
    bump_map = cv.resize(bump_map, (bump_map.shape[1]/scale_factor, bump_map.shape[0]/scale_factor))
    
    final_visualization = np.zeros(bump_map.shape)
    intensity_values = np.zeros(bump_map.shape)
    
    power = 100
    # src_pos = (bump_map.shape[1]/2,bump_map.shape[0]/2)
    # density = 2
      
    k = ''
    while k != ord('q'):
                
        cv.setMouseCallback(light_window, onClick)
        
        intensity_values = np.zeros(bump_map.shape)

        for l in range(0,bump_map.shape[0]-1,density):
            for c in range(0,bump_map.shape[1]-1,density):
                intensity = calculateIntensity((src_pos[0]/scale_factor, src_pos[1]/scale_factor), (c,l), power, bump_map)
                intensity_values[l][c] = intensity
                
        final_visualization = intensity_values*255/power *10

        final_visualization = cv.resize(final_visualization, (original_size[1], original_size[0]))

        cv.imshow(light_window, final_visualization)    

        k = cv.waitKey(1)

        
        


if __name__ == '__main__':
    main()
