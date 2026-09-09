import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Stock Price simulation using GBM
def stock_price_func(S0, t, T, r, sigma, x):
    N = 252 
    dt = (T - t)/N
    Z = np.random.normal(0, 1)

    return S0 * np.exp((r - (sigma ** 2)/(2)) * dt  + sigma * np.sqrt(dt) * Z)

# Monte Carlo simulation
def monte_carlo_func(S, t, T, K, r, sigma, npaths):
    N = 252 
    steps = int((T - t) * N)
    S_arr = np.zeros((npaths, steps + 1))
    S_mean = np.zeros(steps + 1)
    po_arr = np.zeros(npaths)

    # Path simulation and payoff logging
    for i in range(npaths):
        S0 = S
        S_arr[(i, 0)] = S0
        for x in range(1, steps + 1):
            S_arr[(i, x)] = stock_price_func(S_arr[i, x - 1], t, T, r, sigma, x)
        po_arr[i] = np.maximum(S_arr[i, steps] - K, 0)

        plt.plot(range(steps + 1), S_arr[i,range(steps + 1)], color = "steelblue", linewidth = "0.1")

    # Plot
    for x in range(steps + 1):
        S_mean[x] = S_arr[:, x].mean()
    print(S_mean[steps])
    plt.plot(range(steps + 1), S_mean[range(steps + 1)], color = "red")
    legend_gbm = Line2D([], [], color = "steelblue", linewidth = 1, label = f"GBM simulation, n = {npaths}")
    legend_mean = Line2D([], [], color = "red", linewidth = 1, label = f"Mean Underlying")
    plt.legend(handles = [legend_gbm, legend_mean])
    plt.grid()
    plt.xlabel("tradingdays t")
    plt.ylabel("price Underlying S(t)")
    plt.show()

    # Payoff
    payoff_mean = po_arr.mean()
    mc_price = payoff_mean * np.exp(r * (t - T))
    print(f"expected payoff: {payoff_mean:.2f}$ \nMonte Carlo call price: {mc_price:.2f}$")
    return (payoff_mean, mc_price)




