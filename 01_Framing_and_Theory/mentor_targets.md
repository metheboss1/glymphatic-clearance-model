# Mentor Outreach Targets & Fully Drafted Email

## Target Mentors (Research Triangle Area)

| Name | Department | One sentence on their most relevant recent work | Specific paper or finding you'll reference in their email |
| :--- | :--- | :--- | :--- |
| **Dr. Richard Superfine** | Applied Physical Sciences (UNC Chapel Hill) | Characterizes dynamic viscoelastic properties and fluid-structure energy dissipation in biological hydrogels under oscillatory motion. | *Vasquez et al. (2016) / Hill et al. (2014)* — Frequency-dependent loss tangent ($\tan \delta$) transition in biological viscoelastic gels under $1–2 \text{ Hz}$ oscillatory shear. |
| **Dr. Mette Olufsen** | Mathematics (NC State University) | Models pulsatile biofluid dynamics and viscoelastic fluid-structure interactions in dynamic arterial and microvascular channels. | *Colebank & Olufsen (2021)* — Parameter sensitivity of wall compliance and pressure-flow phase lag in pulsatile fluid networks. |
| **Dr. William Polacheck** | Cell Biology & Physiology / Joint BME (UNC Chapel Hill) | Investigates microvascular fluid mechanics and cellular microenvironment hemodynamics using microfluidic channels. | *Polacheck et al.* — Fluid shear stress and boundary traction mechanics in microfluidic channel geometries. |
| **Dr. Caterina Gallippi** | Joint Department of Biomedical Engineering (UNC / NC State) | Innovates Viscoelastic Response (VisR) ultrasound imaging to measure dynamic tissue stiffness and loss modulus *in vivo*. | *Gallippi et al. (2025)* — *In vivo* measurement of loss modulus ($G''$) in vascular tissue under pulsatile displacement. |
| **Dr. Hossein (Amir) Salahshoor** | Mechanical Engineering & Materials Science (Duke) | Applies computational mechanics to model brain tissue viscoelasticity under dynamic intracranial pressure loading. | *Salahshoor et al.* — Viscoelastic dissipation and boundary-layer stability in dynamic intracranial continuum models. |

---

## Tier-1 Outreach Email Draft (Dr. Richard Superfine)

**Subject:** High school researcher, computational PVS clearance model — question on loss tangent behavior in oscillatory shear

Dear Professor Superfine,

My name is Sanjay, a high school student in the Research Triangle area. I am building an independent computational model of cerebrospinal fluid (CSF) clearance through the perivascular space (PVS), using a Kelvin-Voigt viscoelastic vessel-wall model and a custom Arbitrary Lagrangian-Eulerian (ALE) solver, aimed at the Regeneron Science Talent Search and ISEF.

I have been closely studying your lab's work on the rheology of biological hydrogels, particularly the frequency-dependent loss tangent ($\tan \delta = G''/G'$) transitions under oscillatory shear reported in your 2014 biophysical clearance papers (*Hill et al.*). My model's central hypothesis is that a critical Deborah number exists at which wall-fluid phase lag jumps discontinuously, producing an abrupt drop in net CSF clearance efficiency. 

Given your lab's measurement of viscoelastic storage versus loss moduli at physiological frequencies ($1.2 \text{ Hz}$), I have a specific question: when modeling the fluid-solid boundary layer, does treating the wall loss modulus $G''$ as constant across a heartbeat cycle introduce artificial numerical damping into the phase lag calculation, or must $G''(\omega)$ be explicitly coupled to the instantaneous strain rate of the moving inner wall?

I am not asking for lab access at this stage — I am hoping to ask a handful of focused technical questions as I validate my solver against established benchmarks like Womersley flow. If you are open to a short email exchange or a 15-minute call sometime in the coming weeks, I would be deeply grateful. I am happy to share my pre-registered hypotheses and preliminary solver results.

Thank you for your time and for your foundational contributions to biological fluid mechanics.

Sincerely,  
Sanjay  
[GitHub Repository Link]
