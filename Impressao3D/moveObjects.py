import numpy as np

import interpretGCode

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def rot3(axis, angle):
    """Returns 3D rotation matrix

    Args:
        axis (string): axis around which the rotation will be performed
        angle (float): angle of rotation, in radians

    Returns:
        numpy.array: rotation matrix
    """
    if axis == 'z':
        R = np.array([
            [np.cos(angle), -np.sin(angle), 0, 0],
            [np.sin(angle), np.cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])
    elif axis == 'y':
        R = np.array([
            [np.cos(angle), 0, np.sin(angle), 0, 0],
            [0, 1, 0, 0],
            [-np.sin(angle), 0, np.cos(angle), 0],
            [0, 0, 0, 1],
        ])
    elif axis == 'x':
        R = np.array([
            [1, 0, 0, 0],
            [0, np.cos(angle), -np.sin(angle), 0],
            [0, np.sin(angle), 0, np.cos(angle), 0],
            [0, 0, 0, 1]
        ])
    
    return R

def trans3(x, y, z):
    """Returns 3D translation matrix

    Args:
        x (float): increment along x axis
        y (float): increment along y axis
        z (float): increment along z axis

    Returns:
        numpy.array: translation matrix
    """
    T = np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1],
    ])
    
    return T

def moveObjects(objs, trans_list):
    # [
    #     [x,y, theta],
    #     [x,y, theta],
    #     ...
    # ]
        
    for i,o in enumerate(objs):
        for n,a in enumerate(o):
            t = trans3(trans_list[i][0],trans_list[i][1],0).dot(rot3('z', trans_list[i][2]))
            a_extended = np.append(a, np.ones((1,a.shape[1])), 0)
            new_pos = t.dot(a_extended)
            objs[i][n] = new_pos[0:3,:]
            
    return objs

def showObjects(new_objs):
    # plot points      
    plt.figure()
    ax = plt.axes(projection='3d')
    for o in new_objs:
        ax.plot3D(o[0][0,:], o[0][1,:], o[0][2,:]) 

    ax.set_xlabel('x')
    ax.set_ylabel('y')

    plt.show()


def test():
    objs = interpretGCode.getObjectsPts('Impressao3D/GCode/')
    
    trans_list = [
        [20,0,0],
        [0,20,np.pi/4],
        [20,60,0],
        [-40,50,np.pi/4],
    ]
    
    new_objs = moveObjects(objs, trans_list)
    showObjects(new_objs)
    
    
if __name__ == "__main__":
    test()