import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import moveObjects
import interpretGCode
from mpl_toolkits.mplot3d import Axes3D


results = pd.read_csv('impressao3D_iteration_costv3_75.csv')

x = results.values[9,2:]
objs = interpretGCode.getObjectsPts('Impressao3D/GCode/')
trans_list = x.reshape(x.shape[0] / 3, 3)
newobjs=moveObjects.moveObjects(objs,trans_list)
moveObjects.showObjects(newobjs)

