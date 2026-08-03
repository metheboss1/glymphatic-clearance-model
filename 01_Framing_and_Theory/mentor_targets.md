# Mentor Outreach Targets

## Target Mentors (Research Triangle Area)

| Name | Verified current affiliation | Verified focus | Why relevant here |
| :--- | :--- | :--- | :--- |
| **Dr. Richard Superfine** | UNC-Chapel Hill, Applied Physical Sciences (Chair) | Biophysics, mechanobiology, force sensing in living systems, microfluidics | Broad biophysics/mechanics fit; strongest for general force-sensing and instrumentation questions |
| **Dr. William Polacheck** | UNC/NC State Joint Department of Biomedical Engineering | Microfluidic organ-on-chip models, biofluid mechanics and hemodynamics in the cellular microenvironment, interstitial fluid pressure gradients | Very close fit — his lab explicitly studies fluid-mechanical forces in tissue microenvironments |
| **Dr. Caterina Gallippi** | UNC/NC State Joint (Lampe) Department of Biomedical Engineering | Ultrasound elasticity imaging — noninvasive measurement of tissue stiffness and fluid thickness | Directly relevant to validating a viscoelastic wall model non-invasively |
| **Dr. Murthy Guddati** | NC State, Civil, Construction, and Environmental Engineering | Computational mechanics, wave propagation; currently collaborating with Mayo Clinic and Duke on ultrasound-based measurement of arterial wall stiffness | Unusually strong, specific fit — his current work is literally about measuring the same kind of wall viscoelasticity this project models, just via a different route |
| **Dr. Hossein (Amir) Salahshoor** | Duke University (Civil & Environmental Engineering, and Mechanical Engineering & Materials Science) | Data-driven viscoelasticity, brain tissue mechanics, computational modeling of soft biological materials under ultrasound | Arguably the single closest match of all five — his recent papers are literally about data-driven viscoelastic modeling of brain tissue |

---

## Tier-1 Outreach Email Draft (Dr. Richard Superfine)

> **Note:** Do not send yet. Review with a parent/advisor once the Boster/Kelley PNAS methods section reading is complete to finalize the specific technical question. *Update: Based on the verified table above, consider pivoting this first email to Dr. Salahshoor or Dr. Guddati once the open items are finalized.*

Subject: High school researcher, computational PVS clearance model — question on strain-dependent diffusivity in poroelastic media

Dear Professor Superfine,

My name is Sanjay, a high school student in the Research Triangle area. I'm
building an independent computational model of cerebrospinal fluid clearance
through the perivascular space, using a Kelvin-Voigt viscoelastic vessel-wall
model and a custom Arbitrary Lagrangian-Eulerian solver, aimed at the Regeneron
Science Talent Search and ISEF.

I've been closely reading your 2026 work on how strain impacts the diffusivity and localization of large solutes in poroelastic media, particularly
your analysis of how mechanical deformation governs the spatial localization and transport rates of large molecules in porous biological environments. My model's central hypothesis is that a critical
Deborah number exists at which wall-fluid phase lag jumps discontinuously,
producing an abrupt drop in clearance efficiency -- and I have a specific
question your work is unusually well positioned to answer: when mapping a moving fluid-structure boundary, does the dynamic strain rate fundamentally alter the localized diffusivity tensor near the poroelastic wall interface, or can it be treated as constant over a high-frequency pulsation cycle?

I'm not asking for lab access at this stage -- just hoping to ask a handful of
technical questions as I validate my solver against known results like
Womersley flow. If you're open to a short email exchange or a 15-minute call
sometime in the next few weeks, I'd be genuinely grateful. I'm happy to send
my pre-registered hypotheses and current results so far.

Thank you for your time and for the work in the Applied Physical Sciences department -- it's been
central to how I've framed this project.

Sincerely,
Sanjay
[GitHub repository link]