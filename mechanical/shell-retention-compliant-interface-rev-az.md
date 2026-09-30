# AudioPicture V2.2 — compliant retention interface architecture Rev.AZ

Status: **CONCENTRIC_INTERFACE_PACKAGING_PASS / FULL_0P2_TO_1P8_GAP_NOT_SOLVABLE_BY_GENERIC_COMPLIANT_PAD / GRADED_SPACER_PLUS_COMPLIANT_TRIM_PREFERRED**

## Geometry screen
Rev.AY fits a concentric interface inside the existing 10 mm ASA seat.

Packaging seeds only:
- M3 screw class;
- clearance-hole diameter 3.6 mm seed;
- hard-stop sleeve/shoulder OD 6.0 mm seed;
- compliant annulus OD 9.0 mm seed;
- seat OD 10.0 mm.

This leaves:
- 0.5 mm radial outer packaging land between compliant OD and seat edge;
- 1.5 mm radial compliant annulus between hard-stop OD and compliant OD.

No diameter above is a released manufacturing dimension.

## Key tolerance result
Rev.AX current unqualified gap sensitivity:
0.2..1.8 mm.

A compliant element thick enough to bridge 1.8 mm must have approximately 2 mm free thickness or more.

At the opposite 0.2 mm gap, a 2.0 mm element would require up to 1.8 mm compression before geometric closure, approximately 90% of free thickness.

Without a specifically characterized material, this is not a credible generic design assumption.

Therefore:
**do not use one generic compliant washer to absorb the entire 0.2..1.8 mm sensitivity range.**

## Preferred architecture
Use two-stage dimensional accommodation:

1. graded hard spacer / shoulder class
   - selected from a small controlled thickness family after process capability is known or local gap is measured;

2. thin compliant trim washer
   - absorbs only residual local variation;
   - prevents rattle;
   - avoids high ASA local stress;
   - compression window defined from actual material data.

The hard element remains the compression stop.
The compliant element is not the structural stop.

## Why this is better
It separates functions:
- hard spacer controls clamp geometry;
- compliant washer controls residual tolerance/noise;
- M3 screw supplies retention;
- metal PC-CF insert supplies durable thread;
- ASA shell remains unthreaded and replaceable.

## Next qualification
Before freezing spacer classes:
- print/measure representative ASA shell;
- print/measure representative PC-CF frame;
- record local gap at all six nodes;
- determine real min/max and distribution.

Before freezing compliant washer:
- choose candidate material;
- obtain compression-force/deflection data;
- check compression set/creep at product temperature;
- define residual compression window.

## Checks
C1187 concentric interface fits inside D10 seat at packaging level.
C1188 M3 clearance-hole seed 3.6 mm not released.
C1189 hard-stop OD6 seed not released.
C1190 compliant OD9 seed not released.
C1191 full current gap sensitivity remains 0.2..1.8 mm.
C1192 2 mm compliant free thickness can geometrically bridge 1.8 mm.
C1193 same 2 mm element could require ~90 percent compression at 0.2 mm gap.
C1194 generic compliant-only solution rejected for full current range.
C1195 hard spacer retains compression-stop function.
C1196 thin compliant element becomes residual tolerance/rattle trim only.
C1197 graded/matched spacer architecture preferred.
C1198 actual six-node dimensional measurement required.
C1199 compliant material compression data required.
C1200 creep/compression-set qualification required.

Status:
**RETENTION_INTERFACE_REV_AZ / M3_CONCENTRIC_PACKAGING_PASS / COMPLIANT_ONLY_REJECTED / GRADED_HARD_SPACER_PLUS_COMPLIANT_TRIM / C01_TO_C1200**.
