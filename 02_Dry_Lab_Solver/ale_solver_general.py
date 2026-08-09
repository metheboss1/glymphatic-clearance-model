"""
ale_solver_general.py
Phase 5: A generalization of Day 4's ale_solver.py. Day 4's solver only
accepted one specific formula for wall motion (a fixed sinusoid). Today's
Kelvin-Voigt wall model produces a *different*, phase-lagged wall-motion
function, so the solver is generalized to accept ANY R_i(t) (and its time
derivative) as a callable, rather than a hardcoded formula.

This is the same validated physics and numerics as Day 4 -- the boxed
ALE equation from Day 4, Part 1 -- just parameterized more generally.
See test_ale_solver_general.py for the regression test proving this
generalization did not change any previously-validated behavior.
"""

import numpy as np


def compute_flow_rate(u_vals, eta, R_i, R_o):
    """
    Volumetric flow rate Q(t) = integral of u(r)*2*pi*r dr across the
    annulus cross-section, computed from the eta-grid velocity solution.
    """
    r_vals = R_i * (1 - eta) + R_o * eta
    integrand = u_vals * 2 * np.pi * r_vals
    return np.trapezoid(integrand, r_vals)


def solve_ale_general(Ri_func, dRidt_func, R_o, rho, nu, G, omega_heart,
                       n_eta=60, steps_per_period=150, n_periods=8):
    """
    Solves the Day-4-derived ALE momentum equation for an arbitrary wall
    motion Ri_func(t), dRidt_func(t), driven additionally by an optional
    externally-imposed oscillatory axial pressure gradient of amplitude G
    (set G=0 to test wall motion as the ONLY driver -- see Part 3).
    """
    deta = 1.0 / (n_eta + 1)
    eta = np.linspace(deta, 1 - deta, n_eta)
    T = 2 * np.pi / omega_heart
    dt = T / steps_per_period
    N = n_eta

    def build_M(t):
        Ri = Ri_func(t)
        W = R_o - Ri
        r_vals = Ri * (1 - eta) + R_o * eta
        ug = dRidt_func(t) * (1 - eta)
        M = np.zeros((N, N))
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