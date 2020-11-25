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
        [20,60,0],
        [-40,50,np.pi/4],
    ]
    
    new_objs = moveObjects(objs, trans_list)
    
    # plot points      
    plt.figure()
    ax = plt.axes(projection='3d')
    for o in new_objs:
        ax.plot3D(o[0][0,:], o[0][1,:], o[0][2,:]) 

    ax.set_xlabel('x')
    ax.set_ylabel('y')

    plt.show()
    
if __name__ == "__main__":
    test()