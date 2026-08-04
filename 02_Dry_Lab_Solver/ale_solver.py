"""
ale_solver.py
Phase 4: The true ALE solver. Merges Day 2's moving mesh (R_i(t), grid
speed u_g) with the boxed equation derived in Part 1 above, so the wall
genuinely pulses while the flow is solved.

Unlike Day 3 and Part 2's rigid solvers, the operator matrix here is
NOT constant in time -- r(eta,t), W(t), and u_g(eta,t) all change every
instant the wall moves, so the linear system is rebuilt and re-solved
at every single timestep. This is more expensive than a rigid solve,
but at this grid size (tens of points) it's still fast, and there is no
shortcut around it: an accurate moving-boundary solver has to actually
account for the boundary moving.
"""

import numpy as np


def inner_radius(t, R_i0, a, f):
    omega = 2 * np.pi * f
    return R_i0 * (1 + a * np.sin(omega * t))


def dRi_dt(t, R_i0, a, f):
    omega = 2 * np.pi * f
    return R_i0 * a * omega * np.cos(omega * t)


def solve_ale(R_i0, R_o, a, f, rho, nu, G, n_eta=80,
              steps_per_period=200, n_periods=8):
    """
    Solves the boxed ALE equation from Part 1 on the moving eta-grid.
    Returns a list of (t, u(eta), eta) snapshots from the final period.
    """
    deta = 1.0 / (n_eta + 1)
    eta = np.linspace(deta, 1 - deta, n_eta)   # interior points; walls at eta=0,1
    omega_heart = 2 * np.pi * f
    T = 2 * np.pi / omega_heart
    dt = T / steps_per_period
    N = n_eta

    def build_M(t):
        """Builds the full right-hand-side linear operator (diffusion +
        grid-motion pseudo-convection) at instant t, in eta-space."""
        Ri = inner_radius(t, R_i0, a, f)
        W = R_o - Ri
        r_vals = Ri * (1 - eta) + R_o * eta
        ug = dRi_dt(t, R_i0, a, f) * (1 - eta)

        M = np.zeros((N, N))
        # Diffusion term: nu/(r*W^2) * d/deta( r * du/deta )
        for j in range(N):
            rj = r_vals[j]
            eta_p, eta_m = eta[j] + deta / 2, eta[j] - deta / 2
            r_p = Ri * (1 - eta_p) + R_o * eta_p
            r_m = Ri * (1 - eta_m) + R_o * eta_m
            coef = nu / (rj * W * W * deta * deta)
            if j - 1 >= 0:
                M[j, j - 1] += coef * r_m
            M[j, j] += -coef * (r_p + r_m)
            if j + 1 < N:
                M[j, j + 1] += coef * r_p
        # Grid-motion term: (u_g / W) * du/deta  (central difference)
        for j in range(N):
            c = ug[j] / (W * 2 * deta)
            if j + 1 < N:
                M[j, j + 1] += c
            if j - 1 >= 0:
                M[j, j - 1] += -c
        return M

    u = np.zeros(N)
    t = 0.0
    n_steps = steps_per_period * n_periods
    history = []
    I = np.eye(N)
    for step in range(n_steps):
        M_n, M_np1 = build_M(t), build_M(t + dt)
        f_n = (G / rho) * np.cos(omega_heart * t)
        f_np1 = (G / rho) * np.cos(omega_heart * (t + dt))
        A_impl = I - 0.5 * dt * M_np1
        rhs = (I + 0.5 * dt * M_n).dot(u) + 0.5 * dt * (f_n + f_np1)
        u = np.linalg.solve(A_impl, rhs)
        t += dt
        if step >= n_steps - steps_per_period:
            history.append((t, u.copy(), eta.copy()))
    return history