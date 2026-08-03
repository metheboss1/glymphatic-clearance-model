"""
test_womersley.py
Validates womersley_solver.py's finite-difference pipe-flow solver against
the classical analytic Womersley solution -- the rigid-channel check
Section 5/Phase 3 of the master plan calls for, before any moving wall
gets added.

Two regimes are checked:
  1. A numerically DEMANDING Womersley number (Wo ~ 2), deliberately
     higher than physiological PVS flow. A solver that's correct at
     high Wo is certainly correct at low Wo -- but not the reverse,
     since low-Wo flow degenerates toward quasi-steady Poiseuille flow,
     which even a buggy time-integration scheme could match by accident.
  2. The actual PHYSIOLOGICAL Womersley number for pial PVS flow,
     Wo ~ 0.13, computed directly from Boster et al. (PNAS 2023)'s own
     Reynolds-number estimate (f ~ 5 Hz cardiac frequency, nu = 7e-7 m^2/s).
"""

import numpy as np
from womersley_solver import womersley_analytic, solve_pipe_fd

rho = 993.0        # kg/m^3, CSF ~ water at 37C (Boster et al. 2023)
mu = 6.95e-4        # Pa s   (Boster et al. 2023)
nu = mu / rho        # ~7e-7 m^2/s (matches Boster et al.'s stated value)
G = 100.0            # Pa/m, forcing amplitude -- arbitrary but fixed for the test

TOL = 0.02  # 2% relative L2 error ceiling (a numerically comfortable margin;
            # in practice this solver lands well under 0.1% at these resolutions)

failures = []

# --- Regime 1: numerically demanding Wo ~ 2 ---
R1 = 100e-6
Wo1_target = 2.0
omega1 = nu * (Wo1_target / R1) ** 2
Wo1 = R1 * np.sqrt(omega1 / nu)

r1, hist1 = solve_pipe_fd(R1, rho, nu, omega1, G, n_r=80, steps_per_period=200, n_periods=8)
errs1 = []
for (t, u_fd) in hist1[::20]:
    u_an = womersley_analytic(r1, t, R1, rho, nu, omega1, G)
    err = np.sqrt(np.mean((u_fd - u_an) ** 2)) / (np.sqrt(np.mean(u_an ** 2)) + 1e-30)
    errs1.append(err)
mean_err1 = np.mean(errs1)
print(f"[Regime 1] Wo={Wo1:.3f} (numerically demanding)  mean rel L2 error = {mean_err1:.4%}")
if mean_err1 > TOL:
    failures.append(f"Regime 1 (Wo~2) mean error {mean_err1:.4%} exceeds {TOL:.0%} tolerance")

# --- Regime 2: physiological Wo, from Boster et al. 2023's own Re estimate ---
R2 = 20e-6
f2 = 5.0                      # Hz, approximate murine cardiac frequency (Boster et al. 2023)
omega2 = 2 * np.pi * f2
Wo2 = R2 * np.sqrt(omega2 / nu)

r2, hist2 = solve_pipe_fd(R2, rho, nu, omega2, G, n_r=80, steps_per_period=200, n_periods=8)
errs2 = []
for (t, u_fd) in hist2[::20]:
    u_an = womersley_analytic(r2, t, R2, rho, nu, omega2, G)
    err = np.sqrt(np.mean((u_fd - u_an) ** 2)) / (np.sqrt(np.mean(u_an ** 2)) + 1e-30)
    errs2.append(err)
mean_err2 = np.mean(errs2)
print(f"[Regime 2] Wo={Wo2:.3f} (physiological, literature-grounded)  mean rel L2 error = {mean_err2:.4%}")
if mean_err2 > TOL:
    failures.append(f"Regime 2 (physiological Wo) mean error {mean_err2:.4%} exceeds {TOL:.0%} tolerance")

# --- Grid convergence sanity: error should shrink as the grid is refined ---
err_coarse, err_fine = None, None
for nr in [20, 160]:
    r_c, hist_c = solve_pipe_fd(R1, rho, nu, omega1, G, n_r=nr, steps_per_period=200, n_periods=8)
    t_c, u_fd_c = hist_c[100]
    u_an_c = womersley_analytic(r_c, t_c, R1, rho, nu, omega1, G)
    e = np.sqrt(np.mean((u_fd_c - u_an_c) ** 2)) / (np.sqrt(np.mean(u_an_c ** 2)) + 1e-30)
    if nr == 20:
        err_coarse = e
    else:
        err_fine = e
print(f"[Convergence] n_r=20 error={err_coarse:.4%}   n_r=160 error={err_fine:.4%}")
if not (err_fine < err_coarse):
    failures.append("Refining the grid did not reduce error -- solver may have a bug, "
                     "not just discretization noise")

if failures:
    print(f"\nFAILED: {len(failures)} check(s):")
    for f_msg in failures:
        print("  -", f_msg)
    raise SystemExit(1)
else:
    print("\nAll Womersley validation checks passed.")