# AudioPicture V2.2 Rev.B — front carrier DML-clear magnetic stations

Status: **MAGNET_PAD_DML_OVERLAP_REMOVED_BY_EDGE_STATION_ARCHITECTURE / REAL_KERNEL_REGEN_REQUIRED**

## 1. Purpose
Correct the Rev.A front-carrier magnetic station geometry after the integrated DMU detected overlap between 12 mm circular pads and the DML projected perimeter.

The DML is not modified.

## 2. Authoritative product geometry
Product:
320 x 400 mm.

Front carrier projected outer boundary:
X=0.8..319.2
Y=0.8..399.2.

DML projected hard region:
X=10..310
Y=10..390.

DML hard region is treated as unavailable to rear-projecting magnetic station thickening.

## 3. Rev.B magnet centers
Top:
- M1B=(70,388)
- M2B=(250,388)

Bottom:
- M3B=(70,12)
- M4B=(250,12)

Left:
- M5B=(12,135)
- M6B=(12,275)

Right:
- M7B=(308,135)
- M8B=(308,315).

These centers remain seed coordinates.

## 4. Key geometric consequence
A centered 6 mm diameter magnet at only 2 mm from the DML boundary cannot remain completely outside the DML projected rectangle.

Therefore the previous assumption that a conventional centered rear boss could be made DML-clear merely by making the 12 mm pad D-shaped is insufficient.

This is a genuine geometry constraint.

## 5. Revised station architecture
Use an **edge-pocket / tangential capture** architecture.

The magnetic element remains near the named station, but the rearward-thickened pocket is biased toward the product perimeter.

The carrier's base 1.8 mm ring may overlap the DML projected XY perimeter because it belongs to the front perimeter stack; the prohibited feature is the local rearward thickening that would consume the DML clearance.

## 6. Pocket center offset
For each station define:
- station reference point = Rev.B seed above;
- actual magnet pocket center is offset outward from DML.

Minimum magnet center distance from DML edge for radius 3.0 mm plus 0.5 mm clearance:
**3.5 mm**.

Thus candidate actual pocket centers:

Top:
- P1=(70,393.5)
- P2=(250,393.5)

Bottom:
- P3=(70,6.5)
- P4=(250,6.5)

Left:
- P5=(6.5,135)
- P6=(6.5,275)

Right:
- P7=(313.5,135)
- P8=(313.5,315).

## 7. Carrier-edge fit
Check against carrier outer boundary.

For 6.6 mm process pocket diameter, radius=3.3 mm.

At X=6.5:
pocket edge reaches X=3.2, inside carrier Xmin=0.8.

At X=313.5:
edge reaches X=316.8, inside carrier Xmax=319.2.

At Y=6.5:
edge reaches Y=3.2, inside carrier Ymin=0.8.

At Y=393.5:
edge reaches Y=396.8, inside carrier Ymax=399.2.

Therefore all eight 6.6 mm pocket bores fit within the carrier projected boundary.

## 8. DML clearance
DML edge:
X=10/310 and Y=10/390.

Actual pocket bore closest edge:
- left/bottom maximum toward DML = 9.8
- right/top minimum toward DML = 310.2 / 390.2.

Nominal projected clearance:
**0.2 mm** for the 6.6 mm bore.

This is too small for production tolerance.

## 9. Production clearance improvement
Move actual pocket centers further outward to 6.0 / 314.0 and 6.0 / 394.0 where edge margin allows.

With 6.6 mm bore radius 3.3:
- inward edge = 9.3 or 310.7/390.7
- nominal DML projected clearance = **0.7 mm**.

Carrier outer edge margin:
- outward edge at 2.7 or 317.3/397.3
- carrier boundary margin = **1.9 mm**.

This is the preferred Rev.B seed.

## 10. Preferred actual pocket centers
Top:
- P1=(70,394)
- P2=(250,394)

Bottom:
- P3=(70,6)
- P4=(250,6)

Left:
- P5=(6,135)
- P6=(6,275)

Right:
- P7=(314,135)
- P8=(314,315).

Station reference points M1B..M8B remain useful artwork/retention map references, but P1..P8 are the actual pocket-center geometry.

## 11. Local thickening shape
Use perimeter-biased truncated pad.

Pad rearward thickening:
- surrounds 6.6 mm pocket with >=1.5 mm polymer where feasible;
- is clipped at DML hard boundary plus clearance;
- blends into 10 mm perimeter ring;
- does not form a circular 12 mm boss.

