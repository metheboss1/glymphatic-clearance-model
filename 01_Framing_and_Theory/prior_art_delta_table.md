\# Prior Art Delta Table

Updated: 7/19/26



| Paper | What they did | What's different here |

|---|---|---|

| Bilston, Fletcher, Brodbelt, Stoodley (2003), "Arterial pulsation-driven CSF flow in the perivascular space: a computational model," \*Computer Methods in Biomechanics \& Biomedical Engineering\* | Early computational model of PVS flow driven by arterial pulsation | Does not model wall viscoelasticity (Kelvin-Voigt or otherwise) and does not predict a critical transition threshold |

| Boster, Cai, Ladrón-de-Guevara, Sun, Zheng, Du, Thomas, Nedergaard, Karniadakis, Kelley (2023), "AI velocimetry reveals in vivo flow rates, pressure gradients, and shear stresses in murine perivascular flows," \*PNAS\* | AI-based measurement of real, in-vivo perivascular flow | This is experimental measurement of existing flow, not a first-principles predictive model of a critical viscoelastic transition |

| Boster et al. (2023), "Sizes and shapes of perivascular spaces surrounding murine pial arteries," \*Fluids and Barriers of the CNS\* | Geometric characterization of PVS shape | Characterizes geometry, not wall dynamics or viscoelasticity |

| Kelley et al. (2024), "Restoration of cervical lymphatic vessel function in aging rescues CSF drainage," \*Nature Aging\* | Aging intervention study on downstream cervical lymphatic vessels | Downstream of the PVS itself; not a model of wall viscoelasticity within the perivascular annulus |

| DTI-ALPS clinical imaging studies (multiple, e.g. glioma and TBI cohorts) | Correlate a diffusion-imaging biomarker with clinical glymphatic dysfunction | Correlational clinical biomarker work, not a mechanistic computational model with a falsifiable critical-threshold prediction |



\## One-sentence novelty claim (draft — refine after reading the above in full)

This project is, as far as current review shows, the first to combine a full

Kelvin-Voigt viscoelastic wall model with an ALE-solved advection-diffusion clearance

metric to predict a specific, falsifiable critical Deborah number at which phase lag

and clearance both undergo a sudden, quantifiable transition.



\## Day 5 finding (August 4, 2026)



The z-independent (uniform-pulsation) wall model used in Days 2-4, while

necessary infrastructure, is mathematically proven (and numerically

confirmed at De = 0.01, 0.5, and 5.0) to produce exactly zero net axial

flow, regardless of the wall's Kelvin-Voigt Deborah number. This follows

directly from the ALE momentum equation with no external pressure

gradient being linear and homogeneous in u. Hypothesis 1 (Phase Lag Phi

between wall motion and fluid flow) cannot be meaningfully tested until

the model is extended to include an axial traveling-wave component,

R\_i(z,t) rather than R\_i(t). This does not invalidate Days 2-4's work --

the mesh, the validated flow solver, and the Kelvin-Voigt wall model are

all necessary components of the traveling-wave model and carry over

directly. Scoped as the primary objective of Day 6.



\## Day 6 finding (August 9, 2026)



Extended the wall model to a genuine traveling wave, R\_i(z,t), using the

classical wave-frame ("skateboard") transformation and the exact annular

Poiseuille resistance law as the local closure. Confirmed (two independent

ways, matching to >10 decimal digits) that net pumping rate = wave speed

x mean cross-sectional area, and that the phase lag between local wall

motion and local flow is exactly pi radians -- BOTH independent of the

wall's own Kelvin-Voigt Deborah number. This traces to the steady

(quasi-static) local closure used today, which does not capture the

finite-Wo, "flow can't quite keep up" effects Hypothesis 1 is actually

about. Next step: replace the steady local closure with the already-

validated unsteady Womersley/ALE local law from Days 3-4.



\## Day 7 finding (August 9, 2026, continued)



Derived the wave's propagation speed and decay length self-consistently

from the same Kelvin-Voigt Deborah number used throughout the project

(via a complex effective modulus E\* = E(1+i\*De) in the classical

Moens-Korteweg wave-speed formula). Confirmed this correctly reduces to

the purely-elastic baseline at De=0, and that wave decay is negligible

over vessel-scale distances for all De tested. Found that net pumping

rate NOW genuinely depends on De (roughly 10x change across the De range

tested) -- the missing ingredient identified at the end of Day 6.

However, a formal statistical changepoint test (smooth cubic fit vs.

best two-segment fit, compared via BIC) found NO evidence of a sudden

jump; the dependence is smooth across three orders of magnitude in De.

Combined with Day 5 and Day 6's findings, this is now three independent,

increasingly complete models all finding smooth (not discontinuous)

De-dependence, within the small-amplitude, long-wavelength regime

studied. This is treated as a genuine, honestly-earned partial

falsification of Hypothesis 1's specific "sudden jump" claim within this

regime, per the Day 1 pre-registration's own stated falsification

criteria -- not a failed day of work.



\## Day 8 finding (August 2026)



Derived, exactly (not approximated), the full harmonic content of the

peristaltic flow signal: A(theta) contains precisely three terms -- DC,

fundamental, and a second harmonic at 2\*omega -- with amplitude ratio

exactly eps0/4 and phase exactly 2\*phi\_wall, verified numerically across

amplitudes from eps0=0.01 to eps0=0.6 (the real project value is 0.045).

Proved algebraically that this second-harmonic content cannot hide a

sudden De-jump, since its phase is a direct multiple of the already-

smooth Day-5 Kelvin-Voigt phase lag. This DEFINITIVELY closes the

"instantaneous local response" family of models (Days 6, 7, 8 all

belong to this family) as a possible source of Hypothesis 1's predicted

jump. The one assumption shared by all three of those days, and never

yet tested, is that the local flow responds to the local pressure

gradient INSTANTLY, with no memory -- i.e. a steady/quasi-static local

law. Day 9 will replace that with the already-validated UNSTEADY

(Womersley) local law from Days 3-4, which is the one genuinely

different, untested mechanism remaining.

