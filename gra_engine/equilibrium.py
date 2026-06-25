import numpy as np

def compute_nash_equilibrium(adj, s0, influence_weight, max_iter, epsilon):
    n = adj.shape[0]
    s = s0.copy()
    for _ in range(max_iter):
        s_new = np.zeros(n)
        for i in range(n):
            neighbor_influence = adj[:, i].dot(s)
            s_new[i] = np.clip(s0[i] + influence_weight * neighbor_influence, 0, 1)
        if np.linalg.norm(s_new - s) < epsilon:
            break
        s = s_new
    return s
