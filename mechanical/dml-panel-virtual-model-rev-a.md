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


## 17. Normalized modal-placement screening — 2026-09-29

A geometry-only first pass was run before assigning uncertain absolute sandwich material constants. The panel was represented by rectangular bending-mode shape functions and the first 35 modes were evaluated for aggregate coupling at the four exciter points.

This is NOT the production FEA and does not predict absolute resonance frequencies, SPL or impedance. Its purpose is to detect geometric placement pathologies before the material model is frozen.

### Result
The original symmetric 2 x 2 seed:
- (75,105)
- (225,105)
- (75,275)
- (225,275)

shows repeated weakly coupled modal families caused by symmetry/equal spacing. It is retained only as a comparison case and is no longer the preferred placement seed.

A randomized constrained search over the permitted panel region produced substantially more uniform low-order modal coupling when the four excitation points were intentionally non-uniform. One geometry-only high-scoring seed was approximately:
- P1 = (163,311) mm
- P2 = (110,283) mm
- P3 = (219,125) mm
- P4 = (50,176) mm

These coordinates are **NOT production coordinates**. They are a numerical seed demonstrating that controlled asymmetry is valuable. They must be re-optimized with:
- real sandwich orthotropic properties;
- compliant frame boundary;
- exciter mass/contact model;
- left/right channel grouping and stereo objective;
- RADAR_RF_KEEP_OUT;
- VOICE isolation volume;
- wiring/assembly clearance;
- acoustic radiation objective.

### Placement rule for detailed FEA
Do not force a regular 2 x 2 grid. Use constrained asymmetric optimization while preserving practical channel grouping. Include the Dayton unequal-edge-distance guidance as a seed/constraint family, but let the coupled FEA/acoustic objective select the final coordinates.

Status: **SYMMETRIC_GRID_DEMOTED / ASYMMETRIC_PLACEMENT_OPTIMIZATION_REQUIRED**.


## 18. Stereo-pairing pre-screen — 2026-09-29

The four-point asymmetric seed was evaluated under all three possible 2+2 electrical pairings using the same normalized rectangular modal basis used for the geometry pre-screen.

This remains a geometry-only diagnostic. It does not predict stereo image, SPL or production response.

Seed points:
- P1=(163,311)
- P2=(110,283)
- P3=(219,125)
- P4=(50,176) mm.

Pairing results, using equal in-phase drive within each series pair:
1. P1+P2 versus P3+P4: normalized modal-vector correlation about 0.003; pair-centroid separation about 146.5 mm.
2. P1+P3 versus P2+P4: correlation about 0.029; centroid separation about 111.6 mm.
3. P1+P4 versus P2+P3: correlation about 0.008; centroid separation about 70.2 mm.

The numerically lowest modal correlation is NOT automatically the stereo winner: pairing 1 separates the channel centroids mainly along the panel vertical axis. AudioPicture is intended to preserve a useful horizontal stereo image, so the detailed optimization shall include horizontal centroid separation and acoustic cross-correlation/directivity as explicit objectives.

### Detailed stereo optimization constraints
- exactly two 4-ohm exciters in series per channel;
- preserve polarity within each series branch;
- maximize useful horizontal L/R acoustic separation over the intended listening window;
- minimize excessive L/R transfer-function correlation where it collapses stereo width;
- keep channel-averaged sensitivity and spectral balance close enough for DSP correction without large boost;
- retain non-uniform edge distances and avoid regular-grid placement;
- enforce radar, VOICE, PCB, frame and harness exclusion volumes.

Dayton confirms that stereo can be produced by exciters on one panel and that image quality depends on exciter distance and symmetry; Dayton also advises against evenly spaced multiple exciters. Therefore the production solution shall balance stereo geometry against DML modal optimization rather than applying either rule alone.

Status: **STEREO_PAIRING_OBJECTIVE_DEFINED / NO_FINAL_LR_PAIR_OR_COORDINATES_FROZEN**.


## 19. Horizontal-stereo constrained placement — Candidate A

A second geometry-only optimization was run with explicit horizontal stereo constraints:
- LEFT exciters constrained to x=45..125 mm;
- RIGHT exciters constrained to x=175..255 mm;
- minimum exciter-to-exciter distance 55 mm;
- minimum within-channel vertical offset 70 mm;
- non-uniform placement retained;
- objectives combine modal-coupling uniformity, low normalized L/R modal correlation, horizontal centroid separation and channel aggregate-sensitivity balance.

