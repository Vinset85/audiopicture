# AudioPicture V2.2 — shell retention clamp-stack gate Rev.AX

Status: **FIXED_1MM_LIMITER_NOT_RELEASED / TOLERANCE_STACK_DOMINATES / COMPLIANT_OR_MATCHED_INTERFACE_REQUIRED**

## Nominal stack
Current CAD:
- rear shell inner plane Z37.8;
- ASA seat inward height 1.8;
- ASA seat front Z36.0;
- coarse PC-CF rear plane Z35.0;
- nominal geometric separation 1.0 mm.

The 1.0 mm value is nominal CAD geometry only.

## Rev.AW sensitivity sweep
Until measured process capability exists, Rev.AW intentionally used broad engineering sensitivity seeds:
- shell plane shift +/-0.30 mm;
- seat-height error +/-0.20 mm;
- PC-CF rear-plane shift +/-0.30 mm.

These are not manufacturing tolerances.

Combined sensitivity produces a possible local gap range:
**0.2 to 1.8 mm**.

## Fixed limiter sweep
Candidate hard limiter heights screened:
0.6 / 0.8 / 1.0 / 1.2 / 1.4 mm.

Across the unqualified sensitivity range, every fixed height can produce either:
- interference/preload before intended screw clamp;
- or residual free gap.

Therefore:
**a fixed 1.0 mm hard spacer is not released.**

## Preferred interim architecture
Keep:
- M3 screw class;
- ASA clearance-hole concept;
- M3 metal thread in PC-CF.

Change the local clamp interface to one of two qualification paths.

Path A — controlled compliant interface:
a thin characterized washer/grommet/interface element accommodates local dimensional variation while a hard stop limits excessive ASA compression.

Path B — measured/matched hard spacer:
measure the assembled shell/frame datum after qualified printing and select/machine a spacer thickness from a controlled set.

Path A is preferable for normal production/service if a suitable material and compression window can be characterized.

## What must be measured
ASA large-panel qualification:
- local inner-plane Z at six nodes;
- seat protrusion;
- flatness/warp after conditioning.

PC-CF frame qualification:
- rear interface Z at six nodes;
- tab flatness;
- local insert/boss geometry after insertion.

Only measured distributions can replace the Rev.AW sensitivity seeds with release tolerances.

## Clamp-load boundary
No screw torque is frozen yet.

Required before torque release:
- exact screw and insert;
- interface material;
- compression curve;
- ASA creep check;
- PC-CF insert pull-out/torque-out;
- vibration/service-cycle test.

## Checks
C1167 nominal local gap 1.0 mm confirmed.
C1168 shell-plane sensitivity +/-0.30 used only as engineering sweep.
C1169 seat-height sensitivity +/-0.20 used only as engineering sweep.
C1170 frame-plane sensitivity +/-0.30 used only as engineering sweep.
C1171 combined sensitivity gap 0.2..1.8 mm.
C1172 fixed 0.6 mm limiter screened.
C1173 fixed 0.8 mm limiter screened.
C1174 fixed 1.0 mm limiter screened.
C1175 fixed 1.2 mm limiter screened.
C1176 fixed 1.4 mm limiter screened.
C1177 no fixed candidate guarantees no-interference/no-gap across current sweep.
C1178 fixed 1.0 mm limiter not released.
C1179 M3 architecture retained.
C1180 ASA remains clearance-hole part.
C1181 metal PC-CF thread retained.
C1182 controlled compliant interface identified as preferred production path.
C1183 measured/matched hard spacer retained as alternate path.
C1184 process capability measurements required at all six nodes.
C1185 clamp torque remains open.
C1186 creep/pull-out/torque-out/service-cycle qualification required.

Status:
**RETENTION_STACK_REV_AX / NOMINAL_GAP_1P0 / SENSITIVITY_0P2_TO_1P8 / FIXED_LIMITER_REJECTED_FOR_NOW / COMPLIANT_INTERFACE_NEXT / C01_TO_C1186**.
