"""
test_uniform_pulsation_pumping.py
The key experiment of Day 5: couple the validated Kelvin-Voigt wall
model (kelvin_voigt_wall.py) to the validated ALE flow solver
(ale_solver_general.py), with NO externally-imposed pressure gradient
(G=0) -- so that the moving wall is the ONLY possible driver of flow,
exactly as Day 1 describes ("peristaltic pump").

This test both PROVES mathematically and CONFIRMS numerically that a
wall which pulses uniformly along the entire vessel length (no z
dependence -- the simplification made, and explicitly flagged, on
Day 2) produces exactly zero net axial flow, no matter what Deborah
number the viscoelastic wall model uses. See Day 5's Part 4 for the
full explanation of why, and its consequence for the project plan.
"""

import numpy as np
from kelvin_voigt_wall import wall_analytic
from ale_solver_general import solve_ale_general, compute_flow_rate

rho, mu = 993.0, 6.95e-4
nu = mu / rho
R_i0, R_o, f = 22.4e-6, 34.6e-6, 5.0
omega = 2 * np.pi * f
eps0 = 0.045   # literature-anchored baseline amplitude (Day 4, Part 5)

failures = []

print("Mathematical argument (see Part 4): with G=0, the governing equation")
print("du/dt|_eta = (u_g/W) du/deta + (nu/(r*W^2)) d/deta(r du/deta)")
print("is LINEAR and HOMOGENEOUS in u -- every term is proportional to u or")
print("its derivatives. Starting from u=0, u(t)=0 for all t is the unique")
print("solution, regardless of how u_g(t) behaves. Numerical confirmation:\n")

for De_test in [0.01, 0.5, 5.0]:
    phi_wall = np.arctan(De_test)

    def Ri_func(t, phi_wall=phi_wall):
        return R_i0 * (1 + eps0 * np.cos(omega * t - phi_wall))

    def dRidt_func(t, phi_wall=phi_wall):
        return -R_i0 * eps0 * omega * np.sin(omega * t - phi_wall)

    hist = solve_ale_general(Ri_func, dRidt_func, R_o, rho, nu, G=0.0, omega_heart=omega,
                              n_eta=60, steps_per_period=150, n_periods=6)
    Qs = np.array([compute_flow_rate(h[1], h[2], Ri_func(h[0]), R_o) for h in hist])
    max_abs_Q = np.max(np.abs(Qs))
    print(f"De={De_test:5.2f}  phi_wall={phi_wall:.4f} rad   max|Q(t)| over final period = {max_abs_Q:.3e} m^3/s")
    if max_abs_Q > 1e-20:   # allow for pure floating-point roundoff only
        failures.append(f"De={De_test}: uniform pulsation produced nonzero flow "
                         f"(max|Q|={max_abs_Q:.3e}) -- contradicts the linear-homogeneous proof")

print("\nConclusion: uniform (z-independent) wall pulsation cannot pump fluid axially,")
print("regardless of the wall's viscoelastic Deborah number. This is a structural")
print("consequence of the z-independence simplification made on Day 2, not a bug.")
print("Hypothesis 1 (Phase Lag Phi between wall motion and fluid flow) cannot be")
print("meaningfully tested until the model includes an axial traveling-wave component.")

if failures:
    print(f"\nUNEXPECTED: {len(failures)} check(s) contradicted the proof:")
    for f_msg in failures:
        print("  -", f_msg)
    raise SystemExit(1)
else:
    print("\nAll checks consistent with the zero-net-flow proof.")