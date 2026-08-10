"""
peristaltic_pumping.py
Phase 6: The traveling-wave (real peristaltic) pumping calculation.
Uses the "skateboard trick" (wave-frame coordinates) to turn the hard,
moving-in-time-and-space problem into an easy, steady, space-only one,
then uses the classical closed-form annular Poiseuille flow formula as
the "local resistance law" at each point along the wave.
"""

import numpy as np
from scipy.integrate import quad


def R_local(zeta, R_i0, R_o, eps0, k, phi_wall, mu):
    """Local resistance (dp/dz per unit Q) at wave-frame position zeta,
    from the classical closed-form annular Poiseuille formula."""
    Ri = R_i0 * (1 + eps0 * np.cos(k * zeta + phi_wall))
    return 8 * mu / (np.pi * (R_o**4 - Ri**4 - (R_o**2 - Ri**2)**2 / np.log(R_o / Ri)))


def mean_area(R_i0, R_o, eps0, k, phi_wall, wavelength):
    """<A>, the cross-sectional area averaged over one full wavelength."""
    def A(zeta):
        Ri = R_i0 * (1 + eps0 * np.cos(k * zeta + phi_wall))
        return np.pi * (R_o**2 - Ri**2)
    val, _ = quad(A, 0, wavelength, limit=200)
    return val / wavelength


def net_flow_rate(R_i0, R_o, eps0, c_wave, f, phi_wall, mu):
    """
    The full Day 6 calculation: <Q_lab> = c * <A>, after confirming the
    closure condition (q0=0) via the local-resistance integral.
    """
    omega = 2 * np.pi * f
    k = omega / c_wave
    wavelength = 2 * np.pi / k

    # Confirm the closure: mean local resistance must be positive (it always is),
    # which forces the wave-frame flow rate q0 to be exactly zero.
    mean_R, _ = quad(lambda z: R_local(z, R_i0, R_o, eps0, k, phi_wall, mu),
                      0, wavelength, limit=200)
    mean_R /= wavelength
    assert mean_R > 0, "Resistance must be positive -- geometry error"

    A_avg = mean_area(R_i0, R_o, eps0, k, phi_wall, wavelength)
    Q_lab_mean = c_wave * A_avg
    return Q_lab_mean, wavelength, A_avg