import numpy as np
from scipy.special import erf


def phi(x):


    return 0.5 * (1 + erf(x / np.sqrt(2)))


def var_phi(x):


    return 1 / np.sqrt(2 * np.pi) * np.exp(-(x**2) / 2)


def d1(S, tau, K, r, sigma, q=0):


    return (np.log(S / K) + (r - q + sigma**2 / 2) * tau) / (sigma * np.sqrt(tau))


def d2(S, tau, K, r, sigma, q=0):


    return d1(S, tau, K, r, sigma, q) - sigma * np.sqrt(tau)


# Black-Scholes Call Price
def black_scholes_call(S, tau, K, r, sigma, q=0):
    d_1 = d1(S, tau, K, r, sigma, q)
    d_2 = d2(S, tau, K, r, sigma, q)

    call_price = (S * np.exp(-q * tau) * phi(d_1) - K * np.exp(-r * tau) * phi(d_2))


    return call_price


# Greeks

def delta_c(S, tau, K, r, sigma, q=0):
    d_1 = d1(S, tau, K, r, sigma, q)


    return np.exp(-q * tau) * phi(d_1)


def gamma(S, tau, K, r, sigma, q=0):
    d_1 = d1(S, tau, K, r, sigma, q)


    return (np.exp(-q * tau) * var_phi(d_1) / (S * sigma * np.sqrt(tau)))


def vega(S, tau, K, r, sigma, q=0):
    d_1 = d1(S, tau, K, r, sigma, q)


    return (S * np.exp(-q * tau) * var_phi(d_1) * np.sqrt(tau))


def theta_c(S, tau, K, r, sigma, q=0):
    d_1 = d1(S, tau, K, r, sigma, q)
    d_2 = d2(S, tau, K, r, sigma, q)

    x1 = (S * np.exp(-q * tau) * var_phi(d_1) * sigma / (2 * np.sqrt(tau)))
    x2 = r * K * np.exp(-r * tau) * phi(d_2)
    x3 = q * S * np.exp(-q * tau) * phi(d_1)


    return -(x1 + x2) + x3


def rho_c(S, tau, K, r, sigma, q=0):
    d_2 = d2(S, tau, K, r, sigma, q)


    return (tau * K * np.exp(-r * tau) * phi(d_2))


def omega_c(S, tau, K, r, sigma, q=0):
    d_1 = d1(S, tau, K, r, sigma, q)


    return (S * np.exp(-q * tau) * phi(d_1) / black_scholes_call(S, tau, K, r, sigma, q))