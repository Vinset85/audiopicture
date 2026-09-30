# AudioPicture V2.2 — shell fastener architecture trade study Rev.AV

Status: **M3_PC_CF_THREAD_ARCHITECTURE_PREFERRED / ASA_UNTHREADED / EXACT_INSERT_MPN_AND_COUPON_GATE_OPEN**

## Functional requirement
The rear ASA shell must be removable repeatedly without relying on threads cut directly into ASA.

The six-node geometry is already frozen at packaging level.

## Architecture comparison
A. Threaded insert in ASA shell:
rejected as baseline.
It makes the cosmetic/service shell carry the durable thread and complicates replacement.

B. Direct screw thread in printed PC-CF:
not preferred for repeated service until cyclic thread-wear testing exists.

C. Metal threaded insert in PC-CF + clearance hole through ASA:
preferred architecture.

Benefits:
- durable thread remains on structural frame;
- ASA shell is a replaceable clamped part;
- service cycles do not wear an ASA thread;
- clamp stack can be controlled independently.

## Thread-size screen
Preferred nominal thread class:
M3.

Reason:
the current ASA seat is diameter 10 mm.
An M3 insert family can fit with materially more surrounding land than an M4-class insert.

Manufacturer dimensional screening:
Böllhoff AMTEC/HITSERT documentation lists an M3 example with length 5.3 mm and installation/body diameter around 5.8/5.9 mm; the corresponding M4 example is around 8.5/8.6 mm diameter and 7.5 mm long.

These catalogue dimensions are screening evidence only. They do not freeze the final insert MPN or prove performance in printed PC-CF.

## Proposed stack architecture
From rear/outside toward front:
1. removable screw head on rear-shell side;
2. ASA shell wall/local seat, clearance hole only;
3. controlled local spacer/compression-limiter function across the shell-to-frame gap;
4. metal M3 female thread anchored in PC-CF frame/tab.

The screw must clamp through a controlled hard stack rather than crushing ASA to close an uncontrolled gap.

## Current geometric implication
Current seat front:
Z36.0.

Coarse PC-CF rear:
Z35.0.

Nominal geometric separation:
1.0 mm.

Therefore the next CAD gate should introduce a local hard spacer/stand-off concept of approximately the current 1.0 mm nominal gap, but its production height cannot be released before tolerance/process stack analysis.

## Open qualification
Before insert release:
- exact insert MPN;
- exact recommended hole diameter;
- insertion method compatible with printed PC-CF;
- coupon pull-out;
- coupon torque-out;
- repeated assembly cycle test;
- local tab/frame load check;
- screw-head/washer geometry;
- clamp-load target;
- vibration loosening strategy.

## Checks
C1151 repeated-service thread shall not be cut directly in ASA.
C1152 ASA-shell threaded-insert baseline rejected.
C1153 direct repeated-service PC-CF printed thread not preferred without cycle data.
C1154 metal insert in PC-CF preferred.
C1155 ASA uses clearance hole only.
C1156 M3 selected as preferred thread-size class for next CAD gate.
C1157 M4 not selected at current D10 seat due packaging margin.
C1158 catalogue insert dimensions treated as screening only.
C1159 exact insert MPN remains open.
C1160 current local shell/frame nominal gap 1.0 mm.
C1161 controlled hard spacer/compression-limiter required.
C1162 spacer release height requires tolerance/process analysis.
C1163 PC-CF insert coupon pull-out required.
C1164 PC-CF insert coupon torque-out required.
C1165 repeated assembly-cycle test required.
C1166 local structural verification remains required.

Status:
**FASTENER_REV_AV / M3_METAL_THREAD_IN_PC_CF / ASA_CLEARANCE_ONLY / CONTROLLED_HARD_STACK_REQUIRED / INSERT_MPN_OPEN / C01_TO_C1166**.
