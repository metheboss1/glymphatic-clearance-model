"""
visualize_mesh.py
Plots the annular PVS grid at two instants: resting (t=0) and near
maximum inner-wall expansion, side by side, so the moving-boundary
behavior is visible at a glance.
"""

import numpy as np
import matplotlib.pyplot as plt
from mesh import generate_mesh

f = 1.2  # Heartbeat frequency (Hz)
R_i0, R_o, L = 8e-6, 15e-6, 200e-6
a = 0.03

t_rest = 0.0
t_peak = 0.25 / f  # quarter period after t=0, at sin(omega*t)=1: max expansion

fig, axes = plt.subplots(1, 2, figsize=(10, 5), sharey=True)

# Unpacking ax alongside t_val and title
for ax, t_val, title in zip(axes, [0.0, t_peak], ["Resting (t=0)", "Near maximum expansion"]):
    mesh = generate_mesh(R_i0, R_o, L, n_r=12, n_z=30, a=a, f=f, t=t_val)
    r_um = mesh['r_grid'] * 1e6
    z_um = mesh['z_grid'] * 1e6

    # Draw constant-eta lines (should curve/shift with the wall)
    for i in range(r_um.shape[0]):
        ax.plot(z_um[i, :], r_um[i, :], color='steelblue', linewidth=0.6)
    
    # Draw constant-xi lines (should stay straight and vertical)
    for j in range(r_um.shape[1]):
        ax.plot(z_um[:, j], r_um[:, j], color='steelblue', linewidth=0.6)

    # Draw the boundary walls
    ax.plot(z_um[0, :], r_um[0, :], color='crimson', linewidth=2, label='Inner wall (moving)')
    ax.plot(z_um[-1, :], r_um[-1, :], color='black', linewidth=2, label='Outer wall (rigid)')
    ax.set_title(f"{title}\nR_i = {mesh['R_i']*1e6:.3f} um")
    ax.set_xlabel("z (um)")
    ax.legend(loc='upper right', fontsize=8)

axes[0].set_ylabel("r (um)")
plt.tight_layout()
plt.savefig("02_Dry_Lab_Solver/mesh_check.png", dpi=150)
print("Saved 02_Dry_Lab_Solver/mesh_check.png")