# AudioPicture V2.2 Rev.A — small-magnet trade study

Status: **4X2MM_N45_PREFERRED / 5X1MM_N45_ALTERNATE / 3P17X1P59MM_TOO_MARGIN_SENSITIVE / 6X2MM_BASELINE_DEMOTED**

## 1. Objective
Re-evaluate the front-frame magnetic retention using smaller magnets to reduce:
- DML perimeter intrusion;
- local carrier pad size;
- magnetic/steel mass;
- RF perturbation area;
- peel force.

Target assembled total normal retention remains 20..30 N with 8 distributed stations.

Catalogue pull force is not assembled force.

## 2. Candidates

### A — supermagnete S-04-02-N
- disc 4 x 2 mm
- NdFeB N45
- nickel plated
- axial
- manufacturer attraction approx 420 g, about 4.12 N, under manufacturer conditions
- mass approx 0.19 g
- preferred new packaging reference.

Eight magnets mass:
~1.52 g.

Ideal catalogue-force sum:
~33 N, deliberately not used as assembly prediction.

### B — supermagnete S-05-01-N
- disc 5 x 1 mm
- NdFeB N45
- manufacturer attraction approx 320 g, about 3.14 N
- mass approx 0.15 g.

Eight:
~1.20 g.

Very attractive Z packaging, but wider XY than Candidate A.

### C — K&J D21SH
- 3.17 x 1.59 mm
- N42SH
- Pull Force Case 1 0.45 lb, approximately 2.0 N
- high-temperature grade.

Eight ideal Case-1 sum:
~15.7 N.

Because target assembled requirement is 20..30 N and real gaps reduce force, this candidate is not preferred for an 8-station architecture.

It could become viable with more stations, magnet-to-magnet circuits, or lower retention requirement, none baseline.

### D — previous 6 x 2 mm class
Previous packaging reference is demoted.

Reason:
more XY pad area and catalogue attraction than needed.

## 3. Decision
Preferred:
**S-04-02-N / 4 x 2 mm / N45**

Alternate:
**S-05-01-N / 5 x 1 mm / N45**

The 4 x 2 mm part gives the best current balance between:
- compact XY footprint;
- enough magnetic authority;
- manageable 2 mm Z;
- eight-station distributed retention.

## 4. Revised pocket
Preferred magnet pocket:
- nominal diameter 4.4 mm before process compensation;
- depth 2.2 mm class.

Local station pad:
- D-shaped;
- nominal outer width 8 mm;
- perimeter-direction length 9..10 mm;
- DML-facing edge clipped to hard DML keep-out.

This replaces the old 12 mm circular pad.

## 5. Revised station coordinates
Use Rev.B centers:
M1B (70,388)
M2B (250,388)
M3B (70,12)
M4B (250,12)
M5B (12,135)
M6B (12,275)
M7B (308,135)
M8B (308,315).

D-shaped pads grow toward product perimeter, not toward DML.

## 6. DML edge geometry
DML projection:
X10..310
Y10..390.

Station centers are only 2 mm from the DML projected edge.

Therefore even 8 mm pads require clipping.

Hard rule:
DML-facing pad edge shall terminate before DML hard-clearance mask.

The carrier perimeter itself may overlap the projected DML edge only where its Z placement remains outside the DML/fabric dynamic clearance; magnet thickening may not.

## 7. Force strategy
For Candidate A:
manufacturer attraction ~4.12 N per magnet in its reference condition.

Product target average:
2.5..3.75 N/station if equal.

Therefore the preferred magnet is in the correct order of magnitude.

Use:
- controlled target thickness;
- polymer/adhesive gap;
- local target area
to tune the assembled curve.

Initial G_MAG sweep:
0.2 / 0.4 / 0.6 / 0.8 mm.

The previous 1.0/1.2 mm upper sweep is retained only as diagnostic because a smaller magnet loses force faster with separation.

## 8. Target geometry
Initial discrete steel target:
- 7 x 7 mm square or 8 mm disc class
- thickness 0.8 / 1.0 / 1.2 mm sweep.

No continuous steel.

Exact low-carbon steel grade/coating remains open.

## 9. Peel requirement
Smaller magnets are beneficial because the front frame should release progressively.

Evaluate:
- total normal pull;
- lower-center initial peel;
- second-station release;
- re-seat snap energy.

Reject any configuration that:
- requires excessive fingernail/tool force;
- snaps violently onto DML/front system;
- rattles under DML vibration.

## 10. RF benefit
Smaller magnet/target geometry reduces metal area but does not eliminate RF validation.

All radar/ESP32 exclusion rules remain mandatory.

## 11. Mass benefit
Preferred 4 x 2:
~1.52 g total magnets.

Previous 6 x 2 reference:
~3.44 g total.

Reduction:
~1.92 g magnets, about 56 percent.

The larger benefit is local pad/target footprint, not mass alone.

## 12. Thermal
Standard N45 candidate has 80 C class manufacturer limit.

This remains adequate as a candidate only if measured front-frame temperatures stay well below it with margin.

High-temperature SH variants remain fallback if thermal test requires.

## 13. Validation matrix
M0 no magnet.
M1 4x2 + 0.2 gap.
M2 4x2 + 0.4 gap.
M3 4x2 + 0.6 gap.
M4 4x2 + 0.8 gap.
M5 5x1 alternate.
M6 3.17x1.59 diagnostic.

For each:
- normal force/station;
- total frame pull;
- peel force curve;
- lateral slip;
- vibration/rattle;
- temperature;
- radar;
- Wi-Fi.

## 14. Automatic checks
C431 smaller-magnet study completed.
C432 4x2 N45 selected preferred.
C433 5x1 N45 retained alternate.
C434 3.17x1.59 rejected as 8-station baseline due force margin.
C435 6x2 baseline demoted.
C436 preferred pocket diameter reduced to 4.4 mm seed.
C437 station pad reduced from 12 mm circle to ~8 x 9..10 mm D-shape.
C438 DML-facing pad clipped to hard keep-out.
C439 Rev.B magnet coordinates retained.
C440 G_MAG small-magnet sweep 0.2..0.8 mm defined.
C441 discrete target reduced to 7..8 mm class.
C442 no catalogue-force multiplication accepted as proof.
C443 total retention target remains 20..30 N.
C444 peel curve required.
C445 RF validation retained.
C446 eight preferred magnets mass ~1.52 g.
C447 standard N45 thermal limit checked against product test.
C448 alternate magnet remains regenerable.
C449 exact target steel/coating open.
C450 Rev.B carrier CAD regeneration required.

## 15. State
Preferred front-frame magnetic system:
**8 x S-04-02-N / 4 x 2 mm N45 / D-shaped local pads / discrete 7..8 mm steel targets**

Status:
**SMALL_MAGNET_ARCHITECTURE_SELECTED / 4X2MM_N45 / 8_STATIONS / 20_TO_30N_ASSEMBLY_TARGET / C01_TO_C450 / REV_B_CAD_REGENERATION_NEXT**.