One high-scoring seed is:

LEFT:
- L1 = (50,83) mm
- L2 = (96,169) mm

RIGHT:
- R1 = (204,243) mm
- R2 = (237,123) mm

Geometry-only diagnostics:
- horizontal L/R centroid separation ~=147 mm;
- normalized L/R modal-vector correlation ~=0.006;
- aggregate modal-vector norm imbalance ~=0.24%.

Interpretation:
This is the first AudioPicture placement seed that simultaneously preserves deliberate DML asymmetry and a true horizontal LEFT/RIGHT geometry. It is designated **Candidate A**, not a production coordinate set.

The candidate must now survive detailed sandwich FEA, compliant-edge modeling, real exciter mass/contact, acoustic radiation, radar/VOICE exclusion volumes, wiring clearance and tolerance analysis. Final optimization shall permit local movement around these points rather than locking them.

Manufacturer guidance remains consistent with this search strategy: multiple exciters should not be evenly spaced, unequal edge/inter-exciter distances are preferred, and stereo image on a single panel depends on L/R exciter separation and placement symmetry. In AudioPicture, acoustic optimization has authority over simple geometric symmetry.

Status: **DML_PLACEMENT_CANDIDATE_A_DEFINED / DETAILED_FEA_NOT_YET_FROZEN**.


## 20. Stack-A material baseline and first absolute-frequency sanity model — 2026-09-29

### Core baseline
Use **ROHACELL 51 IG-F, 5 mm** as the first detailed Stack-A core model.
Manufacturer typical properties:
- density: 52 kg/m^3 (published tolerance depends on product/thickness);
- tensile modulus: 70 MPa;
- shear modulus: 19 MPa;
- compressive modulus: 43 MPa;
- shear strength: 0.8 MPa;
- compressive strength: 0.9 MPa.

The 5 mm thickness is within Evonik's standard IG-F sales range. These are model initialization properties, not incoming-inspection limits.

### Legacy exciter concentrated model
For DAEX25FHE-4 initialize:
- total exciter net mass: 110.9 g;
- Mms: 1.61 g;
- BL: 3.63 Tm;
- Re: 4.3 ohm;
- Le: 0.10 mH;
- uncoupled Fs: 224 Hz.

The total 110.9 g mass is included in structural inertia through the real attachment footprint; Mms is reserved for the coupled moving-system model and must not be double-counted as an additional rigid mass.

### Skin-property gate
No exact glass/epoxy laminate grade is frozen yet. Therefore absolute modal frequencies cannot yet be treated as predictions.

For scale checking only, a provisional symmetric sandwich calculation using 5 mm PMI core, 0.30 mm skins, and an assumed quasi-isotropic glass/epoxy skin modulus of 20 GPa gives:
- sandwich areal mass before exciters/adhesive/fabric ~=1.37 kg/m^2;
- first simply-supported equivalent plate mode ~=230 Hz before discrete exciter mass, compliant frame and shear correction.

This ~230 Hz value is a **SANITY-CHECK SCALE ONLY**, not a FEA result or product specification. Real frequencies may move materially when laminate layup, core shear deformation, adhesive, four 110.9 g exciters, edge compliance and fabric are included.

### Immediate modeling implication
The four legacy exciters add about 444 g of rigid device mass in total, which is large relative to the lightweight 300 x 380 mm sandwich panel. Their distributed attachment mass therefore must be present in the first detailed eigenfrequency solve; a bare-panel modal solution is insufficient for placement freeze.

Status: **STACK_A_CORE_BASELINE_FROZEN_FOR_FEA / SKIN_LAMINATE_PROPERTY_GATE_OPEN**.


## 21. Stack-A glass/epoxy skin baseline — 2026-09-29

### Material system selected for detailed numerical baseline
Use **Gurit SE75 with EGL 300 g/m2 unidirectional E-glass** as the first traceable skin-property dataset.

Manufacturer published laminate data for the standard cured system includes:
- cured ply thickness: 0.25 mm;
- fibre volume fraction: 47.3%;
- E-glass fibre density: 2.6 g/cm3;
- E-glass fibre modulus: 69 GPa;
- 0-degree tensile modulus E1: 51 GPa;
- 90-degree tensile modulus E2: 10.7 GPa;
- 0-degree tensile strength: 1499 MPa.

