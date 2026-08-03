"""
visualize_womersley.py
Plots the numerical (finite-difference) and analytic Womersley velocity
profiles on top of each other at four phases across one cardiac-like
cycle, so the match is visible, not just numeric.
"""

import numpy as np
import matplotlib.pyplot as plt
from womersley_solver import womersley_analytic, solve_pipe_fd

rho, mu = 993.0, 6.95e-4
nu = mu / rho
R = 20e-6
f = 5.0
omega = 2 * np.pi * f
G = 100.0

r, hist = solve_pipe_fd(R, rho, nu, omega, G, n_r=80, steps_per_period=200, n_periods=8)

fig, ax = plt.subplots(figsize=(6, 5))
phases_to_plot = [0, 50, 100, 150]
colors = plt.cm.viridis(np.linspace(0, 0.85, len(phases_to_plot)))
for c, idx in zip(colors, phases_to_plot):
    t, u_fd = hist[idx]
    u_an = womersley_analytic(r, t, R, rho, nu, omega, G)
    phase_frac = (idx / 200)
    ax.plot(u_an * 1e6, r * 1e6, color=c, linewidth=2, label=f"analytic, t/T={phase_frac:.2f}")
    ax.plot(u_fd * 1e6, r * 1e6, 'o', color=c, markersize=3, markerfacecolor='none')

ax.set_xlabel("velocity u (µm/s)")
ax.set_ylabel("radius r (µm)")
ax.set_title(f"Womersley pipe flow: FD (circles) vs analytic (lines)\nWo={R*np.sqrt(omega/nu):.3f}")
ax.legend(fontsize=8)
ax.axhline(0, color='gray', linewidth=0.5)
plt.tight_layout()
plt.savefig("02_Dry_Lab_Solver/womersley_check.png", dpi=150)
print("Saved 02_Dry_Lab_Solver/womersley_check.png")