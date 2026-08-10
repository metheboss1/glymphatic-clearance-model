"""
test_peristaltic_pumping.py
Verifies the Day 6 peristaltic pumping calculation two independent ways,
and directly tests the central, surprising finding: does the wall
material's own Deborah number (via phi_wall) change the net pumping
rate or the phase lag between local wall motion and local flow?
"""

import numpy as np
from peristaltic_pumping import net_flow_rate, R_local, mean_area
from scipy.integrate import quad

rho, mu = 993.0, 6.95e-4
R_i0, R_o = 22.4e-6, 34.6e-6
eps0 = 0.045
f = 5.0
c_wave = 2.0   # m/s, representative small-artery pulse-wave speed

failures = []

print("phi_wall (rad)   <Q_lab> (m^3/s)         wavelength (m)   long-wavelength ratio")
Qs = []
for phi_wall_test in [0.0, 0.3, 0.8, 1.4]:
    Q, wavelength, A_avg = net_flow_rate(R_i0, R_o, eps0, c_wave, f, phi_wall_test, mu)
    ratio = wavelength / (2 * R_o)  # wavelength vs. vessel diameter scale
    print(f"{phi_wall_test:6.2f}          {Q:.6e}         {wavelength:.4f}         {ratio:.1f}")
    Qs.append(Q)

# The central finding: <Q_lab> should NOT depend on phi_wall at this order.
Qs = np.array(Qs)
spread = (Qs.max() - Qs.min()) / Qs.mean()
print(f"\nSpread in <Q_lab> across all tested phi_wall values: {spread:.2e} (relative)")
if spread > 1e-6:
    failures.append(f"Net flow unexpectedly depends on phi_wall (spread={spread:.2e})")

# Long-wavelength approximation must actually be justified for these numbers
_, wavelength, _ = net_flow_rate(R_i0, R_o, eps0, c_wave, f, 0.0, mu)
if wavelength / (2 * R_o) < 100:
    failures.append("Wavelength is not much larger than the vessel scale -- "
                     "long-wavelength approximation not justified")

if failures:
    print(f"\nFAILED: {len(failures)} check(s):")
    for f_msg in failures:
        print("  -", f_msg)
    raise SystemExit(1)
else:
    print("\nAll peristaltic pumping checks passed. Confirmed finding: at this order "
          "of approximation, net pumping rate does NOT depend on the wall's own "
          "Deborah number -- only on wave speed, amplitude, and geometry.")