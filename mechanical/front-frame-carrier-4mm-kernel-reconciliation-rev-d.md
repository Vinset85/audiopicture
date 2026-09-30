# AudioPicture V2.2 — front carrier magnetic baseline reconciliation and real kernel gate

Status: **4X2MM_MAGNET_BASELINE_RECONFIRMED / REAL_BREP_PASS / 6P6MM_POCKET_WITHDRAWN / DML_CLEARANCE_CLOSED_AT_CAD_LEVEL**

## 1. Purpose
Reconcile the conflicting late Rev.B documents and execute the next real CAD-kernel gate against the current master geometry.

The repository contains both:
- a miniaturized 4 x 2 mm N45 baseline with 4.4 mm pocket; and
- later documents that accidentally returned to a 6.6 mm pocket without explicitly superseding the miniaturization decision.

This document resolves that inconsistency using a real CadQuery/OpenCASCADE rebuild.

## 2. Governing geometry
Carrier outer boundary:
- X = 0.8..319.2 mm
- Y = 0.8..399.2 mm
- 318.4 x 398.4 mm.

DML hard projected rectangle:
- X = 10..310 mm
- Y = 10..390 mm.

Base carrier thickness:
- 1.8 mm.

Local magnetic-station total thickness:
- 3.2 mm.

DML rigid keep-out seed:
- 0.5 mm.

## 3. First real kernel test — 6.6 mm pocket
The current M*C coordinates were rebuilt with:
- pocket diameter 6.6 mm;
- pocket depth 2.2 mm;
- clipped perimeter-biased station thickening;
- lower peel recess;
- provisional rear mechanical-capture nubs.

Kernel result:
- B-rep validity: PASS
- connected solids: 1
- volume: 25,315.04 mm3
- bounding box: 318.4 x 398.4 x 3.2 mm
- station-thickening/DML intersection: 0 mm3
- minimum pocket-to-DML projected clearance: 0.7 mm
- minimum pocket-to-carrier-outer-boundary wall: 1.9 mm.

However, the DML-facing structural ligament inside the legal station strip is only:
0.7 - 0.5 = **0.2 mm**.

This violates the already stated local polymer ligament target >=1.2 mm.

Therefore the 6.6 mm pocket is **REJECTED** for this flat perimeter station architecture even though the B-rep itself is valid.

A valid kernel is not sufficient evidence of a mechanically acceptable design.

## 4. Reconciled baseline
The prior miniaturization decision is restored as authoritative:

Primary magnet packaging reference:
- Supermagnete S-04-02-N class
- 4 mm diameter
- 2 mm thickness
- N45 class.

Nominal CAD pocket:
- **4.4 mm diameter**
- 2.2 mm diagnostic depth.

Eight stations remain the baseline.

The 20..30 N assembled front-frame retention target is unchanged and remains a physical coupon/test gate.

## 5. Real kernel — 4.4 mm pocket
A second real CadQuery 2.8 / OpenCASCADE 7.9.3 B-rep was generated using the same carrier geometry and station centers:

Top:
- M1D = (70,394)
- M2D = (250,394)

Bottom:
- M3D = (70,6)
- M4D = (250,6)

Left:
- M5D = (6,135)
- M6D = (6,275)

Right:
- M7D = (314,135)
- M8D = (314,315).

The D suffix identifies the reconciled 4.4 mm-pocket kernel seed; it does not change the station center locations.

## 6. Kernel result
Real result:
- kernel validity: **PASS**
- connected solid count: **1**
- disconnected fragments: **0**
- volume: **25,649.48 mm3 = 25.649 cm3**
- bounding box: **318.4 x 398.4 x 3.2 mm**
- station-thickening/DML hard-region intersection: **0 mm3**
- minimum pocket-to-DML projected clearance: **1.8 mm**
- DML hard keep-out: **0.5 mm**
- resulting minimum DML-facing structural ligament: **1.3 mm**
- minimum pocket-to-carrier-outer-boundary wall: **3.0 mm**
- pocket count: **8**.

The 1.3 mm DML-facing ligament meets the >=1.2 mm diagnostic structural target.

## 7. Carrier mass
Using the existing unfilled-ASA sensitivity:
- 1.05 g/cm3 -> 26.93 g
- 1.075 g/cm3 -> 27.57 g
- 1.10 g/cm3 -> 28.21 g.

Carrier-only mass remains far below the 60 g ceiling.

