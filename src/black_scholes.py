import numpy as np
from scipy.special import erf


def phi(x):
    return 0.5 * (1 + erf(x / np.sqrt(2)))


def var_phi(x):
    return 1 / np.sqrt(2 * np.pi) * np.exp(-(x**2) / 2)


def d1(S, tau, K, r, sigma):
    return (
        np.log(S / K) + (r + sigma**2 / 2) * tau
    ) / (sigma * np.sqrt(tau))


def d2(S, tau, K, r, sigma):
    return d1(S, tau, K, r, sigma) - sigma * np.sqrt(tau)


# Black-Scholes Call Price
def black_scholes_call(S, tau, K, r, sigma):
    d_1 = d1(S, tau, K, r, sigma)
    d_2 = d2(S, tau, K, r, sigma)

    call_price = (
        S * phi(d_1)
        - K * np.exp(-r * tau) * phi(d_2)
    )

    return call_price


# Greeks

def delta_c(S, tau, K, r, sigma):
    d_1 = d1(S, tau, K, r, sigma)

    return phi(d_1)


def gamma(S, tau, K, r, sigma):
    d_1 = d1(S, tau, K, r, sigma)

    return var_phi(d_1) / (S * sigma * np.sqrt(tau))


def vega(S, tau, K, r, sigma):
    d_1 = d1(S, tau, K, r, sigma)

    return S * var_phi(d_1) * np.sqrt(tau)


def theta_c(S, tau, K, r, sigma):
    d_1 = d1(S, tau, K, r, sigma)
    d_2 = d2(S, tau, K, r, sigma)

    x1 = S * var_phi(d_1) * sigma / (2 * np.sqrt(tau))
    x2 = r * K * np.exp(-r * tau) * phi(d_2)

    return -(x1 + x2)


def rho_c(S, tau, K, r, sigma):
    d_2 = d2(S, tau, K, r, sigma)

    return tau * K * np.exp(-r * tau) * phi(d_2)


def omega_c(S, tau, K, r, sigma):
    d_1 = d1(S, tau, K, r, sigma)

    return (
        phi(d_1) * S
        / black_scholes_call(S, tau, K, r, sigma)
    )