#!/usr/bin/python

import numpy as np
import math

def objectiveFunction(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    F=0.7854*x1*x2**2*(3.3333*x3**2+14.9334*x3-43.0934)-1.508*x1*(x6**2+x7**2)+0.7854*(x4*x6**2+x5*x7**2)
    return F

def G1(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    F=(27/(x1*x2**2*x3))-1
    return F

def G2(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    F=(397.5/(x1*x2**2*x3**2))-1
    return F

def G3(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    F=((1.93*x4**3)/x2*x3*x6**4)-1
    return F

def G4(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    F=((1.93*x5**3)/x2*x3+x7**4)-1
    return F

def G5(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    F=((math.sqrt((((745*x4)/(x2*x3))**2)+16.9e6))/110*x6**3)-1
    return F

def G6(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    F=((math.sqrt((((745*x5)/(x2*x3))**2)+157.5e6))/85*x7**3)-1
    return F

def G7(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    F=((x2*x3)/40)-1
    return F

def G8(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    F=((5*x2)/(x1))-1
    return F

def G9(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    F=((x1)/(12*x2))-1
    return F

def G10(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    F=((1.5*x6+1.9)/x4)-1
    return F

def G11(x):
    x1,x2,x3,x4,x5,x6,x7 = x
    F=((1.1*x7+1.9)/(x5))-1
    return F