This excludes fabric, ink, adhesive, magnets and steel targets.

## 8. Mechanical capture
The diagnostic kernel includes three small rear snap-nub seeds per pocket to prove that mechanical capture can coexist with the pocket and remain one connected solid.

These nub dimensions are **NOT production-frozen**.

Production capture still requires:
- print-process coupon;
- insertion/removal force;
- creep/temperature assessment;
- magnet tolerance;
- no loose-part failure.

Adhesive remains secondary retention only.

## 9. Peel recess
The lower-center peel recess is retained.

It does not disconnect the carrier.

M3D/M4D remain separated from the X160 peel initiation region.

## 10. Global Z transform
Local carrier CAD:
- base Z = 0..1.8 mm
- local station Z = 0..3.2 mm.

Assembly transform:
- local Z0 -> product-global Z0.5 mm, immediately behind the nominal fabric thickness.

Therefore:
- base carrier global Z = 0.5..2.3 mm
- station local thickening global Z = 0.5..3.7 mm.

The station thickening is legal only because its XY footprint is outside the DML hard projection.

The active DML remains:
- front Z3.3
- rear Z9.3.

No central carrier slab is introduced.

## 11. Supersession
The following late assumption is withdrawn:
- 6 x 2 mm magnet / 6.6 mm pocket as the active flat-perimeter front-carrier baseline.

The 6.6 mm result remains useful diagnostic evidence showing why kernel validity alone did not close the station design.

The authoritative baseline becomes:
- 4 x 2 mm N45 class magnet
- 4.4 mm pocket
- eight perimeter stations
- same M* center locations used by the corrected kernel
- 10-station fallback only if measured assembled retention is below target and RF/peel checks allow it.

## 12. Remaining gates
Still open:
- exact manufacturer verification for the selected 4 x 2 mm magnet at sourcing/release;
- production capture geometry;
- magnetic force coupon with actual steel target/gap;
- exact ESP32 RF mask;
- exact radar EM mask;
- fabric process and bonding-land detail;
- print compensation/warp capability;
- full transformed master-DMU exact STEP collision solve.

No FEA/CFD result is claimed here.

## 13. Reproducibility
Generator:
`mechanical/cad/generate_front_carrier_rev_b_4mm.py`

Local DMU artifact generated during this gate:
`AP22_FRONT_CARRIER_REV_B_4MM_DMU.step`

The STEP is a DMU artifact, not manufacturing release.

## 14. Automatic checks
C471 conflicting 6.6 mm and 4.4 mm late baselines identified.
C472 6.6 mm real B-rep generated and kernel-valid.
C473 6.6 mm B-rep one connected solid.
C474 6.6 mm pocket-to-DML clearance measured at 0.7 mm.
C475 6.6 mm DML-facing ligament calculated at only 0.2 mm after 0.5 mm keep-out.
C476 6.6 mm flat-perimeter pocket rejected against >=1.2 mm ligament target.
C477 4 x 2 mm N45 / 4.4 mm pocket baseline reconfirmed.
C478 4.4 mm real B-rep generated.
C479 4.4 mm B-rep validity PASS.
C480 4.4 mm connected solid count == 1.
C481 4.4 mm volume recorded at 25,649.48 mm3.
C482 4.4 mm bounding box == 318.4 x 398.4 x 3.2 mm.
C483 station-thickening/DML hard-region intersection == 0 mm3.
C484 minimum pocket-to-DML projected clearance == 1.8 mm.
C485 minimum DML-facing structural ligament == 1.3 mm.
C486 minimum outer structural wall == 3.0 mm.
C487 eight pockets generated.
C488 peel recess preserves connectivity.
C489 global-Z transform defined without changing frozen master datum.
C490 production capture, force coupon and exact RF/EM masks remain open release gates.

## 15. State
The front-carrier magnetic geometry is now internally consistent at CAD-kernel level.

The 6.6 mm pocket path is withdrawn because it leaves an unacceptable 0.2 mm DML-facing ligament.

The 4.4 mm pocket path passes the current geometric/structural-ligament gate with a real one-solid OpenCASCADE B-rep.

Status:
**FRONT_CARRIER_4MM_MAGNET_BASELINE / REAL_ONE_SOLID_BREP / 25P649CM3 / DML_INTERSECTION_ZERO / 1P3MM_MIN_DML_SIDE_LIGAMENT / C01_TO_C490 / FORCE_RF_PROCESS_GATES_OPEN**.
