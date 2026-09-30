# AudioPicture V2.2 Rev.B — front carrier with perimeter-biased D-shaped magnet stations

Status: **REV_B_MAGNET_PAD_GEOMETRY_DEFINED / DML_OVERLAP_REMOVED_BY_CONSTRUCTION / REAL_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Correct the Rev.A front-carrier magnetic-station conflict discovered by the integrated master DMU.

Rev.A issue:
12 mm circular station pads centered approximately 4 mm from the DML projected edge intruded into the DML projected region.

Rev.B solution:
- move station centers toward the product perimeter;
- replace circular local pads with perimeter-biased D-shaped pads;
- define a hard DML-facing clipping plane for every station;
- do not notch the DML.

## 2. Authoritative DML projected hard region
Nominal DML projection:
X=10..310 mm
Y=10..390 mm.

For front magnetic hardware, define additional seed lateral clearance:
**0.5 mm**

Therefore magnet-pad hard exclusion starts at:
X=9.5..310.5
Y=9.5..390.5
where applicable to the DML-facing side.

The exact final clearance may increase after tolerance analysis.

## 3. Rev.B magnet centers
Top:
M1B=(70,388)
M2B=(250,388)

Bottom:
M3B=(70,12)
M4B=(250,12)

Left:
M5B=(12,135)
M6B=(12,275)

Right:
M7B=(308,135)
M8B=(308,315).

## 4. Magnet pocket
Packaging reference remains:
supermagnete S-06-02-N class
6 x 2 mm.

Pocket seed:
diameter 6.6 mm.

The pocket itself must remain legal relative to the DML.

Because the magnet radius is ~3 mm class, a center only 2 mm from the nominal DML edge requires the magnet pocket to be shifted/perimeter-biased or the station center moved further outward.

Therefore Rev.B distinguishes:
- nominal magnetic-station anchor coordinate;
- actual pocket center after DML legality solve.

## 5. Important geometry consequence
For a 6.6 mm pocket and 0.5 mm lateral clearance from the DML projection, minimum pocket-center offset from DML edge is:

3.3 + 0.5 = **3.8 mm**.

Thus the proposed centers at 2 mm outside/inside the nominal DML edge are insufficient for an unmodified circular 6.6 mm pocket.

This is a second-order issue revealed by exact dimensional reasoning.

## 6. Revised legal pocket-center coordinates
Use minimum 4.0 mm center offset from DML edge.

Top DML edge Y390:
pocket centers must be >=394.0 mm if outside above DML.

Bottom edge Y10:
pocket centers must be <=6.0 mm if outside below DML.

Left edge X10:
pocket centers must be <=6.0 mm.

Right edge X310:
pocket centers must be >=314.0 mm.

These positions are still inside the 320 x 400 product envelope for the magnet pocket itself:
- top pocket outer edge <=397.3
- bottom >=2.7
- left >=2.7
- right <=317.3.

Therefore the 6 x 2 mm magnet architecture remains feasible without DML overlap.

## 7. Rev.B final pocket centers
Freeze as CAD seeds:

Top:
MB1=(70,394)
MB2=(250,394)

Bottom:
MB3=(70,6)
MB4=(250,6)

Left:
MB5=(6,135)
MB6=(6,275)

Right:
MB7=(314,135)
MB8=(314,315).

These replace the intermediate MxB anchor coordinates for actual magnet pocket placement.

## 8. D-shaped structural pads
The structural pad around each pocket is not circular.

Pad construction:
1. create local rounded pad around pocket;
2. extend material toward product perimeter;
3. clip DML-facing edge to the legal clearance plane;
4. union to perimeter carrier ring.

Nominal local pad width along perimeter:
12..16 mm.

Nominal inward extent:
limited by DML clearance plane.

Pad thickness:
3.2 mm local first seed.

## 9. Top pad clipping
Top pads:
- magnet centers Y394;
- DML-facing pad boundary must remain >=Y390.5;
- pad extends preferentially toward Y399.2 carrier outer boundary.

## 10. Bottom pad clipping
Bottom:
- center Y6;
- DML-facing pad boundary <=Y9.5;
- pad extends toward Y0.8.

## 11. Left pad clipping
Left:
- center X6;
- DML-facing pad boundary <=X9.5;
- pad extends toward X0.8.

## 12. Right pad clipping
Right:
- center X314;
- DML-facing pad boundary >=X310.5;
- pad extends toward X319.2.

## 13. Pocket-to-product-edge margin
With center 6 mm and radius 3.3 mm:
nearest nominal pocket edge:
2.7 mm from product datum edge.

