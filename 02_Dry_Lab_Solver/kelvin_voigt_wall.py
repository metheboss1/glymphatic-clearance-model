"""
kelvin_voigt_wall.py
Phase 5: The Kelvin-Voigt viscoelastic wall model from Day 1's framing,
made real. Instead of an ASSUMED sinusoidal R_i(t), the wall's motion is
now the OUTPUT of a genuine mechanical model responding to a driving
blood-pressure pulse.

Physical picture: a thin-walled vessel obeys Laplace's law (hoop stress
= transmural pressure * radius / wall thickness). The Kelvin-Voigt
constitutive law says stress = E*strain + eta*(d(strain)/dt) -- an
elastic spring and a viscous dashpot sharing the load side-by-side.
Combining these for small deformations gives a first-order linear ODE
for the hoop strain epsilon(t) = (R_i(t) - R_i0)/R_i0:

    eta * d(epsilon)/dt + E * epsilon = P_forcing(t)

where P_forcing(t) = deltaP(t) * R_i0 / h folds the driving pressure
pulse and geometry into one term. No wall-mass/inertia term appears,
matching Day 1's original framing (vessel-wall inertia is negligible
compared to viscoelastic forces at physiological frequencies -- this is
standard in vascular biomechanics, consistent with the Womersley-number
argument already used for the fluid in Days 3-4).
"""

import numpy as np


def wall_analytic(t, P0, E, eta, omega):
    """
    Exact steady-periodic (long-time) solution to
        eta*d(eps)/dt + E*eps = P0*cos(omega*t)
    Returns eps(t), the steady-state amplitude eps_ss, the phase lag phi
    (in radians), and the Deborah number De = eta*omega/E.
    This is the classical "loss angle" result for a Kelvin-Voigt element:
    tan(phi) = De exactly.
    """
    De = eta * omega / E
    eps_ss = P0 / np.sqrt(E ** 2 + (eta * omega) ** 2)
    phi = np.arctan(De)
    return eps_ss * np.cos(omega * t - phi), eps_ss, phi, De


def wall_fd(P0, E, eta, omega, steps_per_period=400, n_periods=15):
    """
    Numerically integrates eta*d(eps)/dt + E*eps = P0*cos(omega*t) from
    rest, using implicit trapezoidal (Crank-Nicolson) time-stepping --
    unconditionally stable, matching the numerical philosophy of every
    prior day's solver. Returns (t, eps) snapshots from the final period.
    """
    T = 2 * np.pi / omega
    dt = T / steps_per_period
    eps = 0.0
    t = 0.0
    n_steps = steps_per_period * n_periods
    history = []
    for step in range(n_steps):
        P_n = P0 * np.cos(omega * t)
        P_np1 = P0 * np.cos(omega * (t + dt))
        rhs = (eta / dt - 0.5 * E) * eps + 0.5 * (P_n + P_np1)
        eps = rhs / (eta / dt + 0.5 * E)
        t += dt
        if step >= n_steps - steps_per_period:
            history.append((t, eps))
    return history


def calibrate_P0(eps0_target, E, eta, omega):
    """
    Given a desired steady-state pulsation amplitude eps0_target (e.g.
    the literature value a=0.045 resolved on Day 4), back out the
    forcing amplitude P0 that produces it at this (E, eta, omega).
    Used to keep the pulsation amplitude fixed at the literature-anchored
    baseline while De is swept by varying eta/E, isolating the effect of
    De itself rather than conflating it with an amplitude change.
    """
    return eps0_target * np.sqrt(E ** 2 + (eta * omega) ** 2)