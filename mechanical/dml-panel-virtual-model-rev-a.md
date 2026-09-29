# AudioPicture V2.2 Rev.A — DML panel virtual model contract

Status: **PARAMETRIC_MODEL_BASELINE / MATERIAL_AND_EXCITER_VARIANT_OPTIMIZATION_REQUIRED**

## 1. Purpose
This document defines the virtual modal/electro-mechanical model that has authority over final DML panel material, thickness, exciter coordinates and the load model used to release the TAS5825M output filter.

It does not freeze a panel construction before FEA/acoustic optimization.

## 2. Fixed geometry envelope
- product envelope: 320 x 400 x 40 mm maximum;
- DML active-panel baseline: 300 x 380 mm;
- four exciters;
- two exciters in series per amplifier channel;
- printed acoustic fabric remains outside the structural DML model initially and is added as distributed mass/damping in the refined model.

Coordinate origin: lower-left corner of the 300 x 380 mm active panel.

Initial coordinates only:
- EX1 = (75,105) mm
- EX2 = (225,105) mm
- EX3 = (75,275) mm
- EX4 = (225,275) mm

Coordinates are optimization variables, not production dimensions.

## 3. Exciter authority and lifecycle gate
Original baseline: Dayton Audio DAEX25FHE-4.
Manufacturer data baseline:
- nominal impedance 4 ohm;
- Re 4.3 ohm;
- Le 0.10 mH at 1 kHz;
- free-air Fs approximately 224 Hz;
- 25 mm voice coil;
- 24 W RMS;
- approximately 50.5 mm diameter and 20.5 mm height.

Dayton/Parts Express engineering-change documentation identifies EX25FHE2-4 as the successor/revision. It retains 4 ohm, Re 4.3 ohm, Le 0.10 mH and 24 W but changes the free-air resonance to approximately 115 Hz and changes mechanical construction/dimensions.

Therefore the virtual model shall contain two exciter parameter sets:
A. legacy DAEX25FHE-4;
B. current EX25FHE2-4 revision.

Do not silently substitute one mechanical model for the other. Procurement status and final mechanical drawing shall decide the production exciter only after the virtual comparison.

## 4. Panel model
Start with a laminated/sandwich plate model rather than a homogeneous isotropic plate.

Parameter sweep shall include:
- face-sheet material and thickness;
- core material and thickness;
- adhesive-layer shear modulus and damping;
- panel areal mass;
- orthotropic bending stiffness where applicable;
- structural loss factor;
- edge-support stiffness/damping;
- exciter adhesive/contact stiffness;
- added exciter mass and inertia.

Candidate construction families may include lightweight foam-core or honeycomb sandwich panels, but no family is production-frozen by this document.

## 5. Boundary conditions
Do not use perfectly clamped edges as the sole model.

Run at least:
1. free-panel diagnostic modes;
2. compliant perimeter support representing elastomer/frame retention;
3. worst-case locally stiffened support caused by enclosure attachment.

The production support model shall be correlated to the actual CAD retention geometry.

## 6. Exciter representation
Stage 1 modal optimization:
- lumped exciter mass/inertia at the contact region;
- distributed normal force over the adhesive/contact annulus;
- electrical force proportional to BL * current where a validated BL is available.

Stage 2 coupled model:
- voice-coil Re + Le;
- mechanical suspension/resonance;
- contact compliance;
- panel mobility at each exciter;
- back-EMF/electromechanical coupling.

Manufacturer free-air parameters are initialization data, not a substitute for mounted-panel impedance.

## 7. Optimization variables
Exploration bounds for first virtual sweep:
- EX x coordinate: 45..255 mm;
- EX y coordinate: 55..325 mm;
- preserve minimum mechanical clearance from panel edge and from other controlled volumes;
- left/right geometry may begin symmetric but symmetry is not mandatory if modal optimization benefits from controlled asymmetry.

Radar RF aperture/keep-out, microphone isolation region and enclosure hardware are exclusion constraints.

## 8. Objective functions
Rank candidate configurations using:
- modal-density uniformity from approximately 100 Hz to 20 kHz;
- avoidance of strongly coincident exciter/modal nodes;
- spatially averaged surface velocity flatness;
- low peak-to-average modal response;
- left/right channel similarity;
- low reaction force transferred into VOICE/radar/enclosure;
- acceptable maximum panel strain;
- acceptable exciter contact stress;
- minimum DSP boost requirement.

Do not optimize only a single on-axis SPL point.

## 9. Acoustic refinement
For shortlisted structures, couple panel surface velocity to an acoustic radiation model.

Evaluate:
- 0.5 m and 1 m listening distances;
- on-axis and representative room angles;
- spatial average over a listening window;
- fabric added mass/damping;
- wall-mounted rear boundary condition.

The goal is a smooth correctable response, not a mathematically flat raw curve.

## 10. Electrical impedance output
The final model shall export complex impedance Z(f) for:
- each mounted exciter;
- each two-exciter series channel;
- tolerance/corner cases.

Minimum useful frequency grid: 20 Hz..20 kHz with additional resolution around mechanical resonances.

