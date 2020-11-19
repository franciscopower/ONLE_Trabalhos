import numpy as np

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

def rot(angle):
    """Returns 2D rotation matrix

    Args:
        angle (float): angle of rotation, in radians

    Returns:
        numpy.array: rotation matrix
    """
    R = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1],
        ])
    
    return R

def trans(x, y):
    """Returns 3D translation matrix

    Args:
        x (float): increment along x axis
        y (float): increment along y axis

    Returns:
        numpy.array: translation matrix
    """
    T = np.array([
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1],
    ])
    
    return T
