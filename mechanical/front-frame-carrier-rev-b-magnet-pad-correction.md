# AudioPicture V2.2 Rev.B — front carrier magnet-pad correction

Status: **REV_B_PERIMETER_MAGNET_STATIONS_DEFINED / DML_FACING_PAD_INTRUSION_REMOVED_BY_DIRECTIONAL_GEOMETRY / REAL_CAD_KERNEL_REGEN_REQUIRED**

## 1. Purpose
Correct the Rev.A front-carrier magnetic station geometry after the integrated DMU identified overlap between 12 mm circular pads and the DML projected perimeter.

No DML notch is introduced.

## 2. Fixed product geometry
Product:
320 x 400 mm.

DML projection:
X=10..310
Y=10..390.

Front carrier nominal outer boundary:
X=0.8..319.2
Y=0.8..399.2.

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

## 4. Important geometric consequence
The 6.6 mm magnet pocket itself has radius 3.3 mm.

At top center Y388, a symmetric pocket extends to Y384.7, inside the DML projected Y<=390 region.

Likewise:
- bottom Y12 pocket extends to Y15.3;
- left X12 pocket extends to X15.3;
- right X308 pocket extends to X304.7.

Therefore simply moving centers by 2 mm does NOT make the complete magnet pocket disjoint from the DML XY projection.

The previous proposed center shift alone is insufficient.

## 5. Correct interpretation of DML keep-out
A strict full-height XY projection of the DML cannot coexist with a 6.6 mm magnet pocket located in the 10 mm product perimeter if both are treated as full-depth rigid columns.

The design must use Z separation at the perimeter interface.

The DML occupies:
Z=3.3..9.3 nominal.

Magnetic pocket/carrier hardware can occupy a front/perimeter Z region only if it does not violate the required fabric/DML clearance and does not contact the DML.

Thus collision checking is 3D, not pure XY.

## 6. Rev.B magnetic station architecture
Use a perimeter-biased D-shaped reinforcement pad around each pocket.

The pocket center remains near the perimeter.

Pad reinforcement grows away from DML:
- top stations: reinforcement grows +Y;
- bottom: -Y;
- left: -X;
- right: +X.

DML-facing reinforcement is minimized.

The magnet pocket itself remains circular.

## 7. Pad seed geometry
Pocket:
- diameter 6.6 mm.

Outer reinforcement envelope:
- tangential width 12 mm;
- outward radial depth 7 mm;
- inward radial material from pocket tangent only 1.2..1.8 mm where structurally needed.

Use filleted D-shape, not a sharp rectangular tab.

## 8. Z placement rule
The magnet pocket and pad are not allowed to extend rearward through the DML thickness in an overlapping XY region.

Global rear face of magnetic station shall remain:
**Z <= 3.0 mm seed**

while DML front is:
Z=3.3 mm nominal.

Nominal separation:
>=0.3 mm at overlapping XY projection.

This is a packaging seed only.

Because the product requires >=2.0 mm fabric-to-DML clearance in the active acoustic region, this local perimeter magnetic geometry must remain outside the active fabric-DML gap definition and be treated as perimeter hardware.

## 9. DML edge clearance
The DML edge is not an acoustically active infinite plane beyond its physical boundary.

At the perimeter, carrier/magnet features may overlap the DML projected rectangle only if:
- they are entirely in front of the DML front plane;
- no mechanical contact occurs under tolerance/warp;
- they do not clamp or preload the compliant DML perimeter;
- fabric acoustic gap over active DML remains compliant.

## 10. Hard tolerance requirement
Nominal 0.3 mm Z separation is NOT sufficient for production release.

Production target:
**>=0.8 mm worst-case mechanical separation** between magnetic hardware and DML/front mount system.

Therefore one or more must change before production:
- thinner magnet/pocket front stack;
- move magnet center further outward;
- reduce pocket diameter/magnet size;
- locally move the DML hard boundary only if the panel physical edge/mount architecture permits without changing active panel;
- move magnetic circuit to a different perimeter interface.

## 11. Candidate A packaging implication
S-06-02-N:
6 x 2 mm.

With a mechanical pocket/capture, a <=3.0 mm total front-side station is plausible geometrically, but the 0.8 mm worst-case separation target must be demonstrated.

Candidate B lower-profile D41:
6.35 x 1.59 mm
may provide additional Z tolerance margin despite slightly larger diameter.

Thus Candidate B becomes more attractive mechanically if force tuning remains acceptable.

## 12. Preferred Rev.B optimization
Do not modify DML.

