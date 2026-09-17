import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from market_data import get_market_data
from black_scholes import black_scholes_call


def implied_volatility_call(ticker_str, r, q=0.0, target_tau=None):

    _, tau, S, option_chain, call_prices = get_market_data(ticker_str, target_tau)

    strikes = option_chain["strike"].to_numpy()
    market_prices = call_prices.to_numpy()
    n = len(market_prices)
    implied_vols = np.full(n, np.nan)

    # Optimization of every strikeprice
    for i in range(n):
        K = strikes[i]
        C_market = market_prices[i]

        def objective(sigma):
            return black_scholes_call(S, tau, K, r, sigma, q) - C_market

        try:
            implied_vols[i] = brentq(objective, 1e-6, 5.0)
        except ValueError:
            implied_vols[i] = np.nan


    return strikes, implied_vols, tau, S


def plot_vol(strikes, implied_vols, reference=None):
    plt.plot(strikes, implied_vols, color="steelblue",linestyle = " " , marker = ".", linewidth=0.8, label="calculated implied volatility")

    if reference is not None:
        ref_strikes, ref_iv = reference
        plt.plot(ref_strikes, ref_iv, color="red", linewidth=0.8, label="yfinance implied volatility")

    plt.xlabel(r"strike price $K$")
    plt.ylabel(r"implied volatility $\sigma$")
    plt.legend()
    plt.grid()
    plt.show()


