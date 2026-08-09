"""
test_ale_solver_general.py
Regression test: proves generalizing ale_solver.py into
ale_solver_general.py (Part 2) did not change any previously-validated
behavior. Re-runs Day 4's exact two checks (a=0 reduction, and
linear-in-amplitude scaling), now going through the general interface.
"""

import numpy as np
from ale_solver_general import solve_ale_general
from annular_womersley_solver import annular_womersley_analytic

rho, mu = 993.0, 6.95e-4
nu = mu / rho
G = 100.0
R_i0, R_o, f = 22.4e-6, 34.6e-6, 5.0
omega = 2 * np.pi * f
TOL = 0.02

failures = []


def Ri_sin(t, a):
    return R_i0 * (1 + a * np.sin(omega * t))


def dRidt_sin(t, a):
    return R_i0 * a * omega * np.cos(omega * t)


def err_vs_rigid(a_val):
    hist = solve_ale_general(lambda t: Ri_sin(t, a_val), lambda t: dRidt_sin(t, a_val),
                              R_o, rho, nu, G, omega, n_eta=60, steps_per_period=150, n_periods=8)
    errs = []
    for (t, u_ale, eta) in hist[::30]:
        r_phys = R_i0 * (1 - eta) + R_o * eta
        u_an = annular_womersley_analytic(r_phys, t, R_i0, R_o, rho, nu, omega, G)
        e = np.sqrt(np.mean((u_ale - u_an) ** 2)) / (np.sqrt(np.mean(u_an ** 2)) + 1e-30)
        errs.append(e)
    return np.mean(errs)


err_a0 = err_vs_rigid(0.0)
print(f"[Regression: a=0] mean error vs rigid analytic = {err_a0:.4%}")
if err_a0 > TOL:
    failures.append(f"a=0 regression error {err_a0:.4%} exceeds {TOL:.0%}")

amps = [0.001, 0.002, 0.004, 0.01]
errs_amp = [err_vs_rigid(a) for a in amps]
for a_val, e_val in zip(amps, errs_amp):
    print(f"[Regression: amplitude scaling] a={a_val:.4f}  err={e_val:.4%}")
slope, _ = np.polyfit(np.log(amps), np.log(errs_amp), 1)
print(f"[Regression] fitted scaling exponent = {slope:.3f} (expect close to 1.0)")
if not (0.7 <= slope <= 1.3):
    failures.append(f"Regression scaling exponent {slope:.3f} not close to linear")

if failures:
    print(f"\nFAILED: {len(failures)} check(s):")
    for f_msg in failures:
        print("  -", f_msg)
    raise SystemExit(1)
else:
    print("\nAll regression checks passed -- generalization preserved Day 4's validated behavior.")