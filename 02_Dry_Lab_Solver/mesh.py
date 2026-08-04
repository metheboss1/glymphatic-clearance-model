"""
mesh.py
Phase 2: Coordinate mapping and mesh generation for the ALE perivascular
space (PVS) solver.

Physical space: an annular channel between the inner (vessel) wall at
r = R_i(t), which pulses with the heartbeat, and the outer (astrocytic
sleeve) wall at r = R_o, which is rigid and fixed.

Computational space: a fixed rectangle (xi, eta) where
    xi  = z                                      (axial coordinate, unchanged)
    eta = (r - R_i(t)) / (R_o - R_i(t))      (radial coordinate, in [0, 1])

eta = 0 always sits exactly on the moving inner wall.
eta = 1 always sits exactly on the fixed outer wall.
That is what lets this solver keep a perfectly rectangular grid even
though the physical channel is squeezing in and out every heartbeat.
"""

import numpy as np


def inner_radius(t, R_i0=22.4e-6, a=0.045, f=5.0):
    # R_i0, a resolved from literature (see Day 4, Part 5):
    #   R_i0 = 22.4 um, derived from Boster et al. (PNAS 2023) mouse-1
    #   subdomain area (1.1e3 um^2, half-annulus) combined with their
    #   cited PVS:vessel area ratio K=1.4 (Mestre et al. 2018).
    #   Cross-checked against Raicevic et al. (2023), whose independently
    #   measured area ratio (K~1.12-1.21) gives R_i0 in the range 22-25 um --
    #   the nominal value here sits within that literature-cited range.
    #   a = 0.045, from Boster et al.'s stated ~1 um wall displacement
    #   divided by the nominal R_i0.
    #   f = 5.0 Hz, approximate murine cardiac frequency (Boster et al. 2023).
    """
    Time-varying inner (vessel) wall radius under pulsatile forcing.

    Parameters
    ----------
    t    : float or ndarray -- time (s)
    R_i0 : float -- resting/mean inner radius (m)
    a    : float -- pulsation amplitude as a fraction of R_i0
    f    : float -- heartbeat frequency (Hz)

    Returns
    -------
    R_i(t), same shape as t
    """
    omega = 2 * np.pi * f
    return R_i0 * (1 + a * np.sin(omega * t))


def grid_speed(t, R_i0=22.4e-6, R_o=34.6e-6, a=0.045, f=5.0, eta=0.0):
    """
    Radial speed of a fixed-eta grid point through physical space, u_g.
    This is the term the ALE Navier-Stokes equations will need on Day 3+
    for the relative convective velocity (u - u_g).

    Derivation: since r(eta, t) = R_i(t) * (1 - eta) + R_o * eta,
        u_g = dr/dt at fixed eta = dR_i/dt * (1 - eta)
    which is exact and analytic -- no finite-difference approximation
    needed, and no dependence on R_o since the outer wall never moves.
    """
    omega = 2 * np.pi * f
    dRi_dt = R_i0 * a * omega * np.cos(omega * t)
    return dRi_dt * (1 - eta)


def generate_mesh(R_i0=22.4e-6, R_o=34.6e-6, L=200e-6, n_r=20, n_z=50, a=0.045, f=5.0, t=0.0):
    """
    Build the computational (xi, eta) grid and map it to physical (r, z)
    coordinates at a single instant in time t.

    Parameters
    ----------
    R_i0 : float -- resting inner radius (m)
    R_o  : float -- outer, rigid radius (m)
    L    : float -- axial length of the modeled vessel segment (m)
    n_r  : int   -- number of radial grid points (eta direction)
    n_z  : int   -- number of axial grid points (xi direction)
    a, f : pulsation amplitude and frequency, passed to inner_radius
    t    : float -- time at which to evaluate the mesh (s)

    Returns
    -------
    dict with 'eta', 'xi', 'R_i', 'R_o', 'r_grid', 'z_grid', 'u_g_grid'
    """
    eta = np.linspace(0.0, 1.0, n_r)
    xi = np.linspace(0.0, L, n_z)

    R_i = inner_radius(t, R_i0, a, f)

    # r(eta, t) = R_i(t) * (1 - eta) + R_o * eta -- a straight-line
    # interpolation between the two walls at this instant.
    r_1d = R_i * (1 - eta) + R_o * eta
    u_g_1d = grid_speed(t, R_i0, R_o, a, f, eta)

    r_grid, z_grid = np.meshgrid(r_1d, xi, indexing='ij')
    u_g_grid, _ = np.meshgrid(u_g_1d, xi, indexing='ij')

    return {
        'eta': eta,
        'xi': xi,
        'R_i': R_i,
        'R_o': R_o,
        'r_grid': r_grid,
        'z_grid': z_grid,
        'u_g_grid': u_g_grid,
    }


if __name__ == "__main__":
    # Quick manual sanity print -- not the real verification (see
    # test_mesh.py), just a fast human-readable check while developing.
    mesh = generate_mesh(R_i0=22.4e-6, R_o=34.6e-6, L=200e-6, t=0.0)
    print(f"R_i at t=0: {mesh['R_i']*1e6:.4f} um")
    print(f"Inner-wall row r-values (should all equal R_i):")
    print(mesh['r_grid'][0, :5] * 1e6, "... (um)")
    print(f"Outer-wall row r-values (should all equal R_o):")
    print(mesh['r_grid'][-1, :5] * 1e6, "... (um)")