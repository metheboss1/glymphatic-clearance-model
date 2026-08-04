"""
annular_womersley_solver.py
Phase 3.5: The classical Womersley solution for a RIGID annulus (both
walls fixed) -- closing the gap Day 3's single-pipe test left open,
since a pipe has no inner wall to validate against.
"""

import numpy as np
from scipy.special import jv, yv


def annular_womersley_analytic(r, t, R_i, R_o, rho, nu, omega, G):
    """
    Classical Womersley solution for oscillatory flow in a rigid annulus
    (R_i <= r <= R_o, both walls no-slip), driven by dp/dz(t)=-G*cos(omega*t).
    Both J0 and Y0 are needed because the domain excludes r=0 (unlike the
    single-pipe case), so both are finite and both are required to satisfy
    two boundary conditions instead of one.
    """
    k = np.exp(1j * 3 * np.pi / 4) * np.sqrt(omega / nu)   # i^(3/2) sqrt(omega/nu)
    U_p = G / (1j * omega * rho)
    A = np.array([[jv(0, k * R_i), yv(0, k * R_i)],
                  [jv(0, k * R_o), yv(0, k * R_o)]], dtype=complex)
    b = np.array([-U_p, -U_p], dtype=complex)
    C1, C2 = np.linalg.solve(A, b)
    U = U_p + C1 * jv(0, k * r) + C2 * yv(0, k * r)
    return np.real(U * np.exp(1j * omega * t))


def solve_annulus_rigid_fd(R_i, R_o, rho, nu, omega, G, n_r=80,
                            steps_per_period=200, n_periods=8):
    """
    Implicit (Crank-Nicolson) finite-difference solver for the same
    equation on a FIXED annular grid (both walls stationary) -- the
    numerical counterpart validated against annular_womersley_analytic.
    """
    dr = (R_o - R_i) / (n_r + 1)
    r_full = np.linspace(R_i, R_o, n_r + 2)   # includes both wall points
    r = r_full[1:-1]                          # interior unknowns only
    T = 2 * np.pi / omega
    dt = T / steps_per_period
    N = n_r

    L = np.zeros((N, N))
    for j in range(N):
        rj = r[j]
        rp, rm = rj + dr / 2, rj - dr / 2
        if j - 1 >= 0:
            L[j, j - 1] += rm / (rj * dr * dr)
        # j-1 < 0 means the inner wall (u=0) -- Dirichlet BC, no term added
        L[j, j] += -(rp + rm) / (rj * dr * dr)
        if j + 1 < N:
            L[j, j + 1] += rp / (rj * dr * dr)
        # j+1 == N means the outer wall (u=0) -- Dirichlet BC, no term added

    I = np.eye(N)
    A_impl_inv = np.linalg.inv(I - 0.5 * dt * nu * L)
    A_expl = I + 0.5 * dt * nu * L

    u = np.zeros(N)
    t = 0.0
    n_steps = steps_per_period * n_periods
    history = []
    for step in range(n_steps):
        f_n = (G / rho) * np.cos(omega * t)
        f_np1 = (G / rho) * np.cos(omega * (t + dt))
        rhs = A_expl.dot(u) + 0.5 * dt * (f_n + f_np1)
        u = A_impl_inv.dot(rhs)
        t += dt
        if step >= n_steps - steps_per_period:
            history.append((t, u.copy()))
    return r, history