"""
second_harmonic.py
Phase 8: Looks at the FULL, exact shape of the flow signal over one
heartbeat -- not just its average value (Days 6-7) -- and asks whether
squeezing at full, real amplitude (not just "small") hides any extra
structure the earlier, simplified view missed.

Because A(theta) = pi*(R_o^2 - R_i0^2*(1+eps0*cos(theta))^2) is an exact
QUADRATIC function of cos(theta), its exact Fourier decomposition has
only three terms -- a constant part, a once-per-cycle ("fundamental")
part, and a twice-per-cycle ("second harmonic") part -- and nothing
beyond that, for any amplitude eps0, not just small ones. This module
computes all three exactly, with no approximation.
"""

import numpy as np


def harmonic_decomposition(R_i0, R_o, eps0):
    """
    Exact Fourier coefficients of A(theta) = pi*(R_o^2 - R_i(theta)^2),
    where R_i(theta) = R_i0*(1+eps0*cos(theta)).
    Returns (DC, fundamental_coef, second_harmonic_coef) such that
    A(theta) = DC + fundamental_coef*cos(theta) + second_harmonic_coef*cos(2*theta)
    EXACTLY (verified: no higher harmonics exist, at any amplitude).
    """
    DC = np.pi * (R_o**2 - R_i0**2 - R_i0**2 * eps0**2 / 2)
    fundamental_coef = -2 * np.pi * R_i0**2 * eps0
    second_harmonic_coef = -np.pi * R_i0**2 * eps0**2 / 2
    return DC, fundamental_coef, second_harmonic_coef


def second_to_fundamental_ratio(eps0):
    """Exact amplitude ratio of second harmonic to fundamental: eps0/4."""
    return eps0 / 4.0