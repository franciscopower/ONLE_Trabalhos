import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

# a=np.array([1,2,3,4,5])
# b=np.random.rand(5)

# df = pd.DataFrame({'A':a,'B':b})
# print(df)

# df.to_csv('test.csv')

# columns = ['x'+str(n+1) for n in range(7)]
# columns = ['cost'] + columns

# print(columns)

# data = np.zeros((3,4))
# a = np.array([7,8,9])

# data[2][1:] = a

# print(data[2][1:])
# print(data)

a = np.array([
    [1,2,3,4], 
    [4,3,2,4], 
    [1,1,1,1]
])

print(np.where(a < 2)[0].shape[0])