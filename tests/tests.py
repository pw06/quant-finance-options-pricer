import sys
from pathlib import Path
src_path = Path(__file__).resolve().parent.parent / "src"
sys.path.append(str(src_path))

import numpy as np
import matplotlib.pyplot as plt
from black_scholes import black_scholes_call
from monte_carlo import monte_carlo_func, plot_mc
from finite_dif import opt_price
import time

# Convergence of Monte-Carlo Call Price towards Analytical Solution via Black Scholes using GBM
def mc_bs_conv(S, t, T, K, r, sigma):
    x = [1, 10, 100, 1000, 5000, 10000, 15000, 20000, 30000, 40000, 50000]
    dif = np.zeros(len(x))
    ana_price = black_scholes_call(S, t, T, K, r, sigma)
    print(f"Call price via Black-Scholes: {ana_price:.2f}")
    for i in range(len(x)):
        start = time.time()
        tup = monte_carlo_func(S, t, T, K ,r , sigma, x[i])
        sim_price = tup[1]
        dif[i] = np.abs(ana_price - sim_price)
        plot_mc(tup[2])
        end = time.time()
        print(f"Absolute value of difference: {dif[i]:.3f} $")
        print(f"Time needed for simulation: {end - start:.2f} seconds")
    plt.plot(x, dif[range(len(x))], marker = ".", linestyle = "none", color = "steelblue", label = "Difference between Black-Scholes and Monte-Carlo")
    plt.grid()
    plt.legend()
    plt.show()

#Convergence of numerical solution of Black Scholes towards its analytical solution
def fd_bs_conv(S, t, T, r, K, sigma):
    x = [10, 20, 50, 100, 200, 500, 1000]
    dif = np.zeros(len(x))
    ana_price = black_scholes_call(S, t, T, K, r, sigma)
    print(f"Analytical BS price: {ana_price:.6f}")
    for i in range(len(x)):
        start = time.time()
        num_price = opt_price(S, t, T, r, K, sigma, x[i], x[i] ** 2)
        stop = time.time()
        dif[i] = np.abs(ana_price - num_price)
        print(f"FD price: {num_price:.6f}")
        print(f"Absolute value of difference: {dif[i]:.3f} $")
        print(f"Time needed for solution of numerical method: {stop - start:.2f} seconds")
    plt.plot(x, dif[range(len(x))], marker = ".", linestyle = "none", color = "steelblue", label = "Difference between Analytical and Numerical Solution")
    plt.grid()
    plt.legend()
    plt.show()

def fd_mc_bs(S, t, T, r, K, sigma):
    mc_in = [10, 100, 1000, 5000, 10000, 15000, 25000, 50000]
    fd_in = [10, 50, 100, 250, 500, 750, 1000, 1500]
    mc_price = np.zeros(len(mc_in))
    fd_price = np.zeros(len(fd_in))

    ana_price = black_scholes_call(S, t, T, K, r, sigma)

    for i in range(len(mc_in)):
        mc_price[i] = monte_carlo_func(S, t, T, K, r, sigma, mc_in[i])[1]
        print("mc:", mc_in[i])

    for i in range(len(fd_in)):
        fd_price[i] = opt_price(S, t, T, r, K, sigma, fd_in[i], fd_in[i] ** 2)
        print("fd:", fd_in[i])

    plt.axhline(y=ana_price, color="steelblue", label = "Black-Scholes analytical")
    plt.plot(range(1, len(fd_price) + 1), fd_price, color = "red", marker = ".", linestyle = "none", label = "Black-Scholes numerical")
    plt.plot(range(1, len(mc_price) + 1), mc_price, color = "green", marker = ".", linestyle = "none", label = "Monte-Carlo")
    plt.legend()
    plt.grid()
    plt.xlabel("array intervals")
    plt.ylabel("call price in $")
    plt.show()