Preferred pad footprint is an obround/teardrop extending toward the product edge and tangentially along the ring.

## 12. Pocket structural margin
At the product-edge side, available material between 6.6 mm pocket and carrier outer boundary is ~1.9 mm nominal.

This is acceptable only as a CAD seed.

Print/process qualification must check:
- crack initiation;
- magnet insertion;
- capture-cap load;
- peel load.

If insufficient, use smaller/thinner magnet or tangentially enlarged pad, not DML intrusion.

## 13. Magnet candidate implication
The metric 6 x 2 mm candidate remains geometrically viable.

A larger-diameter magnet is disfavored because the edge-pocket geometry has limited radial margin.

Therefore Candidate A 6 x 2 mm becomes preferred over 6.35 mm Candidate B from a packaging standpoint.

This is not yet a production MPN freeze.

## 14. Mechanical capture
Rear-loaded pocket remains.

Because the pocket is close to product edge:
- capture cap/lip should extend tangentially along the perimeter;
- avoid thin isolated circular lip;
- use local bridge into carrier ring.

Adhesive remains secondary retention.

## 15. Magnetic target alignment
Product-side steel target must align to P1..P8, not old M reference centers.

Target shape can be elongated tangentially to tolerate X/Y assembly variation.

No continuous steel ring.

## 16. Force implication
Moving the magnet outward does not change the 20..30 N total assembled target.

However:
- local target support;
- magnetic gap;
- target size

must be re-evaluated at P1..P8.

Catalogue pull values remain non-authoritative.

## 17. Front carrier Z
Base ring:
1.8 mm.

Local magnet station:
up to 3.2 mm local CAD depth in the previous kernel diagnostic.

Rev.B local thickening is allowed only outside DML projected hard region.

Therefore its rearward intrusion no longer competes with the 2.8 mm fabric-to-DML active gap.

## 18. Locator compatibility
LOC_A / LOC_B must not share thin edge material with magnet pockets.

Minimum locator-to-pocket solid ligament seed:
>=4 mm.

If conflict occurs, move locator tangentially before moving a magnet toward DML.

## 19. Peel compatibility
Lower peel recess centered X160 remains far from P3/P4 at X70/250.

No change required.

## 20. Kernel regeneration requirements
Generate a new real B-rep:
**AP22_FRONT_CARRIER_REV_B_DMU**

Required outputs:
- solid count;
- validity;
- volume;
- mass sensitivity;
- bounding box;
- exact DML-overlap volume of local rear-thickened station features.

Acceptance:
- solid count=1;
- valid=true;
- DML-overlap volume of rear-thickened magnet features=0.

## 21. Automatic checks
C431 Rev.B station references generated.
C432 actual pocket centers separated from station references.
C433 P1/P2 Y=394.
C434 P3/P4 Y=6.
C435 P5/P6 X=6.
C436 P7/P8 X=314.
C437 6.6 mm pocket remains inside carrier boundary.
C438 nominal pocket-to-DML projected clearance >=0.7 mm.
C439 carrier outer-edge material margin >=1.9 mm nominal.
C440 no 12 mm circular rear boss baseline.
C441 local thickening clipped outside DML hard region.
C442 local pad blends tangentially into perimeter ring.
C443 6 x 2 mm magnet remains packaging-preferred.
C444 larger 6.35 mm alternative is packaging-disfavored but not prohibited.
C445 steel targets align to P1..P8.
C446 target geometry remains discrete.
C447 total magnetic retention target remains 20..30 N.
C448 locator-to-pocket ligament >=4 mm seed.
C449 peel recess remains clear.
C450 kernel regeneration must prove zero local-thickening/DML overlap.

## 22. State
The DMU warning is resolved architecturally by separating:
- magnetic station reference;
- actual magnet pocket center.

Preferred actual pockets:
P1=(70,394)
P2=(250,394)
P3=(70,6)
P4=(250,6)
P5=(6,135)
P6=(6,275)
P7=(314,135)
P8=(314,315).

Nominal 6.6 mm pocket:
- 0.7 mm projected DML clearance;
- 1.9 mm carrier-edge margin.

Status:
**EDGE_POCKET_MAGNET_ARCHITECTURE / P1_TO_P8_OUTBOARD / 0P7MM_DML_CLEARANCE_SEED / C01_TO_C450 / REAL_KERNEL_ZERO_OVERLAP_PROOF_NEXT**.
