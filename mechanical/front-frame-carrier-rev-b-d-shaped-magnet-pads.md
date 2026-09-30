# AudioPicture V2.2 Rev.B — front carrier with perimeter-clipped magnetic pads

Status: **REV_B_MAGNET_PAD_GEOMETRY_DEFINED / DML_PROJECTED_OVERLAP_REMOVED_BY_CONSTRUCTION / REAL_KERNEL_REGENERATION_GATE**

## 1. Purpose
Resolve the Rev.A magnetic-pad overlap discovered by the integrated master DMU.

The DML active structural projection is not modified.

## 2. Authoritative product geometry
Product:
320 x 400 mm.

Front carrier outer boundary:
318.4 x 398.4 mm nominal.

DML projection:
X=10..310 mm
Y=10..390 mm.

A magnetic pad shall not intrude into the DML hard projected region.

## 3. Rev.B magnetic centers
M1B=(70,388)
M2B=(250,388)
M3B=(70,12)
M4B=(250,12)
M5B=(12,135)
M6B=(12,275)
M7B=(308,135)
M8B=(308,315).

These are nominal seed centers.

## 4. Important geometric consequence
A centered circular pad cannot remain fully outside the DML rectangle at these center locations.

Therefore Rev.B does not use full circular 12 mm pads.

Each station uses a perimeter-biased clipped pad.

The magnet pocket may remain circular, but the surrounding reinforcement body is clipped on its DML-facing side.

## 5. Legal perimeter bands
Top magnetic reinforcement:
Y >= 390 mm.

Bottom:
Y <= 10 mm.

Left:
X <= 10 mm.

Right:
X >= 310 mm.

Because the carrier itself has finite outer limits, these bands are narrow.

This proves that a conventional 12 mm reinforcement boss cannot be placed entirely in the front projected plane without either:
- overlapping DML projection;
- using a rearward/perimeter structural capture;
- or reducing the front-plane reinforcement width.

## 6. Rev.B architecture
Use a two-level magnetic station:

LEVEL 1 — front carrier pocket:
- compact pocket/capture feature centered near Rev.B coordinates;
- minimal front-plane material.

LEVEL 2 — perimeter return/capture:
- reinforcement extends toward product perimeter and/or rearward;
- does not occupy DML hard-clearance volume.

Thus the station is D-shaped in front projection and can gain structural section in Z/perimeter direction instead of toward the DML.

## 7. DML-facing clipping
For each pad create the nominal reinforcement primitive, then Boolean clip by the legal half-plane:

TOP:
keep Y>=390.

BOTTOM:
keep Y<=10.

LEFT:
keep X<=10.

RIGHT:
keep X>=310.

Add only legal connecting neck geometry outside the DML hard projection.

No Boolean subtraction from DML.

## 8. Pocket feasibility warning
A 6.6 mm magnet pocket centered at Y388 or Y12 / X12 or X308 itself crosses the DML projected boundary if interpreted as a hard rearward cylinder.

Therefore the magnet center also needs an outward shift for a strict no-overlap full-depth rule.

Minimum theoretical center for radius 3.3 mm:
TOP Y >=393.3
BOTTOM Y <=6.7
LEFT X <=6.7
RIGHT X >=313.3.

These positions conflict with the nominal carrier outer boundary if a full circular pocket must remain inside a flat 318.4 x 398.4 front ring.

## 9. Resulting design decision
The correct solution is not merely a D-shaped 12 mm boss.

Rev.B magnetic retention shall use:
**edge-loaded magnet cartridges / perimeter-return pockets**

The magnet cylinder is oriented/located in a perimeter return geometry such that its hard volume does not occupy the DML front/rear projected clearance.

This is a correction to the earlier simple flat-pocket concept.

## 10. Cartridge concept
Each magnetic station is a small ASA edge cartridge integrated with the carrier perimeter.

Functions:
- mechanically capture 6 x 2 mm magnet candidate;
- move magnetic hard volume outward from DML;
- provide local stiffness;
- preserve fabric wrap radius;
- remain replaceable parametrically.

Cartridge may use a local rearward flange only in product-perimeter volume proven free by DMU.

## 11. Preferred station coordinates for cartridge datum
Keep Rev.B XY station labels as interface datums:
M1B..M8B.

The actual magnet center is derived from each datum by an outward offset.

Seed outward offset:
**4.0 mm**

Derived magnet-center seeds:
Top:
M1C=(70,392)
M2C=(250,392)

Bottom:
M3C=(70,8)
M4C=(250,8)

Left:
M5C=(8,135)
M6C=(8,275)

Right:
M7C=(312,135)
M8C=(312,315).

These still require exact carrier-edge packaging but materially reduce DML overlap.

