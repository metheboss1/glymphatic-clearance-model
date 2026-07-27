# Mentor Outreach Targets

## Target Mentors (Research Triangle Area)

| Name | Department | One sentence on their most relevant recent work | Specific paper or finding you'll reference in their email |
| :--- | :--- | :--- | :--- |
| **Dr. Richard Superfine** | Applied Physical Sciences (UNC Chapel Hill) | Characterizes dynamic viscoelastic properties and fluid-structure energy dissipation in biological hydrogels under oscillatory motion. | *Hill et al. (2014)* — Frequency-dependent loss tangent transition in biological viscoelastic gels under 1–2 Hz oscillatory shear. |
| **Dr. Murthy Guddati** | Civil, Construction, & Environmental Engineering (NC State) | Develops computational forward modeling and inverse methods to estimate the viscoelastic material properties of dynamic arterial walls. | *Elastic and viscoelastic forward modeling and inversion to estimate human carotid artery stiffness*. |
| **Dr. William Polacheck** | Cell Biology & Physiology / Joint BME (UNC Chapel Hill) | Investigates microvascular fluid mechanics and cellular microenvironment hemodynamics using microfluidic channels. | Fluid shear stress and boundary traction mechanics in microfluidic channel geometries. |
| **Dr. Caterina Gallippi** | Joint Department of Biomedical Engineering (UNC / NC State) | Innovates Viscoelastic Response (VisR) ultrasound imaging to measure dynamic tissue stiffness and loss modulus *in vivo*. | *In vivo* measurement of loss modulus in vascular tissue under pulsatile displacement. |
| **Dr. Hossein (Amir) Salahshoor** | Mechanical Engineering & Materials Science (Duke) | Applies computational mechanics to model brain tissue viscoelasticity under dynamic intracranial pressure loading. | Viscoelastic dissipation and boundary-layer stability in dynamic intracranial continuum models. |

---

## Tier-1 Outreach Email Draft (Dr. Richard Superfine)

> **Note:** Do not send yet. Review with a parent/advisor once the Boster/Kelley PNAS methods section reading is complete to finalize the specific technical question.

Subject: High school researcher, computational PVS clearance model — question on loss tangent transitions in biological hydrogels

Dear Professor Superfine,

My name is Sanjay, a high school student in the Research Triangle area. I'm
building an independent computational model of cerebrospinal fluid clearance
through the perivascular space, using a Kelvin-Voigt viscoelastic vessel-wall
model and a custom Arbitrary Lagrangian-Eulerian solver, aimed at the Regeneron
Science Talent Search and ISEF.

I've been closely reading your 2014 paper on the viscoelastic properties of biological fluids (Hill et al.), particularly
your measurement of the frequency-dependent loss tangent transitions under oscillatory shear at physiological frequencies. My model's central hypothesis is that a critical
Deborah number exists at which wall-fluid phase lag jumps discontinuously,
producing an abrupt drop in clearance efficiency -- and I have a specific
question your work is unusually well positioned to answer: when modeling the fluid-solid boundary layer, does treating the wall loss modulus G'' as constant across a heartbeat cycle introduce artificial numerical damping into the phase lag calculation, or must G''(ω) be explicitly coupled to the instantaneous strain rate of the moving inner wall?

I'm not asking for lab access at this stage -- just hoping to ask a handful of
technical questions as I validate my solver against known results like
Womersley flow. If you're open to a short email exchange or a 15-minute call
sometime in the next few weeks, I'd be genuinely grateful. I'm happy to send
my pre-registered hypotheses and current results so far.

Thank you for your time and for the work in the Superfine Lab -- it's been
central to how I've framed this project.

Sincerely,
Sanjay
[phone number -- optional]
[GitHub repository link]
