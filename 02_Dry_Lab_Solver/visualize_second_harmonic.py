"""
visualize_second_harmonic.py
Makes the hidden overtone visible: plots the real, exact flow next to
a pure single-beat guess (they nearly overlap, since the overtone is
small) -- then plots JUST the leftover difference, which reveals the
clean, twice-as-fast hidden wave underneath.
"""

import numpy as np
import matplotlib.pyplot as plt
from second_harmonic import harmonic_decomposition

R_i0, R_o, eps0 = 22.4e-6, 34.6e-6, 0.045
c_wave = 2.17  # representative self-consistent wave speed (Day 7, De=0.5)

theta = np.linspace(0, 2 * np.pi, 400)
A_exact = np.pi * (R_o**2 - (R_i0 * (1 + eps0 * np.cos(theta)))**2)
Q_exact = c_wave * A_exact

DC, fund, _ = harmonic_decomposition(R_i0, R_o, eps0)
Q_fund_only = c_wave * (DC + fund * np.cos(theta))
residual = Q_exact - Q_fund_only

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
axes[0].plot(theta / np.pi, Q_exact * 1e9, color='crimson', lw=2.2, label='Real flow (exact)')
axes[0].plot(theta / np.pi, Q_fund_only * 1e9, color='steelblue', lw=1.6, ls='--',
             label='Pure single-beat guess')
axes[0].set_title('The two look almost identical here...')
axes[0].set_xlabel('time (heartbeat cycles)')
axes[0].set_ylabel('flow rate (scaled)')
axes[0].legend(fontsize=8)

axes[1].plot(theta / np.pi, residual * 1e9, color='darkorange', lw=2.2)
axes[1].set_title('...but the leftover difference reveals\nthe hidden second beat (twice as fast)')
axes[1].set_xlabel('time (heartbeat cycles)')
axes[1].set_ylabel('leftover (real minus pure guess)')
axes[1].axhline(0, color='gray', linewidth=0.4)
plt.tight_layout()
plt.savefig('02_Dry_Lab_Solver/second_harmonic_check.png', dpi=150)
print('Saved 02_Dry_Lab_Solver/second_harmonic_check.png')