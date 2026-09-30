# AudioPicture V2.2 — frame-aware relocated vent candidate Rev.BJ

Status: **FRAME_AWARE_CANDIDATE_FOUND / LOWER_DISTRIBUTED_PASS / UPPER_LATERAL_STACK_PASS / FULL_MASTER_BOOLEAN_NEXT**

## Executed search result
Rev.BH execution:
- lower distributed candidate: PASS against coarse Rev.C projected frame with 1 mm clearance seed;
- lower minimum pairwise web: 4 mm;
- upper Rev.BH seed: FAIL.

The upper seed was therefore not promoted.

## Revised upper candidate
A separate search including:
- projected Rev.C PC-CF;
- 1 mm frame-clearance seed;
- MAIN-C;
- coarse ESP32 mask;
- 2 mm electronics/RF screen margin

found a clean lateral corridor.

Left upper bank:
- H X17..62 Y315..318
- H X17..62 Y322..325
- H X17..62 Y329..332
- H X17..62 Y336..339
- H X17..62 Y343..346

Right upper bank:
mirror about X160:
- H X258..303 at the same five Y levels.

Web between stacked slots:
4 mm.

## Lower candidate
Left:
- V X17..20 Y14..54
- V X24..27 Y14..54
- V X17..20 Y62..102
- V X24..27 Y62..102
- V X17..20 Y110..150
- V X24..27 Y110..150

Right:
mirror about X160.

## Areas
Real R1.5 capsule areas are unchanged from prior geometry:
- inlet gross 1416.823 mm2;
- outlet gross 1330.686 mm2.

Reduced-order proxy values remain:
- inlet x0.75 = 1062.617 mm2;
- outlet x0.80 = 1064.549 mm2.

These factors are not CFD results.

## Why this candidate is better
Unlike Rev.AD/Rev.V, the candidate is intentionally placed away from the projected PC-CF structural ring.

Therefore the earlier frame-shadow throat penalty is removed at the coarse geometry level instead of being accepted and compensated with a labyrinth.

## Release boundary
Rev.BI/BJ does not yet replace the master shell.

Next:
- build full ASA shell B-rep with all 22 relocated real capsules;
- integrate segmented edge returns and six retention seats;
- verify one solid;
- verify vent areas;
- verify no vent/seat/return conflict;
- verify envelope Z<=40;
- rerun projected-frame audit;
- then design labyrinth.

## Checks
C1252 Rev.BH lower candidate executed PASS.
C1253 Rev.BH upper candidate executed FAIL.
C1254 failed upper seed not promoted.
C1255 revised upper lateral corridor found.
C1256 upper uses 5 horizontal slots per side.
C1257 upper web 4 mm.
C1258 upper candidate clears projected PC-CF at 1 mm seed.
C1259 upper candidate clears MAIN-C in current screen.
C1260 upper candidate clears coarse ESP32 mask at 2 mm screen.
C1261 lower remains six slots per side.
C1262 lower web >=4 mm.
C1263 lower candidate clears projected PC-CF at 1 mm seed.
C1264 inlet real area unchanged 1416.823 mm2.
C1265 outlet real area unchanged 1330.686 mm2.
C1266 reduced-order factors remain proxies only.
C1267 current candidate is not yet master shell.
C1268 full B-rep integration required next.
C1269 projected-frame audit shall be rerun after integration.
C1270 labyrinth remains blocked until full master gate.

Status:
**VENT_RELOCATION_REV_BJ / ZERO_COARSE_FRAME_SHADOW_CANDIDATE / LOWER_12_PLUS_UPPER_10 / FULL_MASTER_NEXT / C01_TO_C1270**.
