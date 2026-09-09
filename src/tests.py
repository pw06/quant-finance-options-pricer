import numpy as np
import matplotlib.pyplot as plt
from monte_carlo import *
from black_scholes import * 
import time

# Convergence of Monte-Carlo Call Price towards Analytical Solution via Black Scholes using GBM
def mc_bs_conv(S, t, T, K, r, sigma):
    x = [1, 10, 100, 1000, 5000, 10000, 15000, 20000, 30000, 40000, 50000]
    dif = np.zeros(len(x))
    ana_price = black_scholes_call(S, t, T, K, r, sigma)
    print(f"Call price via Black-Scholes: {ana_price:.2f}")
    for i in range(len(x)):
        start = time.time()
        sim_price = monte_carlo_func(S, t, T, K ,r , sigma, x[i])[1]
        dif[i] = np.abs(ana_price - sim_price)
        end = time.time()
        print(f"Absolute value of difference: {dif[i]} seconds")
        print(f"Time needed for simulation: {end - start:.2f}")
    plt.plot(x, dif[range(len(x))], marker = ".", linestyle = "none", color = "steelblue", label = "Difference between Black-Scholes and Monte-Carlo")
    plt.grid()
    plt.legend()
    plt.show()

       
