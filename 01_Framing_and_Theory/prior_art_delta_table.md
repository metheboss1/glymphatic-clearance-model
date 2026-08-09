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