Perform magnet optimization in this order:
1. retain 8 stations;
2. D-shaped outward reinforcement;
3. minimize capture-stack thickness;
4. compare 2.0 mm vs 1.59 mm magnet thickness;
5. move center outward within carrier edge;
6. if necessary reduce magnet diameter class;
7. only then reconsider station count.

## 13. Revised center sweep
For each station, sweep outward offset:
- current: 12 mm / 308 mm or 388/12;
- +1 mm outward;
- +2 mm outward.

Maximum legal center is constrained by:
- carrier outer boundary;
- pocket wall thickness;
- fabric wrap radius.

The CAD solver chooses the furthest outward position that preserves >=1.2 mm outer pocket wall seed.

## 14. Carrier outer-edge constraint
Carrier boundary begins 0.8 mm from product edge.

For a 6.6 mm pocket:
minimum center distance from carrier outer edge with 1.2 mm wall:
3.3 + 1.2 = 4.5 mm.

Therefore center can theoretically approach product coordinate:
~5.3 mm from an outer product edge.

This provides more outward room than current 12 mm seeds.

## 15. Improved station seed
Adopt next-kernel candidate centers at approximately 7 mm from product edge:

Top:
- M1C=(70,393)
- M2C=(250,393)

Bottom:
- M3C=(70,7)
- M4C=(250,7)

Left:
- M5C=(7,135)
- M6C=(7,275)

Right:
- M7C=(313,135)
- M8C=(313,315).

At these centers a 6.6 mm pocket remains inside the nominal carrier outer boundary with approximately 2.9 mm material from pocket edge to product edge and ~2.1 mm to carrier outer boundary, before detailed wrap geometry.

## 16. XY relationship at MxC
Top pocket inner edge:
Y=389.7 mm, only ~0.3 mm into DML projection.

Bottom:
Y=10.3 mm, ~0.3 mm into DML projection.

Left:
X=10.3 mm.

Right:
X=309.7 mm.

Thus MxC nearly eliminates projected overlap even before Z separation.

This is substantially better than MxB.

## 17. Production direction
Promote MxC as the next real-CAD seed.

Do not freeze MxB.

Use D-shaped outward pads plus MxC.

The residual ~0.3 mm projected overlap of the pocket envelope is handled by:
- exact carrier boundary;
- pocket/capture shape;
- 3D Z separation;
- tolerance optimization.

## 18. Peel impact
M3C/M4C remain far from lower-center peel recess X160.

Their more outward Y position improves progressive peel lever arm.

No negative peel consequence identified.

## 19. RF impact
Moving magnets closer to the external perimeter is generally preferable for keeping metal away from central RF/sensing zones, but exact radar/ESP32 masks remain authoritative.

No RF performance claim is made without simulation/test.

## 20. Automatic checks
C431 Rev.B circular 12 mm pad overlap recognized.
C432 2 mm center shift alone rejected as insufficient.
C433 collision logic upgraded from XY-only to 3D.
C434 DML is not notched baseline.
C435 D-shaped reinforcement grows outward.
C436 circular magnet pocket retained.
C437 station rear face seed <=Z3.0.
C438 DML front remains Z3.3.
C439 nominal station/DML Z separation positive.
C440 production worst-case separation target >=0.8 mm.
C441 Candidate B lower-profile option retained.
C442 outward-offset sweep defined.
C443 carrier outer-wall requirement >=1.2 mm seed.
C444 MxC center set defined.
C445 MxC projected overlap reduced to ~0.3 mm class.
C446 lower peel recess remains clear.
C447 exact RF masks remain gate.
C448 no DML preload from magnetic station.
C449 real CAD kernel regeneration required.
C450 final station selection requires tolerance and magnetic-force validation.

## 21. State
The integrated correction rejects the simplistic MxB shift as insufficient.

Next real-CAD seed:
M1C=(70,393)
M2C=(250,393)
M3C=(70,7)
M4C=(250,7)
M5C=(7,135)
M6C=(7,275)
M7C=(313,135)
M8C=(313,315).

Architecture:
- circular 6.6 mm pocket;
- outward D-shaped reinforcement;
- front/perimeter Z-separated magnetic hardware;
- no DML notch.

Status:
**MAGNET_STATIONS_MOVED_TO_7MM_EDGE_CLASS / D_SHAPED_OUTWARD_PAD / DML_PROJECTED_OVERLAP_REDUCED_TO_0P3MM_CLASS / C01_TO_C450 / REAL_CAD_REGEN_NEXT**.
