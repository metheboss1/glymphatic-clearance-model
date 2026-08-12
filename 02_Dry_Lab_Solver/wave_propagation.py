"""
wave_propagation.py
Phase 7: Makes the wave's own speed depend on the SAME wall material
properties as everything else in the model, instead of treating it as
an independently-guessed number (as Day 6 did).

Physical idea: a purely elastic tube has a well-known wave speed
(Moens-Korteweg): c0 = sqrt(E*h/(2*rho*R)). A Kelvin-Voigt (viscoelastic)
wall behaves, for an oscillation at frequency omega, like a spring with
a COMPLEX effective stiffness E* = E*(1 + i*De), where De = eta*omega/E
is the exact same Deborah number validated on Day 5. Swapping E for E*
in the Moens-Korteweg formula gives a complex wave speed, whose real
part sets how fast the wave actually travels and whose imaginary part
sets how quickly it fades out as it travels -- both now genuine,
computable functions of De.
"""

import numpy as np


def wave_speed_and_decay(De, c0, omega):
    """
    Given the Deborah number De, the purely-elastic baseline wave speed
    c0 (what the speed would be with no viscous/dashpot component at
    all), and the driving frequency omega, returns:
      phi_wall   -- the same Kelvin-Voigt phase lag from Day 5, tan(phi)=De
      c_prop     -- the REAL propagation (phase) speed of the wave
      k_i        -- the spatial decay rate (1/m) of the wave's amplitude
      L_decay    -- the decay length (m), i.e. 1/k_i
    Derivation: E* = E(1+i*De) = E*sqrt(1+De^2)*exp(i*phi_wall).
    c* = sqrt(E*h/(2 rho R)) = c0*(1+De^2)^(1/4)*exp(i*phi_wall/2).
    """
    phi_wall = np.arctan(De)
    c_prop = c0 * (1 + De**2)**0.25 / np.cos(phi_wall / 2)
    k_i = (omega / c0) * (1 + De**2)**(-0.25) * np.sin(phi_wall / 2)
    L_decay = np.inf if k_i == 0 else 1.0 / k_i
    return phi_wall, c_prop, k_i, L_decay


def net_pumping_rate(De, c0, omega, R_i0, R_o, eps0):
    """
    The Day-6 net-pumping formula, <Q> = c_prop * <A>, now using the
    self-consistent, De-dependent c_prop instead of a fixed guessed
    wave speed. <A> itself does not depend on De (Day 6 finding, still
    true here -- see Part 4).
    """
    _, c_prop, _, _ = wave_speed_and_decay(De, c0, omega)
    A_mean = np.pi * (R_o**2 - R_i0**2 * (1 + eps0**2 / 2))
    return c_prop * A_mean