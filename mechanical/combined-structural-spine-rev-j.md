# AudioPicture V2.2 — combined magnetic-to-rear structural spine Rev.J

Status: **COMBINED_KERNEL_DEFINED / BOOLEAN_CONNECTIVITY_CONTRACT_FROZEN / DML_ZERO_INTERSECTION_REQUIRED / FEA_AFTER_RUNTIME_RESULT**

## 1. Purpose
Combine the previously separated real/diagnostic structural kernels into one reproducible OpenCASCADE model:
- rear PC-CF one-solid base Rev.C;
- eight segmented perimeter returns Rev.I;
- eight front target tabs Rev.H.

This is the first model intended to prove a continuous CAD load path from each magnetic target node to the rear structural ring.

## 2. Geometry imported by construction
Rear:
- outer boundary X2..318 / Y2..398;
- 10 mm ring;
- Z27..35;
- cleat islands fused into top ring;
- known coarse keep-outs subtracted.

Returns:
- 8 local wall blades;
- 10 mm tangential width;
- 2.4 mm radial thickness;
- Z6..29.

Front tabs:
- 8 local tab envelopes;
- 10 mm tangential width;
- approximately 2.0 mm radial thickness;
- Z5.1..9.2.

## 3. Required boolean chain
For every station Mi:
1. rear ring intersects return with positive volume;
2. return intersects front tab with positive volume;
3. union is cleaned;
4. final structural assembly has one connected solid.

Touching at a zero-area/zero-volume boundary is not accepted as structural fusion proof.

## 4. DML gate
DML hard volume:
- X10..310;
- Y10..390;
- Z3.3..9.3.

Combined structural intersection shall equal:
**0 mm3**.

This check is authoritative for the nominal kernel geometry.

## 5. Connectivity acceptance
PASS only if all are true:
- B-rep valid;
- final solid_count == 1;
- disconnected_fragments == 0;
- every rear-return overlap >0 mm3;
- every return-tab overlap >0 mm3;
- DML intersection ==0 mm3.

If any condition fails, Rev.J does not advance to FEA.

## 6. What this proves
A passing Rev.J kernel proves only:
- nominal geometric connectivity of the PC-CF structural path;
- nominal absence of DML hard-volume collision.

It does not prove:
- stress margin;
- stiffness/G_EFF stability;
- fatigue;
- print anisotropy performance;
- RF compatibility;
- thermal airflow;
- manufacturing tolerance closure.

## 7. FEA handoff
Only after kernel PASS, mesh local station submodels including:
- target load application surface;
- target holder;
- front tab;
- perimeter return;
- rear-ring root.

Load seeds retained:
- 5 N normal;
- 2 N tangential;
- 10 N installation/service proof.

Material:
qualified printed PC-CF orthotropic properties required before release-level conclusions.

## 8. RF and thermal exclusions
Rev.J does not upgrade:
- ESP32 coarse compatibility to exact PASS;
- radar OPEN to PASS;
- passive thermal status.

The segmented returns remain editable/suppressible before release.

## 9. Automatic checks
C646 combined rear/return/tab generator created.
C647 rear Rev.C one-solid topology reconstructed in same kernel.
C648 eight Rev.I returns reconstructed.
C649 eight Rev.H front tabs reconstructed.
C650 each rear-return overlap measured as positive-volume boolean.
C651 each return-tab overlap measured as positive-volume boolean.
C652 zero-volume touching prohibited as connectivity evidence.
C653 combined B-rep validity required.
C654 combined solid count required ==1.
C655 disconnected fragments required ==0.
C656 DML hard-volume intersection required ==0 mm3.
C657 nominal geometric PASS not treated as structural FEA PASS.
C658 nominal geometric PASS not treated as tolerance PASS.
C659 ESP32 exact RF gate remains open.
C660 radar exact EM gate remains open.
C661 thermal airflow gate remains open.
C662 local FEA starts only after Rev.J runtime PASS.
C663 5 N normal structural seed retained.
C664 2 N tangential structural seed retained.
C665 10 N installation/service seed retained.
C666 qualified PC-CF orthotropic data required for release FEA.

## 10. State
The project now has a single reproducible generator that encodes the complete nominal magnetic-retention structural spine from front target tab to rear PC-CF frame.

Status remains **PENDING_RUNTIME_RESULT** until the generator is executed in a CadQuery/OpenCASCADE environment and its reported boolean metrics are recorded.

Status:
**COMBINED_STRUCTURAL_SPINE_GENERATOR / C01_TO_C666 / RUNTIME_BOOLEAN_PASS_REQUIRED_BEFORE_FEA**.