The manufacturer dataset is the authority for the material-card baseline. Missing orthotropic constants needed by the solver (notably G12, nu12, through-thickness properties and damping) must be entered as sensitivity ranges or obtained from supplier/test data; they shall not be silently invented as production constants.

### First skin layup
Detailed FEA Baseline A1:
- outer skin: [0/90], 2 x 0.25 mm = approximately 0.50 mm;
- core: ROHACELL 51 IG-F, 5.0 mm;
- inner skin: mirrored/balanced [90/0], approximately 0.50 mm;
- structural thickness before adhesive: approximately 6.0 mm.

This balanced cross-ply construction is selected for the first solve to reduce extreme directional stiffness and to provide a traceable, manufacturable reference. It is not yet the minimum-mass optimum.

### Required comparison layups
Run at least:
- A1: [0/90] / 5 mm PMI / [90/0];
- A2: thinner quasi-isotropic or woven-glass skin candidate if a traceable commercial material card is available;
- A3: A1 with core thickness reduced/increased within the 3/5/8 mm sweep.

The optimization may later select woven or quasi-isotropic skins if they improve modal distribution, mass and manufacturing robustness.

### Material-card rule
Do not collapse the glass/epoxy skin to the old provisional isotropic 20 GPa assumption. Use classical laminate theory / orthotropic shell properties derived from the ply card. Treat adhesive and core shear explicitly.

### Frequency interpretation
The earlier approximately 230 Hz simply-supported estimate used 0.30 mm isotropic assumed skins and is now superseded as a scale-only historical sanity check. No new absolute eigenfrequency is frozen until the orthotropic solver includes the four exciter masses and compliant perimeter.

Status: **STACK_A1_SKIN_SYSTEM_AND_LAYUP_BASELINE_FROZEN_FOR_DETAILED_FEA / FULL_ORTHOTROPIC_CONSTANT_AND_DAMPING_GATE_OPEN**.


## 22. Stack-A1 mass closure and detailed eigenmodel contract — 2026-09-29

Using the traceable Gurit SE75/EGL300 constituent data (Vf 47.3%, E-glass density 2.6 g/cm3) and SE75 cured-resin density 1.19 g/cm3, the first-order laminate density is approximately **1857 kg/m3** by rule of mixtures.

For the 300 x 380 mm A1 panel:
- two 0.50 mm GFRP skins: approximately **211.7 g**;
- 5.0 mm ROHACELL 51 IG-F core at 52 kg/m3: approximately **29.6 g**;
- structural panel before adhesive/fabric: approximately **241.3 g**;
- four legacy DAEX25FHE-4 devices at 110.9 g each: approximately **443.6 g**;
- panel + four exciters before adhesive/fabric/harness: approximately **684.9 g**.

Thus approximately 64.8% of this preliminary structural moving assembly mass is concentrated in the four complete exciter devices. This makes point/distributed exciter inertia a first-order modal-design variable.

### Detailed eigenmodel implementation rule
The next solver model shall use:
1. orthotropic layered shells (or equivalent laminate formulation) for each GFRP skin;
2. a shear-deformable solid/sandwich core using ROHACELL 51 IG-F E=70 MPa and G=19 MPa baseline;
3. bonded/tied adhesive interfaces for the first solve, followed by adhesive-compliance sensitivity;
4. each exciter represented by its real attachment/contact footprint with distributed rigid mass/inertia, not a mathematical point mass;
5. Candidate-A coordinates as initial attachment centers;
6. compliant perimeter springs/damping rather than only simply-supported or clamped edges;
7. a mesh-convergence check on at least the first 30 modes.

### Frequency reporting rule
Absolute eigenfrequencies shall be reported as bands until G12, nu12, laminate density coupon confirmation, adhesive properties, edge-support stiffness and final exciter revision are closed. Any single-frequency value produced before those gates is diagnostic only.

### Model validation metrics
For each mode retain:
- eigenfrequency;
- modal effective mass;
- surface-velocity participation at L1/L2/R1/R2;
- L/R controllability metric;
- strain-energy share in skins/core/edge support;
- sensitivity to +/- core thickness tolerance;
- sensitivity to exciter mass/position tolerance.

Status: **A1_MASS_MODEL_CLOSED_FOR_FIRST_DETAILED_EIGENSOLVE / ABSOLUTE_FREQUENCY_UNCERTAINTY_GATES_REMAIN**.