## 12. Strict no-overlap target
For a 6.6 mm pocket diameter, preferred strict centers:
Top Y>=393.5 design target
Bottom Y<=6.5
Left X<=6.5
Right X>=313.5.

Because product edges are at 0/320/0/400, a 6.6 mm pocket can physically fit in the product perimeter strip if its center is approximately:
- 3.5..6.5 mm from left/bottom;
- 313.5..316.5 mm from right;
- 393.5..396.5 mm from top.

Therefore a valid flat/perimeter solution exists inside the product envelope, but it requires moving centers farther outward than Rev.B initial seeds.

## 13. Rev.C-ready exact center proposal
Adopt as next real-kernel seed:

Top:
M1C=(70,395)
M2C=(250,395)

Bottom:
M3C=(70,5)
M4C=(250,5)

Left:
M5C=(5,135)
M6C=(5,275)

Right:
M7C=(315,135)
M8C=(315,315).

For radius 3.3 mm:
- top inner edge=391.7 >390
- bottom inner/top edge=8.3 <10
- left inner/right edge=8.3 <10
- right inner/left edge=311.7 >310.

Therefore the circular 6.6 mm magnet pocket itself is outside the DML projected rectangle with >=1.7 mm projected margin.

## 14. Carrier-edge feasibility
Carrier nominal edge:
0.8..319.2 / 0.8..399.2.

At center X=5 with radius3.3:
outer edge=1.7 >0.8.

At X=315:
outer edge=318.3 <319.2.

At Y=5:
outer edge=1.7 >0.8.

At Y=395:
outer edge=398.3 <399.2.

Thus the full 6.6 mm circular pocket fits inside the nominal carrier projected boundary.

This is the key geometric closure.

## 15. Reinforcement pad
Use a D-shaped/asymmetric pad around the legal pocket.

Seed maximum outward extent:
to carrier edge minus >=0.8 mm structural skin as applicable.

DML-facing reinforcement edge:
- top >=390.5
- bottom <=9.5
- left <=9.5
- right >=310.5.

Pocket itself remains fully outside DML projection.

## 16. Fabric bonding land interaction
Magnetic cartridges consume part of the 6 mm rear bonding land locally.

At each station:
- reroute bonding land around cartridge;
- preserve >=3 mm local adhesive path on both sides;
- restore nominal >=5 mm land away from station.

No magnet is bonded through fabric.

## 17. Retention force implication
Moving magnet outward does not change the 20..30 N total assembled target.

Steel targets must follow the new perimeter locations.

RF masks remain authoritative and may require tangential movement along the perimeter.

## 18. Revised real-kernel requirements
Next kernel model shall use M1C..M8C, not M1B..M8B.

Generate:
- one connected carrier solid;
- eight full 6.6 mm pockets;
- asymmetric reinforcement pads;
- lower peel recess;
- no pocket/DML projected intersection.

Measure:
- volume;
- mass;
- bbox;
- minimum projected DML clearance;
- minimum carrier-edge skin.

## 19. Automatic checks
C431 Rev.A magnet-pad collision formally retired.
C432 DML projection remains unchanged.
C433 simple 12 mm circular pad architecture rejected.
C434 6.6 mm pocket radius included in placement solve.
C435 M1C/M2C top pocket inner edge >390.
C436 M3C/M4C bottom pocket inner edge <10.
C437 M5C/M6C left pocket inner edge <10.
C438 M7C/M8C right pocket inner edge >310.
C439 all 6.6 mm pockets remain inside carrier projected boundary.
C440 minimum projected pocket-to-DML margin >=1.7 mm nominal.
C441 reinforcement is asymmetric/D-shaped.
C442 DML-facing reinforcement remains outside hard projection.
C443 no DML notch introduced.
C444 bonding land reroutes around cartridges.
C445 retention-force target unchanged.
C446 steel targets move with cartridges.
C447 RF masks may shift station tangentially.
C448 real kernel regeneration uses M1C..M8C.
C449 real kernel must report one-solid connectivity.
C450 real kernel must report exact DML projected clearance.

## 20. State
The DMU warning is resolved analytically by moving the magnet centers to a strict legal perimeter strip.

Next kernel centers:
M1C (70,395)
M2C (250,395)
M3C (70,5)
M4C (250,5)
M5C (5,135)
M6C (5,275)
M7C (315,135)
M8C (315,315).

A 6.6 mm circular pocket at these locations fits inside the nominal carrier and stays outside the 300 x 380 mm DML projection with at least 1.7 mm nominal projected margin.

Status:
**MAGNET_POCKET_DML_OVERLAP_ANALYTICALLY_CLOSED / M1C_TO_M8C_DEFINED / C01_TO_C450 / REAL_BREP_REGENERATION_NEXT**.
