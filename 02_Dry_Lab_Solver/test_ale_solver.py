"""
test_ale_solver.py
Two independent validations of ale_solver.py:
  A) Exact reduction: a=0 must reproduce the already-validated rigid
     annular Womersley solution from Part 2.
  B) Physical scaling: the deviation from that rigid solution must grow
     approximately linearly with pulsation amplitude 'a', for small a --
     a real, falsifiable physics prediction, not just a code check.
"""

import numpy as np
from ale_solver import solve_ale
from annular_womersley_solver import annular_womersley_analytic

rho, mu = 993.0, 6.95e-4
nu = mu / rho
G = 100.0
R_i0, R_o, f = 22.4e-6, 34.6e-6, 5.0
omega = 2 * np.pi * f

failures = []


def rel_err_vs_rigid(a_test):
    hist = solve_ale(R_i0, R_o, a_test, f, rho, nu, G, n_eta=80,
                      steps_per_period=200, n_periods=8)
    errs = []
    for (t, u_ale, eta) in hist[::40]:
        r_phys = R_i0 * (1 - eta) + R_o * eta
        u_an = annular_womersley_analytic(r_phys, t, R_i0, R_o, rho, nu, omega, G)
        e = np.sqrt(np.mean((u_ale - u_an) ** 2)) / (np.sqrt(np.mean(u_an ** 2)) + 1e-30)
        errs.append(e)
    return np.mean(errs)


# --- Check A: exact a=0 reduction ---
err_a0 = rel_err_vs_rigid(0.0)
print(f"[Check A] a=0 exact reduction: mean rel error vs rigid = {err_a0:.4%}")
if err_a0 > 0.02:
    failures.append(f"a=0 case does not reduce to rigid solution (error {err_a0:.4%})")

# --- Check B: error should grow roughly linearly with amplitude ---
amplitudes = [0.0005, 0.001, 0.002, 0.004, 0.01, 0.02]
errs_by_a = [rel_err_vs_rigid(a) for a in amplitudes]
for a_val, e_val in zip(amplitudes, errs_by_a):
    print(f"[Check B] a={a_val:.4f}  mean rel error vs rigid = {e_val:.4%}")

# Fit log(error) vs log(a) over the small-amplitude range; slope should be
# close to 1 (linear scaling) for genuinely small-amplitude perturbation physics.
log_a = np.log(amplitudes)
log_e = np.log(errs_by_a)
slope, intercept = np.polyfit(log_a, log_e, 1)
print(f"[Check B] fitted power-law exponent = {slope:.3f} (expect close to 1.0)")
if not (0.7 <= slope <= 1.3):
    failures.append(f"Amplitude-scaling exponent {slope:.3f} is not close to the "
                     f"expected linear (1.0) scaling -- possible sign or scaling bug")

if failures:
    print(f"\nFAILED: {len(failures)} check(s):")
    for f_msg in failures:
        print("  -", f_msg)
    raise SystemExit(1)
else:
    print("\nAll ALE solver validation checks passed.")