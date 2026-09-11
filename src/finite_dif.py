import numpy as np
import math

def fin_dif_mesh_expl(T, r, K, sigma, M, N):
    S_max = 3 * K
    dt = T / N
    dS = S_max / (M - 1)

    # S-grid
    S = np.arange(M) * dS

    # V-mesh
    V = np.zeros((N + 1, M))

    # Initial condition
    V[-1, :] = np.maximum(S - K, 0)

    # Lower boundary
    for j in range(N + 1):
        V[j, 0] = 0

    # Upper boundary
    for j in range(N + 1):
        V[j, M - 1] = S_max  - K * np.exp(-r * (T - dt * j))

    i_arr = np.arange(1, M - 1)
    a_i = dt * (0.5 * (sigma * i_arr) ** 2 - 0.5 * r * i_arr)
    b_i = 1 - dt * ((sigma * i_arr) ** 2 + r)
    c_i = dt * (0.5 * (sigma * i_arr) ** 2 + 0.5 * r * i_arr)

    for j in range(N - 1, -1, -1):
        V[j, 1:-1] = (a_i * V[j + 1, :-2] + b_i * V[j + 1, 1:-1] + c_i * V[j + 1, 2:])
    return V


def opt_price(S, t, T, r, K, sigma, M, N):
    V_out = 0
    V = fin_dif_mesh_expl(T, r, K, sigma, M, N) 
    S_max = 3 * K
    dt = T / N
    dS = S_max / (M - 1)
    i = t / dt
    j = S / dS

    i_loc = (i % 1 == 0)
    j_loc = (j % 1 == 0)

    i_1 = math.floor(i)
    i_2 = math.ceil(i)
    j_1 = math.floor(j)
    j_2 = math.ceil(j)

    if i_loc and j_loc:
        V_out = V[int(i), int(j)]

    elif i_loc and not j_loc:
        i_id = int(i)
        V_out = V[i_id, j_1] + (V[i_id, j_2] - V[i_id, j_1]) * (j - j_1)

    elif j_loc and not i_loc:
        j_id = int(j)
        V_out = V[i_1, j_id] + (V[i_2, j_id] - V[i_1, j_id]) * (i - i_1)

    elif not j_loc and not i_loc: 
        V_i1 = V[i_1, j_1] + (V[i_1, j_2] - V[i_1, j_1]) * (j - j_1)
        V_i2 = V[i_2, j_1] + (V[i_2, j_2] - V[i_2, j_1]) * (j - j_1)
        V_out = V_i1 + (V_i2 - V_i1) * (i - i_1)

    return V_out