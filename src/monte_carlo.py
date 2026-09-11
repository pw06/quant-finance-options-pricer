import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Monte Carlo simulation
def monte_carlo_func(S, t, T, K, r, sigma, npaths):
    # Variable definition
    N = 252 
    steps = int((T - t) * N)
    dt = (T - t)/steps
    S_mean = np.zeros(steps + 1)
    po_arr = np.zeros(npaths)
    S_a = np.zeros((npaths, steps + 1))

    # Path simulation and payoff logging
    Z = np.random.normal(0, 1, size = (npaths, steps))
    lnr =  ((r - (sigma ** 2)/(2)) * dt  + sigma * np.sqrt(dt) * Z)
    S_a[ : , 0] = S
    S_a[ : , 1: ] = S * np.exp(np.cumsum(lnr, axis = 1))
    po_arr = np.maximum(S_a[:, steps] - K, 0)
    payoff_mean = po_arr.mean()

    # Payoff
    mc_price = payoff_mean * np.exp(r * (t - T))

    # Logging stock price mean
    for x in range(steps + 1):
        S_mean[x] = S_a[:, x].mean()


    return (payoff_mean, mc_price, S_a, S_mean)




    # Plots
def plot_mc(S):
    # Variable definition
    n = len(S)
    st = len(S[0, :])
    S_mean = np.zeros(st)

    # Logging stock price mean
    for x in range(st):
        S_mean[x] = S[:, x].mean()

    for i in range(n):
        plt.plot(range(0, len(S[0, :])), S[i, :], color = "steelblue", linewidth = 0.2)

    plt.plot(range(st), S_mean[range(st)], color = "red")

    legend_gbm = Line2D([], [], color = "steelblue", linewidth = 1, label = f"GBM simulation, n = {n}")
    legend_mean = Line2D([], [], color = "red", linewidth = 1, label = f"Mean Underlying")

    plt.legend(handles = [legend_gbm, legend_mean])
    plt.grid()
    plt.xlabel("tradingdays t")
    plt.ylabel("price underlying S(t) in $")
    plt.show()

