from black_scholes import black_scholes_call, vega
from market_data import get_market_data
import numpy as np
import matplotlib.pyplot as plt

def implied_vol(str_ticker: str, r, n = 100, tol = 1e-8):
    data = get_market_data(str_ticker)


    tau = data[1]
    S = data[2]
    option_chain = data[3]
    call_price_list = data[4]

    plt_in = np.zeros((2, len(call_price_list)))



    
    for i, C_market in enumerate(call_price_list):

        sigma = 0.5
        K = option_chain["strike"].iloc[i]

        for run in range(n):
            C_calc = black_scholes_call(S, tau, K, r, sigma)
            error = C_calc - C_market
            if abs(error) < tol:
                break

            vega_val = vega(S, tau, K, r, sigma)

            if abs(vega_val) < 1e-10:
                print(f"Vega too small for Newton-Raphson.\nVega value: {vega_val}\nSigma value: {sigma}\nMarket value: {C_market}")
                break
            
            sigma = sigma - (error) / vega_val
            if sigma <= 0:
                print(f"Invalid sigma = {sigma} for K = {K}")
                break
        plt_in[0, i] = K
        plt_in[1, i] = sigma
        i += 1


    return plt_in

def plot_vol(plt_in):
    plt.plot(plt_in[0, :], plt_in[1, :], color = "steelblue", linewidth = 0.8, label = "Calculated implied volatility")
    plt.xlabel(r"strike price $K$")
    plt.ylabel(r"implied volatility $\sigma$")
    plt.grid()
    plt.show()

plot_vol(implied_vol("^SPX", 0.05))