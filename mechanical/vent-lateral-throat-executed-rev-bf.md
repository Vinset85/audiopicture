# AudioPicture V2.2 — executed lateral throat gate Rev.BF

Status: **CURRENT_VENT_LAYOUT_NOT_PROMOTED_FOR_LABYRINTH / FULL_SHADOWING_ON_10_SLOTS / VENT_RELOCATION_PREFERRED_OVER_FRAME_RELIEF**

## Executed Rev.BE result
Rev.BE was executed locally against the documented Rev.C PC-CF projection using a 0.25 mm raster geometric screen.

This is not CFD.

### Fully projected-shadowed slots
100 percent shadow in the screen:
- UL1
- UL2
- UL4
- UR1
- UR2
- UR4
- IL1
- IL3
- IL5
- IR1
- IR3
- IR5

Count: 12 slots.

For these slots the slot footprint is entirely over projected PC-CF structure.

Maximum cardinal lateral travel to first free projected region is approximately 5 mm for the regular outer-ring cases in this screen.

### Partial-shadow examples
Upper:
- UL3 ~33 percent shadow;
- UR3 ~33 percent;
- UR5 ~33 percent.

Lower:
- IL2 / IR2 ~46 percent in the coarse projection;
- IL4 / IL6 / IR4 / IR6 ~33 percent.

UL5 is unshadowed in the current coarse projection.

## Important interpretation
The zero escape-edge proxy reported for a fully covered slot does NOT mean zero physical airflow.

It means there is no direct slot-edge-to-free-projection throat in the 2D screen. Flow would have to travel under the projected frame through the approximately 2.8 mm nominal Z gap before reaching a free region.

That path adds a strong turn/restriction before any intentional acoustic labyrinth is added.

Therefore the current vent layout is not promoted as the labyrinth baseline.

## Design decision
Preferred next action:
**relocate vent slots into projected-free regions while preserving the PC-CF structural ring.**

Do not cut reliefs into the structural ring at this stage.

Reason:
- the ring is part of the primary load path;
- vent positions are easier to change than structural topology;
- several slots can likely move inward while retaining distributed inlet/outlet architecture.

## Next solver gate
Search new lower and upper slot coordinates with:
- real R1.5 capsule geometry;
- >=4 mm web target;
- shell edge constraints;
- existing cleat/MAIN-C/ESP32/service/ENV/exciter keep-outs;
- projected PC-CF solid as a hard exclusion or explicit clearance mask;
- symmetry where practical;
- preserve inlet/outlet real gross-area targets;
- retain hidden rear-facing architecture.

Only after a low-shadow or zero-shadow layout is found should the two-turn baffle/labyrinth be generated.

## Checks
C1237 Rev.BE geometric throat audit executed locally.
C1238 raster step 0.25 mm.
C1239 projected PC-CF Rev.C ring included.
C1240 12 slots found fully projected-shadowed.
C1241 partially shadowed slots identified.
C1242 zero escape-edge proxy not interpreted as zero physical airflow.
C1243 approximately 2.8 mm nominal Z bypass path acknowledged.
C1244 added labyrinth on current layout rejected.
C1245 structural ring relief not preferred.
C1246 vent relocation preferred.
C1247 next solver shall treat projected PC-CF as exclusion/clearance.
C1248 real capsule geometry retained.
C1249 >=4 mm web target retained.
C1250 area targets retained.
C1251 CFD still required after revised geometry.

Status:
**VENT_THROAT_REV_BF / 12_FULL_SHADOW_SLOTS / CURRENT_LAYOUT_REJECTED_FOR_BAFFLE_FREEZE / RELOCATION_SOLVER_NEXT / C01_TO_C1251**.
