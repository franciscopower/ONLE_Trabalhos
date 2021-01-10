import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import moveObjects
import interpretGCode




def main():
    results = pd.read_csv('impressao3D_iteration_costv3_75.csv')
    x = results.values[4,2:]

    objs = interpretGCode.getObjectsPts('Impressao3D/GCode/')
    trans_list = x.reshape(x.shape[0] / 3, 3)
    newobjs=moveObjects.moveObjects(objs,trans_list)
    moveObjects.showObjects(newobjs)














if __name__ == '__main__':
    main()