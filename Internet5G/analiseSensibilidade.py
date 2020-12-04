import matplotlib.pyplot as plt

x = [50,60,70,80,90,100]
fx = [0.0145149,0.019427,0.0203423,0.020635779,0.0204007835,0.01899181]

x_o = [110]
fx_o = [0.0053760032]
x_b = [120]
fx_b = [0.0164188861811158]
plt.plot(x, fx)
plt.plot(x_o, fx_o, x_b, fx_b, marker='o')
plt.xlabel('Position x')
plt.ylabel('Objective Function')
plt.show()