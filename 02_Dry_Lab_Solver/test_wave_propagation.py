"""
test_wave_propagation.py
Validates wave_propagation.py, then runs the real Day 7 experiment:
does the now-self-consistent (De-dependent) wave speed put a sudden
jump back into the net pumping rate -- and is any apparent jump
REAL, by a formal statistical test, not just eyeballing a plot?
"""

import numpy as np
from wave_propagation import wave_speed_and_decay, net_pumping_rate

c0 = 2.0          # m/s, baseline purely-elastic wave speed (Day 6's value)
f = 5.0
omega = 2 * np.pi * f
R_i0, R_o = 22.4e-6, 34.6e-6
eps0 = 0.045

failures = []

# --- Sanity checks on the physics itself ---
phi0, c0_check, ki0, _ = wave_speed_and_decay(0.0, c0, omega)
print(f"[Sanity] De=0: phi_wall={phi0}, c_prop={c0_check} (must equal c0={c0}), k_i={ki0} (must be 0)")
if abs(c0_check - c0) > 1e-10 or abs(ki0) > 1e-10:
    failures.append("De=0 does not exactly recover the purely-elastic baseline")

for De_test in [0.1, 1.0, 5.0]:
    _, _, _, L = wave_speed_and_decay(De_test, c0, omega)
    ratio = L / 1e-3
    print(f"[Sanity] De={De_test}: decay length / 1mm-vessel = {ratio:.2e}")
    if ratio < 100:
        failures.append(f"De={De_test}: decay length not safely long compared to vessel scale")

# --- The real experiment: sweep De, look for a jump, FORMALLY test for it ---
De_sweep = np.logspace(-2, 2, 40)
Q_sweep = np.array([net_pumping_rate(De, c0, omega, R_i0, R_o, eps0) for De in De_sweep])

x = np.log(De_sweep)
y = Q_sweep

def sse_smooth(x, y):
    p = np.polyfit(x, y, 3)
    return np.sum((y - np.polyval(p, x))**2)

def sse_two_segment(x, y, split):
    x1, y1, x2, y2 = x[:split], y[:split], x[split:], y[split:]
    if len(x1) < 4 or len(x2) < 4:
        return np.inf
    p1, p2 = np.polyfit(x1, y1, 1), np.polyfit(x2, y2, 1)
    return np.sum((y1 - np.polyval(p1, x1))**2) + np.sum((y2 - np.polyval(p2, x2))**2)

sse0 = sse_smooth(x, y)
best_sse, best_split = np.inf, None
for i in range(5, len(x) - 5):
    s = sse_two_segment(x, y, i)
    if s < best_sse:
        best_sse, best_split = s, i

n = len(x)
BIC_smooth = n * np.log(sse0 / n) + 4 * np.log(n)
BIC_jump = n * np.log(best_sse / n) + 4 * np.log(n)

print(f"\n[Changepoint test] BIC (smooth, no-jump model) = {BIC_smooth:.2f}")
print(f"[Changepoint test] BIC (best two-segment/jump model) = {BIC_jump:.2f}")
print(f"[Changepoint test] Best candidate jump location: De = {De_sweep[best_split]:.3f}")
jump_favored = BIC_jump < BIC_smooth
print(f"[Changepoint test] Two-segment (jump) model favored over smooth model? {jump_favored}")

print("\nDe          Q (m^3/s)")
for i in range(0, len(De_sweep), 4):
    print(f"{De_sweep[i]:9.4f}   {Q_sweep[i]:.6e}")

if jump_favored:
    print("\nA statistically favored jump was found -- would require further scrutiny "
          "before treating it as confirmation of Hypothesis 1.")
else:
    print("\nNo statistically favored jump. The self-consistent (De-dependent) wave speed "
          "DOES restore De-dependence to the net pumping rate -- but that dependence is "
          "SMOOTH, not a sudden jump, at least across three orders of magnitude in De.")

if failures:
    print(f"\nFAILED: {len(failures)} sanity check(s):")
    for f_msg in failures:
        print("  -", f_msg)
    raise SystemExit(1)
else:
    print("\nAll sanity checks passed.")