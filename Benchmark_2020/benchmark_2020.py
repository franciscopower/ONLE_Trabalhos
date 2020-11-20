#!/usr/bin/python

import numpy as np
import math

X1=0
X2=0
X3=0
X4=0
X5=0
X6=0
X7=0

def objectiveFunction(X1,X2,X3,X4,X5,X6,X7):
    F=0.7854*X1*X2**2*(3.3333*X3**2+14.9334*X3-43.0934)-1.508*X1*(X6**2+X7**2)+0.7854*(X4*X6**2+X5*X7**2)
    return F

def G1(X1,X2,X3):
    F=(27/(X1*X2**2*X3))-1
    return F

def G2(x1,x2,x3):
    F=(397.5/(x1*x2**2*x3**2))-1
    return F

def G3(x2,x3,x4,x6):
    F=((1.93*x4**3)/x2*x3*x6**4)-1
    return F

def G4(x5,x2,x3,x7):
    F=((1.93*x5**3)/x2*x3+x7**4)-1
    return F

def G5(x2,x3,x4,x6):
    F=((math.sqrt((((745*x4)/(x2*x3))**2)+16.9e6))/110*x6**3)-1
    return F

def G6(x2,x3,x5,x7):
    F=((math.sqrt((((745*x5)/(x2*x3))**2)+157.5e6))/85*x7**3)-1
    return F

def G7(x2,x3):
    F=((x2*x3)/40)-1
    return F

def G8(x1,x2):
    F=((5*x2)/(x1))-1
    return F

def G9(x1,x2):
    F=((x1)/(12*x2))-1
    return F

def G10(x4,x6):
    F=((1.5*x6+1.9)/x4)-1
    return F

def G11(x5,x7):
    F=((1.1*x7+1.9)/(x5))-1
    return F