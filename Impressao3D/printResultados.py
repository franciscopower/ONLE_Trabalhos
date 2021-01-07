import pandas as pd
import numpy as np







def main():
    results = pd.read_csv('impressao3D_iteration_cost.csv')
    pos = results.values[1,2:]
    print(pos)


def showObjects(new_objs):
    # plot points
    plt.figure()
    ax = plt.axes(projection='3d')
    for o in new_objs:
        ax.plot3D(o[0][0,:], o[0][1,:], o[0][2,:])

    ax.set_xlabel('x')
    ax.set_ylabel('y')

    plt.show()

if __name__ == '__main__':
    main()