# AudioPicture V2.2 — lower inlet executed layout Rev.AD

Status: **REV_AC_EXECUTED_PASS / DISTRIBUTED_SYMMETRIC_LOWER_INLET_PREFERRED / FULL_SHELL_INTEGRATION_READY**

## Executed result
Rev.AB exhaustive optimization was attempted but exceeded the practical runtime budget; it is not treated as a PASS.

Rev.AC replaced the combinatorial search with a deterministic three-band construction and was executed.

Selected real R1.5 capsule slots, global XY mm:

Left:
- IL1 V X4..7 Y4..44
- IL2 V X11..14 Y4..44
- IL3 V X4..7 Y52..92
- IL4 V X11..14 Y52..92
- IL5 V X4..7 Y104..144
- IL6 V X11..14 Y104..144

Right:
- IR1 V X313..316 Y4..44
- IR2 V X306..309 Y4..44
- IR3 V X313..316 Y52..92
- IR4 V X306..309 Y52..92
- IR5 V X313..316 Y104..144
- IR6 V X306..309 Y104..144

The topology is symmetric about X=160 and distributed over three lower Y bands.

## Geometry
- 12 slots total, 6 per side;
- 3 x 40 mm overall capsule envelope;
- R1.5 ends;
- minimum nominal pairwise web: 4.0 mm;
- 2.0 mm conservative expansion applied to documented keep-outs;
- support-pad seed envelopes included;
- conservative anti-lift solver envelope included.

## Real opening area
Per capsule:
(40-3)*3 + pi*1.5^2 = 118.0686 mm2.

Total:
1416.8230 mm2.

At preliminary 0.75 sizing factor:
1062.6173 mm2.

Preferred inlet target:
900 mm2.

Seed margin:
+162.6173 mm2.

The 0.75 factor remains a preliminary CAD sizing proxy, not CFD.

## Limits
Still open:
- exact cable/harness swept solids;
- final lower-support geometry;
- final anti-lift hardware envelope;
- CFD;
- physical ASA dimensional qualification.

## Checks
C986 Rev.AB runtime complexity identified and not misreported as PASS.
C987 deterministic Rev.AC executed.
C988 12 slots selected.
C989 6 left + 6 right.
C990 layout symmetric about X160.
C991 three Y bands used.
C992 slot envelope 3x40 mm.
C993 R1.5 real geometry basis retained.
C994 minimum nominal web 4.0 mm.
C995 documented keep-outs expanded by 2.0 mm.
C996 lower support seed envelopes protected.
C997 anti-lift conservative envelope protected.
C998 real gross inlet area 1416.8230 mm2.
C999 0.75 effective seed 1062.6173 mm2.
C1000 preferred 900 mm2 seed target exceeded.
C1001 CFD remains OPEN.
C1002 exact harness sweep remains OPEN.

Status:
**LOWER_INLET_REV_AD_EXECUTED_PASS / 12X_3X40_R1P5 / 4MM_WEB / 1416P823MM2_REAL_GROSS / 1062P617MM2_EFFECTIVE_SEED / FULL_SHELL_NEXT / C01_TO_C1002**.
