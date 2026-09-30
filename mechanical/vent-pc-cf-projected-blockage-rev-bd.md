# AudioPicture V2.2 — vent / PC-CF projected blockage gate Rev.BD

Status: **PROJECTED_FRAME_SHADOWING_CONFIRMED / SLOT_AREA_NOT_EQUAL_TO_FREE_THROAT / BAFFLE_FREEZE_BLOCKED_PENDING_THROAT_MODEL**

## Purpose
Audit the already selected 22 rear-shell vents against the projected Rev.C PC-CF structural frame before adding labyrinth baffles.

This closes a previously identified unresolved risk.

## Geometry basis
Rear shell vents:
- 10 upper R1.5 capsule slots;
- 12 lower R1.5 capsule slots.

PC-CF basis:
- Rev.C closed perimeter ring X2..318 / Y2..398 with inner opening X12..308 / Y12..388;
- Rev.C cleat islands;
- documented Rev.C keep-out subtractions.

## Result interpretation
The audit confirms that multiple outer vent slots project over the PC-CF perimeter ring.

This is not a solid collision:
- PC-CF rear plane is nominally Z35;
- rear-shell inner plane is Z37.8;
- nominal separation away from local shell features is about 2.8 mm.

However, projected overlap means the slot does not discharge directly into an unobstructed cavity.

Air leaving/entering those slot regions must turn laterally through the frame-to-shell gap.

Therefore:
- nominal capsule opening area is not the local free throat area;
- the earlier 0.75 inlet / 0.80 outlet factors remain only reduced-order sizing proxies;
- baffles must not be designed as if the complete 22-slot area were unobstructed.

## Design consequence
Do not freeze the two-turn labyrinth yet.

Next calculate the minimum lateral throat available between:
1. slot opening;
2. PC-CF projected obstruction;
3. shell/frame Z gap;
4. nearest open edge of the structural ring.

The baffle cross-section must be sized against that throat.

If the throat is inadequate, choose one of:
- move affected vents inward;
- locally reshape the PC-CF ring only where structural analysis permits;
- create dedicated airflow windows/reliefs in the PC-CF architecture;
- enlarge/distribute vent geometry without violating RF/mount constraints.

Do not notch the structural ring casually.

## CFD interpretation
This audit is not CFD and does not predict mass flow, temperature or pressure drop.

It is a geometric pre-CFD gate intended to prevent an obviously restrictive labyrinth from being frozen.

## Checks
C1223 vent/frame projected-blockage audit created.
C1224 real R1.5 vent footprints used.
C1225 Rev.C perimeter-ring projection included.
C1226 Rev.C cleat projections included.
C1227 Rev.C keep-out subtractions included.
C1228 projected shadowing exists on outer vent regions.
C1229 projected shadowing is distinguished from 3D solid collision.
C1230 nominal frame-to-shell separation approximately 2.8 mm retained.
C1231 nominal vent area is not treated as unobstructed throat.
C1232 previous effective-area factors remain proxies only.
C1233 labyrinth geometry not frozen.
C1234 lateral throat model required next.
C1235 structural-ring relief forbidden without structural justification.
C1236 CFD remains required after geometry gate.

Status:
**VENT_FRAME_GATE_REV_BD / PROJECTED_SHADOWING_REAL / 2P8MM_NOMINAL_Z_GAP / LATERAL_THROAT_NEXT / LABYRINTH_NOT_FROZEN / C01_TO_C1236**.
