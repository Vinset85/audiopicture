# AudioPicture V2.2 — rear PC-CF real kernel connectivity gate Rev.C

Status: **REAL_OPENCASCADE_KERNEL_EXECUTED / FIRST_BRIDGE_TOPOLOGY_REJECTED / ONE_SOLID_BASE_KERNEL_PASS / TAB_UNION_NOT_YET_CLAIMED**

## 1. Purpose
Execute the previously pending rear-frame CAD kernel before attempting structural union of the eight front magnetic target tabs.

## 2. Repository evidence
Before this gate the repository contained no STEP/STP/BREP/FCStd rear-frame artifact and no rear-frame generator.

The G2 primitive map explicitly stated FEA_SOLID_PENDING.

Therefore no prior claim of a real rear-frame B-rep was accepted.

## 3. Kernel environment
Executed with:
- CadQuery 2.8.0;
- OpenCASCADE backend through CadQuery.

## 4. First generated topology
The first diagnostic implementation instantiated:
- 10 mm outer ring;
- cleat islands;
- side-rail/bridge seeds;
- lower bridges;
- upper bridges;
- coarse known keep-out subtraction.

Real kernel result:
- B-rep validity: PASS;
- connected solids: **3**;
- volume: approximately 241,296 mm3;
- bounding box: 316 x 396 x 8 mm.

This topology is rejected as a structural baseline because kernel validity does not imply load-path connectivity.

## 5. Root cause
Some bridge primitives survived keep-out subtraction as isolated islands.

The primitive map describes bridge centerlines/seeds, but it does not guarantee that every raw bridge remains connected after booleans.

Therefore automatic restoration of all seed bridges is unsafe.

## 6. Corrected strategy
Return to the minimum topology already guaranteed by the structural contract:
- one closed outer PC-CF ring;
- two cleat islands deliberately overlapping the top ring;
- coarse keep-out subtraction;
- no speculative disconnected mid-bridge restoration.

Then add local bridges incrementally only when each bridge:
1. intersects the existing primary body;
2. survives all hard keep-outs;
3. leaves one connected primary body;
4. does not violate airflow/RF/service constraints.

## 7. Corrected real kernel
Corrected kernel executed locally:
- B-rep validity: **PASS**;
- connected solids: **1**;
- volume: approximately **141,824 mm3**;
- bounding box: **316 x 396 x 8 mm**;
- global Z: **27..35 mm**.

This is the first real one-solid rear PC-CF base kernel in the project.

It is a topology/FEA seed, not manufacturing release.

## 8. Mass seed
At an illustrative PC-CF density of 1.20 g/cm3:
- 141.824 cm3 -> approximately 170.2 g.

Density is not frozen here.

The geometry is therefore plausibly inside the existing <=250 g frame mass target, but released mass requires actual selected-material density and final bridge/boss geometry.

## 9. Why front-tab union is not yet executed
Front target-holder/tab region is around Z5..9 mm.

Rear PC-CF base kernel is Z27..35 mm.

There is currently no authoritative real perimeter side-section solid connecting those Z regions.

A direct union would require inventing a roughly 18+ mm structural transition.

That is explicitly prohibited by Rev.H.

Therefore:
**no false tab/rear-frame union is claimed.**

## 10. Next real CAD gate
Generate the legal perimeter side-section/return geometry that connects:
- front local target tab;
- enclosure perimeter structural section;
- rear PC-CF outer ring.

It must be derived from actual shell/frame section constraints and clipped against:
- DML/PORON;
- electronics;
- exciter keep-outs;
- ESP32 RF;
- radar RF;
- service/airflow.

Only then may the eight tabs be fused and one-solid connectivity tested.

## 11. Automatic checks
C596 repository contained no prior rear-frame STEP/B-rep.
C597 G2 primitive map FEA_SOLID_PENDING state confirmed.
C598 CadQuery 2.8 real kernel executed.
C599 first raw bridge topology B-rep valid.
C600 first raw bridge topology produced 3 solids.
C601 3-solid topology rejected as structural baseline.
C602 disconnected bridge restoration identified as failure mode.
C603 speculative bridge restoration removed.
C604 closed 10 mm outer ring retained.
C605 cleat islands overlap top ring to guarantee fusion.
C606 corrected kernel B-rep valid.
C607 corrected kernel connected solid count == 1.
C608 corrected kernel volume approximately 141,824 mm3.
C609 corrected kernel bounding box 316x396x8 mm.
C610 corrected kernel global Z 27..35 mm.
C611 corrected kernel is topology/FEA seed only.
C612 illustrative 1.20 g/cm3 mass approximately 170.2 g.
C613 released mass remains material/final-geometry dependent.
C614 front tabs not directly bridged across unsupported Z gap.
C615 no fictitious 18+ mm post generated.
C616 real perimeter side-section required before tab union.
C617 local bridges to be restored incrementally with connectivity assertion.
C618 exact exciter/RF/service solids remain release gates.
C619 rear-frame generator corrected to one-solid base strategy.
C620 front-tab/rear-frame one-solid union remains next-after-side-section gate.

## 12. State
The rear frame has progressed from a paper primitive map to a real one-solid OpenCASCADE base kernel.

A failed 3-solid intermediate topology was detected and rejected rather than hidden.

The remaining blocker for front magnetic-node integration is now precise:
**the real perimeter side-section connecting Z~6 to the rear ring at Z27 must be defined without inventing an unsupported post.**

Status:
**REAR_PC_CF_REAL_KERNEL / ONE_SOLID_BASE_PASS / 141P824CM3 / Z27_TO_35 / C01_TO_C620 / PERIMETER_SIDE_SECTION_NEXT**.
