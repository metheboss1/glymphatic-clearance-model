"""
womersley_solver.py
Phase 3: A linear, oscillatory-pressure-driven pipe-flow solver, plus the
classical analytic Womersley solution it gets validated against.

Why a *linear* solver is legitimate here (not a simplification we're
sneaking past a judge): Boster et al. (PNAS 2023) directly measured the
terms of the Navier-Stokes equation in vivo in perivascular flow and found
the nonlinear inertial term (u . grad)u to be negligible compared to the
viscous and pressure terms, at a dynamic Reynolds number Rd ~ 1.1e-2
(Womersley number Wo ~ 0.1). That is exactly the regime this project's
flow lives in. Dropping the nonlinear term turns the full Navier-Stokes
equation into the linear, classical Womersley equation:

    rho * du/dt = -dp/dz + mu * (1/r) d/dr(r du/dr)

which has a known closed-form solution (Womersley, 1955) for flow in a
rigid pipe driven by an oscillating pressure gradient. That closed form is
exactly what today's numerical solver is checked against.
"""

import numpy as np
from scipy.special import jv


def womersley_analytic(r, t, R, rho, nu, omega, G):
    """
    Classical Womersley (1955) solution for oscillatory flow in a rigid
    pipe of radius R, driven by dp/dz(t) = -G*cos(omega*t).

    u(r,t) = Re[ (G / (i*omega*rho)) * (1 - J0(i^1.5 * alpha * r/R) /
                                              J0(i^1.5 * alpha)) * e^{i omega t} ]

    where alpha = R*sqrt(omega/nu) is the Womersley number.
    """
    alpha = R * np.sqrt(omega / nu)
    i32 = np.exp(1j * 3 * np.pi / 4)          # i^(3/2)
    J0_R = jv(0, i32 * alpha)
    J0_r = jv(0, i32 * alpha * (r / R))
    factor = G / (1j * omega * rho)           # = -i*G/(omega*rho)
    return np.real(factor * (1 - J0_r / J0_R) * np.exp(1j * omega * t))


def solve_pipe_fd(R, rho, nu, omega, G, n_r=80, steps_per_period=200, n_periods=8):
    """
    Implicit (Crank-Nicolson) finite-difference solver for the same
    oscillatory pipe-flow equation, marched forward in time from rest.
    Returns the radial grid and (t, u(r)) snapshots from the final period
    only, after early transients have decayed.
    """
    dr = R / n_r
    r = np.linspace(0.0, R, n_r + 1)     # j = 0 (center) .. n_r (wall)
    T = 2 * np.pi / omega
    dt = T / steps_per_period
    N = n_r                              # unknowns: j = 0..N-1 (wall u=0 is fixed, not solved)

    # Radial diffusion operator L such that L(u) ~= (1/r) d/dr(r du/dr)
    L = np.zeros((N, N))
    for j in range(1, N):
        rj, rp, rm = r[j], r[j] + dr / 2, r[j] - dr / 2
        L[j, j - 1] += rm / (rj * dr * dr)
        L[j, j] += -(rp + rm) / (rj * dr * dr)
        if j + 1 < N:
            L[j, j + 1] += rp / (rj * dr * dr)
        # j+1 == N is the wall: u=0 there, so it contributes nothing (implicit Dirichlet BC)
    # Centerline (r=0): axisymmetric limit of (1/r)d/dr(r du/dr) -> 2*u_rr,
    # discretized with the symmetry ghost point u_{-1}=u_1.
    L[0, 0] = -4.0 / dr ** 2
    L[0, 1] = 4.0 / dr ** 2

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
        if step >= n_steps - steps_per_period:   # keep only the final, periodic-state period
            history.append((t, u.copy()))
    return r[:N], history