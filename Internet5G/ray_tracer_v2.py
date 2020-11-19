#!/usr/bin/python

import math
from functools import partial

import cv2 as cv
import numpy as np

src_pos = [(5, 5), (400,400)]
moving1 = False
moving2 = False
density = 1

def onClick(event, x, y, flags, param):
    global moving1, moving2, src_pos, density
    if event == cv.EVENT_LBUTTONDOWN:
        src_pos[0] = (x,y)
        moving1 = True
    elif event == cv.EVENT_LBUTTONUP:
        src_pos[0] = (x,y)
        density = 1
        moving1 = False
        
    if event == cv.EVENT_RBUTTONDOWN:
        src_pos[1] = (x,y)
        moving2 = True
    elif event == cv.EVENT_RBUTTONUP:
        src_pos[1] = (x,y)
        density = 1
        moving2 = False
    
    if event == cv.EVENT_MOUSEMOVE:
        if moving1:
            src_pos[0] = (x,y)
            density = 2
        elif moving2:
            src_pos[1] = (x,y)
            density = 2
        
def createBumpMapImg(bump_map_pts, bump_map):
    I = np.zeros((bump_map.shape[0],bump_map.shape[1]))
    
    for p1,p2 in bump_map_pts:
        I = cv.line(I, p1, p2, (255), 2)
    
    return I
        
                            
def calculateIntensity(src_pos, point, power, bump_map):
    line_of_sight = False

    # analise das distacias ao scr
    pt_dist = np.zeros((len(src_pos),3))

    #add distances to points
    for i,t in enumerate(src_pos):
        pt_dist[i,:] = [t[0], t[1], ((t[0]-point[0])**2 + (t[1]-point[1])**2)]
        
    # sort distances and points:
    pt_dist = pt_dist[np.lexsort((pt_dist[:,2], ))]

    for d in range(0,pt_dist.shape[0]):
        # coordinates of source
        x = int(pt_dist[d][0])
        y = int(pt_dist[d][1])

        #! Altered osbtacle check algorithm ------------------
        #check for obstacles
        for p1,p2 in bump_map:
            x1 = p1[0]
            y1 = p1[1]
            x2 = p2[0]
            y2 = p2[1]
            x3 = x
            y3 = y
            x4 = point[0]
            y4 = point[1]
            
            if ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)) == 0:
                line_of_sight = True
                continue
            
            t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4))/((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
            u = - ((x1-x2)*(y1-y3) - (y1-y2)*(x1-x3))/((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
            
            if t>=0 and t<=1 and u>=0 and u<=1:
                line_of_sight = False
                break
            else:
                line_of_sight = True
        
        
        #! -----------------------------------------------------
        
                
        if (x,y) == (point):
            intensity = power
        elif line_of_sight:
            intensity = power / ( 4 * math.pi * pt_dist[d][2] )
            break
        else:
            intensity = 0

    return intensity

def result_objctive_function(bump_map,matiz):
    _, bump_map_ths = cv.threshold(bump_map, 5, 255, cv.THRESH_BINARY_INV)

    aria_disponivel = np.sum(bump_map_ths / 255)

    intensidade_total = np.sum(matiz)

    funcao_objtivo = intensidade_total / aria_disponivel

    return funcao_objtivo

def intensityMatrix():
    light_window = "Light"
    bump_map_window = "Bump Map"
    
    # bump_map = cv.imread('bump_map2.png',0)
    bump_map = np.zeros((500,300,3))
    #! pairs of points that for lines of bump map
    bump_map_pts = [[(75, 88), (219, 143)], [(174, 238), (77, 357)]] 
    
    original_size = bump_map.shape
    scale_factor = 1
    
    bump_map = cv.resize(bump_map, (int(bump_map.shape[1]/scale_factor), int(bump_map.shape[0]/scale_factor)))
    for i,p in enumerate(bump_map_pts):
        p1 = p[0]
        p2 = p[1]
        p1 = (p1[0]/scale_factor, p1[1]/scale_factor)
        p2 = (p2[0]/scale_factor, p2[1]/scale_factor)
        bump_map_pts[i] = [p1, p2]
    
    bump_map = createBumpMapImg(bump_map_pts, bump_map)
    cv.imshow(bump_map_window, bump_map)
    
    final_visualization = np.zeros(bump_map.shape)
    intensity_values = np.zeros(bump_map.shape)
    
    power = 100
    # src_pos = (bump_map.shape[1]/2,bump_map.shape[0]/2)
    # density = 2
      
    k = ''
    while k != ord('q'):
                
        cv.setMouseCallback(light_window, onClick)
        
        intensity_values = np.zeros(bump_map.shape)
        
        # src_pos_scaled = src_pos
        src_pos_scaled = [(int(src_pos[0][0]/scale_factor),int(src_pos[0][1]/scale_factor))] #,(int(src_pos[1][0]/scale_factor),int(src_pos[1][1]/scale_factor))]
        # for i,pos in enumerate(src_pos):
        #     x_scaled = int(pos[0]/scale_factor)
        #     y_scaled = int(pos[1]/scale_factor)
        #     src_pos_scaled[i] = (x_scaled, y_scaled)
            

        for l in range(0,bump_map.shape[0]-1,density):
            for c in range(0,bump_map.shape[1]-1,density):
                intensity = calculateIntensity(src_pos_scaled, (c,l), power, bump_map_pts) #! changed bump_map to bump_map_pts
                intensity_values[l][c] = intensity
                
        final_visualization = intensity_values*255/power *10

        final_visualization = cv.resize(final_visualization, (original_size[1], original_size[0]))
        bump_map = cv.resize(bump_map, (original_size[1], original_size[0]))

        final_visualization = bump_map + final_visualization
        cv.imshow(light_window, final_visualization) 
        
        if k == ord('r'):
            print(result_objctive_function(bump_map, intensity_values))

        k = cv.waitKey(1)

        


if __name__ == '__main__':
    intensityMatrix()
