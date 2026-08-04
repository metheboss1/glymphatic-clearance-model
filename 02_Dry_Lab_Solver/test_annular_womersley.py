"""
test_annular_womersley.py
Validates the rigid-annulus finite-difference solver against the
two-wall analytic Womersley solution -- the check Day 3's single-pipe
test structurally could not perform.
"""

import numpy as np
from annular_womersley_solver import annular_womersley_analytic, solve_annulus_rigid_fd

rho, mu = 993.0, 6.95e-4
nu = mu / rho
G = 100.0
TOL = 0.02

failures = []

# --- Regime 1: literature-informed physiological geometry (see Part 6) ---
R_i1, R_o1, f1 = 22.4e-6, 34.6e-6, 5.0
omega1 = 2 * np.pi * f1
r1, hist1 = solve_annulus_rigid_fd(R_i1, R_o1, rho, nu, omega1, G, n_r=80,
                                    steps_per_period=200, n_periods=8)
errs1 = []
for (t, u_fd) in hist1[::20]:
    u_an = annular_womersley_analytic(r1, t, R_i1, R_o1, rho, nu, omega1, G)
    e = np.sqrt(np.mean((u_fd - u_an) ** 2)) / (np.sqrt(np.mean(u_an ** 2)) + 1e-30)
    errs1.append(e)
mean_err1 = np.mean(errs1)
print(f"[Physiological annulus] mean rel L2 error = {mean_err1:.4%}")
if mean_err1 > TOL:
    failures.append(f"Physiological annulus error {mean_err1:.4%} exceeds {TOL:.0%}")

# --- Regime 2: numerically demanding gap-based Wo ~ 2 ---
R_i2, R_o2 = 100e-6, 150e-6
gap = R_o2 - R_i2
omega2 = nu * (2.0 / gap) ** 2
r2, hist2 = solve_annulus_rigid_fd(R_i2, R_o2, rho, nu, omega2, G, n_r=80,
                                    steps_per_period=200, n_periods=8)
errs2 = []
for (t, u_fd) in hist2[::20]:
    u_an = annular_womersley_analytic(r2, t, R_i2, R_o2, rho, nu, omega2, G)
    e = np.sqrt(np.mean((u_fd - u_an) ** 2)) / (np.sqrt(np.mean(u_an ** 2)) + 1e-30)
    errs2.append(e)
mean_err2 = np.mean(errs2)
print(f"[Demanding annulus, Wo~2] mean rel L2 error = {mean_err2:.4%}")
if mean_err2 > TOL:
    failures.append(f"Demanding annulus error {mean_err2:.4%} exceeds {TOL:.0%}")

# --- Grid convergence ---
errs_conv = {}
for nr in [20, 40, 80, 160]:
    r_c, hist_c = solve_annulus_rigid_fd(R_i2, R_o2, rho, nu, omega2, G, n_r=nr,
                                          steps_per_period=200, n_periods=8)
    t_c, u_c = hist_c[100]
    u_an_c = annular_womersley_analytic(r_c, t_c, R_i2, R_o2, rho, nu, omega2, G)
    errs_conv[nr] = np.sqrt(np.mean((u_c - u_an_c) ** 2)) / (np.sqrt(np.mean(u_an_c ** 2)) + 1e-30)
    print(f"[Convergence] n_r={nr:4d}  err={errs_conv[nr]:.5%}")
if not (errs_conv[160] < errs_conv[20]):
    failures.append("Refining the grid did not reduce annular error")

if failures:
    print(f"\nFAILED: {len(failures)} check(s):")
    for f_msg in failures:
        print("  -", f_msg)
    raise SystemExit(1)
else:
    print("\nAll annular Womersley validation checks passed.")