This Z(f) becomes the authoritative load for TAS5825M LC-filter SPICE/AC analysis. Until this exists, 10 uH / 0.68 uF remains only the TI capture/reference network.

## 11. Virtual release sequence
1. material-property collection;
2. baseline modal model;
3. mesh-convergence study;
4. exciter-position sweep;
5. support-stiffness sweep;
6. exciter revision A/B comparison;
7. acoustic radiation calculation;
8. electromechanical Z(f) generation;
9. TAS5825M LC co-simulation;
10. thermal/strain worst-case run;
11. freeze panel stack and coordinates.

## 12. Stop conditions
Do not freeze final exciter coordinates from geometric symmetry alone.
Do not infer sandwich material properties from generic labels such as foam or honeycomb.
Do not release the LC capacitor from nominal 8-ohm arithmetic.
Do not use the legacy DAEX25FHE-4 free-air resonance for EX25FHE2-4.


## 13. Rev.A sandwich-stack shortlist

Dayton's exciter guidance favors thin, lightweight panels with high compressive strength and moderate/high bending strength, explicitly listing honeycomb and structural-foam sandwich composites among the best material families. The Rev.A virtual study therefore starts with three deliberately different stacks rather than one assumed material.

### Stack A — composite skins / PMI structural foam core — PRIMARY FEA BASELINE
Initial parameter box:
- symmetric glass-fibre/epoxy or thin high-modulus composite skins: 0.20..0.50 mm each;
- PMI structural foam core: 3..8 mm;
- structural adhesive film/layer: 0.05..0.20 mm each interface;
- total structural thickness target: 4..9 mm.

Reason: non-metallic, low areal mass, useful intrinsic damping and high sandwich bending stiffness. This is the primary AudioPicture baseline because it also avoids placing a continuous conductive skin in conflict with the 60 GHz radar aperture. Carbon-fibre skins may be simulated acoustically but are NOT allowed through RADAR_RF_KEEP_OUT unless RF EM analysis explicitly proves an aperture/window implementation.

### Stack B — glass/epoxy skins / aramid or resin-paper honeycomb core — HIGH-STIFFNESS COMPOSITE CORNER
Initial parameter box:
- glass/epoxy skins: 0.20..0.45 mm each;
- aramid/Nomex-type or resin-impregnated-paper honeycomb: 3..8 mm;
- adhesive: 0.05..0.20 mm;
- total target: 4..9 mm.

Reason: very high stiffness-to-mass and directly aligned with established DML material guidance. Model the honeycomb as orthotropic; do not replace it with an isotropic solid having only matched density.

### Stack C — paper/fibre skins / structural foam core — HIGH-DAMPING / LOW-COST CORNER
Initial parameter box:
- resin-treated paper/fibre or thin glass-fibre skins: 0.25..0.60 mm each;
- structural foam core: 3..8 mm;
- adhesive: 0.05..0.20 mm;
- total target: 4..9 mm.

Reason: useful higher-loss comparison and manufacturing-cost corner. It is not assumed to win; humidity stability, creep, print/fabric bonding and exciter-interface durability are explicit penalties.

### Excluded as primary baseline
A monolithic metal sheet is not a primary DML candidate. Aluminum honeycomb with metallic face sheets may be retained as a simulation reference, but continuous conductive material through the radar forward cone is forbidden and metal skins generally provide less intrinsic damping than composite alternatives.

## 14. First optimization matrix
For each stack, sweep at minimum:
- core thickness: 3, 5, 8 mm;
- skin thickness: low / nominal / high values from the stack range;
- perimeter support: soft, nominal, stiff;
- structural loss factor: low/nominal/high material-data corners;
- exciter set: legacy DAEX25FHE-4 and successor EX25FHE2-4;
- exciter coordinates: baseline plus controlled asymmetric perturbations.

First-stage ranking weights:
- 30% spatial/modal response smoothness;
- 20% usable low-frequency mobility;
- 15% high-frequency modal density/extension;
- 15% panel + exciter mass;
- 10% reaction force into enclosure/VOICE region;
- 10% manufacturability and tolerance robustness.

These weights are engineering search weights, not production acceptance limits.

## 15. Radar interaction
Every candidate shall carry the shared CAD volume RADAR_RF_KEEP_OUT. No conductive face sheet, foil, carbon-rich layer, metallic honeycomb, fastener or exciter hardware may intersect the forward RF cone. If a conductive/high-loss stack otherwise wins acoustically, it must be re-evaluated with a dedicated non-conductive RF window before it can remain a production candidate.

## 16. Current preferred virtual baseline
Start detailed FEA with **Stack A: composite glass-fibre/epoxy skins + PMI structural foam core**, nominally around 5 mm core with thin symmetric skins. This is a simulation baseline, NOT a material purchase/freeze. Stack B and Stack C remain mandatory comparison cases.

Status: **THREE_STACK_FEA_SHORTLIST_FROZEN / EXACT_MATERIAL_GRADES_AND_PROPERTIES_OPEN**.
