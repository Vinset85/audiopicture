# AudioPicture V2.2 Rev.A — Full DML / frame FEA contract

Status: **FULL_FEA_MODEL_CONTRACT_FROZEN / MATERIAL_AND_MOUNT_STIFFNESS_CALIBRATION_OPEN**

## 1. Scope
This contract supersedes reduced-order models for production decisions. It defines the coupled structural model used to compare Candidate A/B, select the DML stack and derive the complex electrical/acoustic load used by the audio release process.

Fixed outer product envelope remains 320 x 400 x 40 mm maximum. Active DML baseline is 300 x 380 mm.

## 2. Solver model
Use a linear eigenfrequency solve first, followed by harmonic response and acoustic coupling for shortlisted configurations.

Preferred structural representation:
- layered orthotropic shell or continuum-shell elements for each GFRP face;
- 3D shear-deformable solid elements for the PMI core;
- explicit adhesive layers where solver conditioning permits, otherwise calibrated cohesive/interface elements;
- rigid/distributed exciter bodies coupled over their physical attachment footprints;
- spring/solid representation of the compliant perimeter mount;
- rear-frame structural members included once their CAD section is frozen.

Do not release production coordinates from a homogeneous equivalent-plate model.

## 3. Baseline material stack A1
Outer skin:
- Gurit SE75 + EGL300 E-glass property dataset;
- [0/90], nominal 0.50 mm total.

Core:
- ROHACELL 51 IG-F;
- nominal 5.0 mm;
- density 52 kg/m3 baseline;
- E = 70 MPa baseline;
- G = 19 MPa baseline.

Inner skin:
- mirrored/balanced [90/0], nominal 0.50 mm.

Nominal structural thickness before adhesive = approximately 6.0 mm.

Missing laminate constants and damping remain sensitivity variables until traceable data/coupon correlation exists.

## 4. Exciter model
Legacy comparison device: DAEX25FHE-4.
Successor comparison device: EX25FHE2-4.

For legacy structural initialization:
- complete device mass 110.9 g each;
- moving mass Mms 1.61 g belongs to the electromechanical submodel and shall not be double counted;
- Re 4.3 ohm;
- Le 0.10 mH;
- BL 3.63 Tm;
- free-air Fs about 224 Hz.

Apply rigid mass/inertia through the actual exciter mounting/contact footprint. Do not use a zero-area point mass for the release solve.

## 5. Candidate coordinates
Candidate A:
- L1 (50,83)
- L2 (96,169)
- R1 (204,243)
- R2 (237,123) mm.

Candidate B:
- L1 (58,70)
- L2 (104,186)
- R1 (196,258)
- R2 (244,108) mm.

Coordinates reference lower-left corner of the 300 x 380 mm active panel.

## 6. Mesh requirements
Perform a convergence study rather than fixing one arbitrary mesh.

Initial guidance:
- global panel in-plane element size <=8 mm;
- refine to <=3 mm around exciter attachment/contact boundaries;
- refine to <=3 mm around perimeter-mount transitions, cut-outs and stiffness discontinuities;
- through-core solid mesh must resolve transverse shear adequately;
- adhesive/cohesive interfaces shall have compatible local discretization.

Convergence acceptance:
- first 30 eigenfrequencies: median change <1% and maximum change <3% between final two mesh levels;
- modal assurance / shape comparison shall be used where mode ordering swaps;
- harmonic-response peaks of interest shall be checked separately.

## 7. Perimeter mount
The panel shall not be modeled only as perfectly clamped or simply supported.

Use three mount-stiffness cases:
- SOFT;
- NOMINAL;
- STIFF.

Until a production elastomer geometry/material is selected, mount stiffness is a parameter sweep. Include normal, in-plane and rotational restraint where supported by the chosen element formulation.

The final enclosure shall avoid hard bridges from DML panel to VOICE PCB support.

## 8. Adhesive
Model two adhesive interfaces:
1. skin-to-core structural bond;
2. exciter-to-panel attachment.

Required sensitivity variables:
- elastic/shear modulus;
- bond-line thickness;
- loss factor;
- temperature dependence;
- creep/durability as a later mechanical-release gate.

No adhesive product is frozen by this contract.

## 9. Eigenfrequency output
Compute at least the first 50 modes and retain:
- frequency;
- modal effective mass;
- generalized mass;
- strain-energy partition by skin/core/adhesive/mount;
- displacement/velocity at all four exciter footprints;
- L/R controllability metric;
- mode-shape correlation between mesh/material cases.

Absolute frequencies remain bands until material/mount uncertainty closes.

## 10. Harmonic structural response
For Candidate A and B run at minimum 20 Hz..20 kHz with dense resolution around modes.

Excitation cases:
- LEFT only: L1+L2 in phase;
- RIGHT only: R1+R2 in phase;
- L+R common;
- L-R differential diagnostic.

Retain surface velocity field, mount reaction forces and strain/stress hot spots.

## 11. Acoustic coupling
For shortlisted structural cases, couple normal panel velocity to an acoustic domain / validated boundary-element equivalent.

Evaluate:
- 0.5 m and 1.0 m;
- center and representative horizontal/vertical listening angles;
- spatial average over a listening window;
- L/R transfer functions and cross-correlation;
- wall-mounted rear boundary condition.

Printed fabric shall enter as measured/estimated distributed mass, damping and acoustic transmission only after its final construction is known.

## 12. Radar / VOICE / ENV exclusion volumes
Import shared CAD keep-outs before coordinate freeze.

Mandatory:
- no conductive skin/hardware through RADAR_RF_KEEP_OUT unless EM-qualified;
- no exciter body/strong structural bridge in VOICE isolation volume;
- ENV passive-air chamber shall not be used as a DML structural brace;
- harnesses shall not preload the active panel.

## 13. Tolerance and robustness sweep
For the winning candidate evaluate:
- each exciter center +/-2 mm;
- core thickness manufacturing tolerance;
- skin thickness/property tolerance;
- exciter mass tolerance if available;
- SOFT/NOMINAL/STIFF perimeter;
- adhesive property corners.

Reject solutions that win only at a narrow nominal point.

## 14. Coupled electrical output
After structural/acoustic selection, generate complex mounted impedance Z(f) for each exciter and each two-exciter series branch.

That Z(f) is the authority for TAS5825M LC-filter simulation. Until then 10 uH / 0.68 uF remains the capture/reference network only.

## 15. Release criteria
Candidate B may replace Candidate A only if the full model shows a robust improvement in modal controllability/acoustic smoothness without materially degrading stereo separation, stress, reaction force or manufacturability.

Production DML placement freeze requires:
- converged structural mesh;
- material sensitivity complete;
- mount sensitivity complete;
- A/B acoustic comparison;
- exciter revision decision;
- tolerance sweep;
- radar/VOICE CAD clearance;
- LC co-simulation using generated Z(f).
