import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from market_data import get_market_data
from black_scholes import black_scholes_call
from scipy.interpolate import griddata
from matplotlib.colors import LightSource
import yfinance as yf


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

def implied_vol_iter(iterations):
    dataset = {}
    for iteration in range(1, iterations + 2):
        target_tau = iteration / (iterations + 2)
        dataset[target_tau] = implied_volatility_call(ticker_str = "^SPX",r = 0.05, target_tau= target_tau)
        print(f"processed tau: {target_tau}")
    return dataset






def plot_vol3D(iterations, vert_exag=10, stock_ticker = None):
    stock_price = 0
    stock_data = 0
    data = implied_vol_iter(iterations)

    if stock_ticker != None:
        stock_data = yf.Ticker(stock_ticker).history()
        stock_price = stock_data["Close"].iloc[-1]
        

    tau_list, strike_list, vol_list = [], [], []

    for target_tau, (strikes, vols, tau, S) in data.items():
        mask = ~np.isnan(vols)
        tau_list.extend([tau] * mask.sum())
        strike_list.extend(strikes[mask])
        vol_list.extend(vols[mask])

    if iterations < 2:
        raise ValueError("Zu wenige Laufzeiten")
        return

    # Grids for the surface
    K_grid = np.linspace(min(strike_list), max(strike_list), 120)
    T_grid = np.linspace(min(tau_list), max(tau_list), 60)
    KK, TT = np.meshgrid(K_grid, T_grid)

    VV_lin = griddata((strike_list, tau_list), vol_list, (KK, TT), method="linear")
    VV_near = griddata((strike_list, tau_list), vol_list, (KK, TT), method="nearest")
    VV = np.where(np.isnan(VV_lin), VV_near, VV_lin)

    # Grids for spotprice plane
    z_min, z_max = np.nanmin(VV), np.nanmax(VV)
    t_plane, vol_plane = np.meshgrid(np.linspace(min(tau_list), max(tau_list), 2), np.linspace(z_min, z_max, 2))



    # Plot 
    ax = plt.figure().add_subplot(projection='3d')
    if stock_price != 0: 
        ax.plot_surface([stock_price, stock_price], t_plane, vol_plane, edgecolor = "red", lw=0.5, rstride=8, cstride=8, alpha=0.3, label = f"At the money S ={stock_price}")

    ls = LightSource()
    rgb = ls.shade(VV, cmap=plt.colormaps["gist_earth"], vert_exag=0.1, blend_mode='soft')
    ax.plot_surface(KK, TT, VV, rstride=1, cstride=1, facecolors=rgb, linewidth=0, antialiased=False, shade=False)
    ax.set(xlabel = "Strike price K", ylabel = r"Time to maturity $\tau $", zlabel = "Calculated implied volatility $\sigma$")
    plt.show()

