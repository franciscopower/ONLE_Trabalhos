import numpy as np
import transform

import interpretGCode

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def moveObjects(objs, trans_list):
    # [
    #     [x,y, theta],
    #     [x,y, theta],
    #     ...
    # ]
        
    for i,o in enumerate(objs):
        for n,a in enumerate(o):
            t = transform.trans3(trans_list[i][0],trans_list[i][1],0).dot(transform.rot3('z', trans_list[i][2]))
            a_extended = np.append(a, np.ones((1,a.shape[1])), 0)
            new_pos = t.dot(a_extended)
            objs[i][n] = new_pos[0:3,:]
            
    return objs


def test():
    objs = interpretGCode.getObjectsPts('Impressao3D/GCode/')
    
    trans_list = [
        [20,0,0],
        [0,20,np.pi/4],
        [20,20,0],
        [0,0,0],
    ]
    
    new_objs = moveObjects(objs, trans_list)
    print(len(new_objs))
    
    all_pts = new_objs[1][0]
    print(all_pts.shape)
    
    # plot points      
    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(all_pts[0,:], all_pts[1,:], all_pts[2,:]) 
    plt.show()
    
if __name__ == "__main__":
    test()