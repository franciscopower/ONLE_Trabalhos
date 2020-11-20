#!/usr/bin/python 
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def interpretGCode(path):

    f = open(path, 'r')
    data = f.read()
    f.close()

    line = data.split('\n')
    
    printing = False
    
    all_pts = np.array([
                [],
                [],
                [],
            ])
    
    in_pts = np.array([
                [],
                [],
                [],
            ])
    
    out_pts = np.array([
                [],
                [],
                [],
            ])
    
    pt = np.array([
                [0.0],
                [0.0],
                [0.0],
            ])
    
    
    for i,l in enumerate(line):
        if 'Z0' in l or 'TYPE' in l:
            printing = True
            
        if 'FILL' in l:
            printing = False
            
        if not 'G0' in l and not 'G1' in l:
            continue
            
        if printing:
            word = l.split(' ')
            
            if 'Z' in l and i != 0:
                out_pts = np.append(out_pts, pt, 1)
            
            for w in word:
                if 'X' in w:
                    pt[0,0] = float(w[1:])       
                elif 'Y' in w:
                    pt[1,0] = float(w[1:])        
                elif 'Z' in w:
                    pt[2,0] = float(w[1:])
                    
            if 'Z' in l:
                in_pts = np.append(in_pts, pt, 1)

            all_pts = np.append(all_pts, pt, 1)
    
    out_pts = np.append(out_pts, pt, 1)
    
    return all_pts, in_pts, out_pts    
    
def iterateFiles(directory):
    objs = []
    
    for filename in os.listdir(directory):
        if filename.endswith('.gcode'):
            path = (os.path.join(directory, filename))
            
            all_pts, in_pts, out_pts = interpretGCode(path)
    
            objs.append([all_pts, in_pts, out_pts])
            
    return objs
            
    
        
if __name__ == "__main__":
    
    print(iterateFiles('Impressao3D/GCode/'))
    
    
        
        
        
    # plot points      
    # plt.figure()
    # ax = plt.axes(projection='3d')
    # ax.plot3D(all_pts[0,:], all_pts[1,:], all_pts[2,:])
    # plt.show()