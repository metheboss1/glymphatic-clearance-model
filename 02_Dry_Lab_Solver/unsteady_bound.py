"""
unsteady_bound.py
Phase 9: Rigorously bounds the size of the ONE piece of physics every
calculation since Day 6 has left out -- genuine fluid inertia/memory in
the local (wave-frame) flow response -- instead of guessing whether it
matters.

Derivation: transforming the already-validated unsteady axial momentum
equation (Days 3-4) into wave-frame coordinates (Day 6's zeta = z - c*t)
produces ONE new term, -rho*c*du/dzeta, alongside the viscous term every
prior day already included. Comparing their natural size gives a single
dimensionless number, Lambda, controlling how much the missing physics
could possibly matter:

    Lambda = rho * c * gap^2 / (mu * wavelength) = Wo^2 / (2*pi)

where Wo = gap*sqrt(omega/nu) is the EXACT SAME Womersley number
validated back on Day 3. Because the governing equation is linear, any
correction from the neglected term is bounded, to leading order, by this
same relative size, Lambda -- so Lambda can be compared directly against
the Day 1 pre-registered thresholds (>=0.15*pi phase jump, >=15%
clearance drop) without needing to solve the full corrected equation.
"""

import numpy as np


def womersley_number(gap, omega, nu):
    """The exact Day-3 Womersley number, based on the annular gap."""
    return gap * np.sqrt(omega / nu)


def lambda_bound(De, c0, omega, gap, nu, mu, rho):
    """
    Lambda(De): the relative size of the neglected inertial/unsteady
    term compared to the already-included viscous term, using the
    self-consistent De-dependent wave speed from Day 7.
    """
    from wave_propagation import wave_speed_and_decay
    _, c_prop, _, _ = wave_speed_and_decay(De, c0, omega)
    Wo = womersley_number(gap, omega, nu)
    return (Wo ** 2) * (c_prop / c0) / (2 * np.pi)