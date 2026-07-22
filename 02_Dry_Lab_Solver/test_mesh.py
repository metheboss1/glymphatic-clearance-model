"""
test_mesh.py
Automated correctness checks for mesh.py. Run this after any change to
mesh.py, before trusting a single number that comes out of it.
"""

import numpy as np
from mesh import generate_mesh, inner_radius, grid_speed

R_I0, R_O, L = 8e-6, 15e-6, 200e-6
A, F = 0.03, 1.2
TOL = 1e-12  # floating-point tolerance, not a physics tolerance

test_times = np.array([0.0, 0.13, 0.25, 0.41, 0.5, 0.83])  # arbitrary, includes a peak near t=0.5*(1/F)/2

failures = []

for t in test_times:
    mesh = generate_mesh(R_I0, R_O, L, n_r=20, n_z=50, a=A, f=F, t=t)
    R_i_expected = inner_radius(t, R_I0, A, F)

    # Check 1: inner wall row must equal R_i(t) at every axial point
    inner_row = mesh['r_grid'][0, :]
    if not np.allclose(inner_row, R_i_expected, atol=TOL):
        failures.append(f"t={t}: inner boundary mismatch, "
                         f"max error {np.max(np.abs(inner_row - R_i_expected)):.3e}")

    # Check 2: outer wall row must equal R_o at every axial point, always
    outer_row = mesh['r_grid'][-1, :]
    if not np.allclose(outer_row, R_O, atol=TOL):
        failures.append(f"t={t}: outer boundary mismatch, "
                         f"max error {np.max(np.abs(outer_row - R_O)):.3e}")

    # Check 3a: grid speed at eta=0 must equal dR_i/dt exactly
    omega = 2 * np.pi * F
    dRi_dt_expected = R_I0 * A * omega * np.cos(omega * t)
    u_g_inner = mesh['u_g_grid'][0, 0]
    if not np.isclose(u_g_inner, dRi_dt_expected, atol=TOL):
        failures.append(f"t={t}: inner grid speed mismatch, "
                         f"got {u_g_inner:.3e}, expected {dRi_dt_expected:.3e}")

    # Check 3b: grid speed at eta=1 must be exactly zero
    u_g_outer = mesh['u_g_grid'][-1, 0]
    if not np.isclose(u_g_outer, 0.0, atol=TOL):
        failures.append(f"t={t}: outer grid speed should be 0, got {u_g_outer:.3e}")

# Check 4: the channel must never collapse or invert -- R_i(t) should
# always stay comfortably below R_o across a full pulsation cycle
t_cycle = np.linspace(0, 1 / F, 200)
R_i_cycle = inner_radius(t_cycle, R_I0, A, F)
if np.any(R_i_cycle >= R_O):
    failures.append("R_i(t) meets or exceeds R_o at some point in the cycle -- "
                     "channel would collapse or invert, amplitude 'a' is too large "
                     "relative to (R_o - R_i0)")

if failures:
    print(f"FAILED: {len(failures)} check(s) did not pass:")
    for f_msg in failures:
        print("  -", f_msg)
    raise SystemExit(1)
else:
    print(f"All checks passed across {len(test_times)} test times "
          f"and a full pulsation cycle sweep.")