With carrier outer edge at 0.8 mm:
polymer edge margin:
~1.9 mm before pocket.

This is tight but feasible as a packaging seed.

Mechanical strength and print-process qualification are required.

## 14. Optional fallback
If 1.9 mm local edge ligament is insufficient:
Option F1:
use Candidate B lower-profile/similar-diameter magnet but does not materially solve XY ligament.

Option F2:
reduce magnet diameter to 5 mm class after force analysis.

Option F3:
increase local front carrier edge width inward only where DML clearance allows.

Option F4:
move magnetic circuit to rear/perimeter sidewall architecture.

Preferred fallback:
**5 mm magnet class**, not DML modification.

## 15. Lower peel recess
Peel recess remains centered X160.

Bottom magnets at X70 and X250.

Horizontal separation remains 90 mm from peel center to each station.

No conflict.

## 16. Magnetic force consequence
Moving pocket centers does not change the 20..30 N total assembled-force requirement.

Exact force must be revalidated because:
- target support geometry changes;
- local polymer thickness/gap may change;
- D-shaped pads may alter target recess packaging.

## 17. Target placement
Product-side steel targets follow MB1..MB8 only if:
- structural support exists;
- radar/ESP32 RF masks permit;
- target does not enter DML compliant mount.

Discrete target geometry remains mandatory.

## 18. RF masks
MB7/MB8 on right edge receive special scrutiny for:
- radar;
- ESP32 antenna.

If exact RF mask rejects them, move along the right perimeter in Y while preserving:
X>=314 mm for 6.6 mm pocket legality.

## 19. Kernel regeneration contract
Generate:
**AP22_FRONT_CARRIER_REV_B_DMU.step**

Required:
- one valid B-rep;
- all eight pockets;
- D-shaped pads unioned to ring;
- peel recess;
- no DML hard-region intersection.

## 20. Boolean collision test
Construct DML hard volume:
X=9.5..310.5
Y=9.5..390.5
over the front-carrier local Z overlap range.

Intersect:
DML_HARD x MAGNET_PAD_AND_POCKET_SOLIDS.

Required intersection volume:
**0 mm3**.

Carrier perimeter itself is treated separately because the DML mount/front perimeter architecture intentionally coexists near the projected boundary; the zero-intersection requirement applies to magnet hardware/local pad intrusion beyond the defined legal interface.

## 21. Edge-strength gate
At each pocket:
minimum remaining edge ligament seed:
>=1.8 mm.

Preferred:
>=2.0 mm.

If real kernel yields <1.8 mm:
6 mm magnet layout is rejected or locally redesigned.

## 22. Automatic checks
C431 Rev.A circular magnet-pad architecture retired.
C432 DML magnetic hard clearance =0.5 mm seed.
C433 minimum 6.6 mm pocket-center offset from DML edge >=3.8 mm.
C434 intermediate 2 mm-offset station centers rejected for pocket placement.
C435 MB1=(70,394).
C436 MB2=(250,394).
C437 MB3=(70,6).
C438 MB4=(250,6).
C439 MB5=(6,135).
C440 MB6=(6,275).
C441 MB7=(314,135).
C442 MB8=(314,315).
C443 all pocket circles remain inside product envelope.
C444 D-shaped pad extends toward perimeter.
C445 DML-facing pad edge clipped to legal plane.
C446 DML notch prohibited baseline.
C447 lower peel recess remains clear.
C448 total magnetic force target unchanged.
C449 right-side RF masks remain authoritative.
C450 kernel regeneration requires one valid solid.
C451 magnet hardware vs DML hard-volume intersection =0.
C452 minimum edge ligament >=1.8 mm.
C453 preferred edge ligament >=2.0 mm.
C454 5 mm magnet class is preferred fallback if ligament fails.
C455 exact target support/RF legality remains open.

## 23. State
Rev.B actual magnet pocket centers:
- top Y394
- bottom Y6
- left X6
- right X314.

This provides 4 mm center offset from the DML nominal edge and supports a 6.6 mm pocket with 0.5 mm DML lateral clearance.

Expected product-edge ligament is only ~1.9 mm and therefore becomes the next real CAD strength/manufacturing gate.

Status:
**MAGNET_POCKET_XY_LEGALIZED_AGAINST_DML / MB_COORDINATES_FROZEN / 1P9MM_EDGE_LIGAMENT_SEED / C01_TO_C455 / REAL_KERNEL_REGENERATION_NEXT**.
