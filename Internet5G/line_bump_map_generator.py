import numpy as np
import cv2 as cv
from functools import partial

p1 = None
p2 = None
drawing = False
bump_map_pts = []
    
def onMouse(event, x, y, flag, param, I):
    global p1, p2, drawing, bump_map_pts
        
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        p1 = (x,y)
        print('-----------')
        print(p1)
    
    if event == cv.EVENT_LBUTTONUP:
        drawing = False
        p2 = (x,y)
        print(p2)
        I = cv.line(I, p1, p2, (255,255,255), 2)
        cv.imshow('Image', I)
        bump_map_pts.append([p1,p2])
        
    if event == cv.EVENT_MOUSEMOVE:
        if drawing:
            p2 = (x,y)
            # print(p2)
            A = I.copy()
            A = cv.line(A, p1, p2, (255,255,255), 2)
            cv.imshow('Image', A)

def main():

    # I = cv.imread('img/atlascar2.png')
    I = np.zeros((500,300,3))
    
    cv.imshow('Image', I)
    
    myOnMouse = partial(onMouse, I=I)
    
    cv.setMouseCallback('Image', myOnMouse)
    
    cv.waitKey(0)
    
    print(bump_map_pts)


if __name__ == '__main__':
    main()