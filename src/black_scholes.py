import numpy as np
from scipy.special import erf

def phi(x):
    return 0.5 * (1 + erf(x / np.sqrt(2)))

def var_phi(x):
    return 1/np.sqrt(2 * np.pi()) * np.exp(-(x**2)/2)

# Black-Scholes call price
def black_scholes_call(S, t, T, K, r, sigma):
    d1 = (np.ln(S/K) + (r + (sigma**2)/(2))*(T - t))/(sigma * np.sqrt(T - t))
    d2 = d1 - sigma * np.sqrt(T - t)

    call_price = S * phi(d1) - K * np.exp(-r * (T - t)) * phi(d2)

    return call_price

# Implementation of greeks (riskmanagement)

def delta_c(S, t, T, K, r, sigma):
    d1 = (np.ln(S/K) + (r + (sigma**2)/(2))*(T - t))/(sigma * np.sqrt(T - t))

    return phi(d1)

def gamma(S, t, T, K, r, sigma):
    d1 = (np.ln(S/K) + (r + (sigma**2)/(2))*(T - t))/(sigma * np.sqrt(T - t))

    return (var_phi(d1))/(S * sigma * np.sqrt(T - t))

def vega(S, t, T, K, r, sigma):
    d1 = (np.ln(S/K) + (r + (sigma**2)/(2))*(T - t))/(sigma * np.sqrt(T - t))
    
    return S * var_phi(d1) * np.sqrt(T - t)

def theta_c(S, t, T, K, r, sigma):
    d1 = (np.ln(S/K) + (r + (sigma **2 )/(2))*(T - t))/(sigma * np.sqrt(T - t))
    d2 = d1 - sigma * np.sqrt(T - t)

    x1 = (S * var_phi(d1) * sigma)/(2 * np.sqrt(T - t))
    x2 = r * K * np.exp(-r * (T - t)) * phi(d2)
    return -(x1 + x2)

def rho_c(S, t, T, K, r, sigma):
    d1 = (np.ln(S/K) + (r + (sigma **2 )/(2))*(T - t))/(sigma * np.sqrt(T - t))
    d2 = d1 - sigma * np.sqrt(T - t)

    return(T - t) * K * np.exp(-r * (T - t)) * phi(d2)

def omega_c(S, t, T, K, r, sigma):
    d1 = (np.ln(S/K) + (r + (sigma **2 )/(2))*(T - t))/(sigma * np.sqrt(T - t))
    d2 = d1 - sigma * np.sqrt(T - t)

    return phi(d1) * (S)/(black_scholes_call(S, t, T, K, r, sigma))

