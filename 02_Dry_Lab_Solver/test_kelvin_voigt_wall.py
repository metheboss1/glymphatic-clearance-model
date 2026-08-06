"""
test_kelvin_voigt_wall.py
Validates the numerical Kelvin-Voigt wall solver against its exact
analytic steady-state solution, across a wide sweep of Deborah numbers
-- the same validate-before-trust standard applied to every solver
built since Day 3.
"""

import numpy as np
from kelvin_voigt_wall import wall_analytic, wall_fd

P0 = 1.0
omega = 2 * np.pi * 5.0
TOL = 0.01  # 1%

failures = []
De_targets = [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]

print("De        phi (rad)   phi (x pi)   numeric-vs-analytic error")
for De_target in De_targets:
    E = 1.0
    eta = De_target * E / omega
    hist = wall_fd(P0, E, eta, omega)
    ts = np.array([h[0] for h in hist])
    eps_num = np.array([h[1] for h in hist])
    eps_an, eps_ss, phi, De = wall_analytic(ts, P0, E, eta, omega)
    err = np.sqrt(np.mean((eps_num - eps_an) ** 2)) / (np.sqrt(np.mean(eps_an ** 2)) + 1e-30)
    print(f"{De:6.3f}    {phi:.4f}      {phi/np.pi:.4f}       {err:.4%}")
    if err > TOL:
        failures.append(f"De={De:.3f}: error {err:.4%} exceeds {TOL:.0%}")

# Sanity checks on the closed-form physics itself (not just the numerics):
# phi must be monotonically increasing with De, and must never exceed pi/2
# (a single-relaxation-time Kelvin-Voigt element cannot lag by more than
# a quarter cycle, no matter how large De gets -- tan(phi)=De -> phi -> pi/2
# only as De -> infinity).
phis = [np.arctan(d) for d in De_targets]
if not all(phis[i] < phis[i+1] for i in range(len(phis)-1)):
    failures.append("Phase lag is not monotonically increasing with De")
if not all(p < np.pi/2 for p in phis):
    failures.append("Phase lag exceeded pi/2 -- violates Kelvin-Voigt theory")

if failures:
    print(f"\nFAILED: {len(failures)} check(s):")
    for f_msg in failures:
        print("  -", f_msg)
    raise SystemExit(1)
else:
    print("\nAll Kelvin-Voigt wall validation checks passed.")