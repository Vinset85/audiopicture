# AudioPicture V2.2 Rev.A — front-frame carrier parametric CAD

Status: **FRONT_CARRIER_DIMENSIONAL_CONTRACT_FROZEN / MAGNET_POCKETS_AND_FABRIC_LAND_DEFINED / EXACT_FABRIC_PROCESS_GATE_OPEN**

## 1. Purpose
Define the removable unfilled-ASA front carrier as a dimensioned parametric CAD part.

Functions:
- carry/tension printed acoustic fabric;
- house mechanically captured magnets;
- provide X/Y registration;
- provide hidden peel access;
- remain acoustically sparse;
- protect required fabric-to-DML clearance.

## 2. Coordinate system
Product:
320 x 400 mm.

Origin:
front lower-left.

Frontmost product plane:
Z=0.

Carrier is fully contained inside the master 320 x 400 x 40 mm envelope.

## 3. Outer carrier boundary
Nominal projected outer boundary:
- X 0.8..319.2
- Y 0.8..399.2

Nominal overall carrier size:
**318.4 x 398.4 mm**

This leaves a 0.8 mm cosmetic/perimeter allowance per side inside the product master boundary.

Final edge reveal is tuned with the artwork/front cosmetic design.

## 4. Perimeter ring
Nominal ring width:
**10 mm**

Sweep:
8 / 10 / 12 mm.

Nominal carrier structural thickness:
**1.8 mm**

Sweep:
1.6 / 1.8 / 2.2 mm.

Use local thickening only at magnetic stations and locator features.

## 5. Front edge
Outer front edge:
- radius 1.0..1.5 mm seed.

Fabric wraps continuously around the edge.

No sharp edge contacts the visible fabric.

## 6. Fabric bonding land
Rear-side continuous bonding land on perimeter:
- nominal width 6 mm;
- minimum legal width 5 mm after local features;
- lightly recessed adhesive zone 0.15..0.30 mm if process requires.

The bonding land is behind the visible face.

No adhesive enters:
- microphone acoustic windows;
- radar window;
- optical sensor window.

## 7. Fabric wrap allowance
Fabric blank extends beyond outer carrier boundary.

Seed trim allowance:
**15 mm per side**

This supports:
- tensioning fixture;
- rear wrap;
- adhesive land;
- trimming after cure.

Final blank size/process determined by selected fabric stretch.

## 8. Fabric seating plane
Define:
DATUM_FABRIC_FRONT = Z0.

The carrier front geometry supports the fabric without a broad central grille.

The fabric rear surface and DML front surface must maintain:
- nominal 2.5..3.0 mm;
- hard worst-case >=2.0 mm.

## 9. Clearance budget
Seed nominal gap:
**2.8 mm**

Preliminary tolerance allocation:
- carrier/frame seating variation: +/-0.25 mm
- fabric sag/process: 0.25 mm allowance
- DML/front assembly variation: +/-0.20 mm
- printed carrier warp local: 0.10 mm after qualified process.

Worst directional consumption seed:
0.25 + 0.25 + 0.20 + 0.10 = 0.80 mm.

2.8 - 0.8 = **2.0 mm minimum design closure**.

This is a dimensional budget, not a measured capability claim.

## 10. Magnet stations
Use the Rev.A coordinate map:
M1 (70,386)
M2 (250,386)
M3 (70,14)
M4 (250,14)
M5 (14,135)
M6 (14,275)
M7 (306,135)
M8 (306,315).

Each station is generated from the same pocket family.

## 11. Magnet pocket
Candidate-A pocket:
- nominal bore diameter 6.6 mm
- depth 2.2 mm class.

Because nominal carrier is only 1.8 mm, each magnetic station receives a local rear boss/thickening.

Local station pad:
- diameter 12 mm seed;
- total local Z thickness 3.0..3.5 mm as permitted by front/DML keep-outs.

Magnet is rear-loaded.

## 12. Mechanical magnet capture
Preferred geometry:
- rear-loaded cylindrical pocket;
- front-side closed floor;
- rear retention cap/lip.

Do not expose magnet on visible front.

Capture shall retain magnet if adhesive bond fails.

The capture feature must not create a hard protrusion into DML clearance.

## 13. Magnetic gap tuning
Do not tune assembled force by thinning the carrier globally.

Use local controlled stack:
- pocket floor;
- optional nonmagnetic shim;
- product-side target recess.

G_MAG sweep remains:
0.5 / 0.8 / 1.0 / 1.2 mm equivalent.

## 14. Registration system
Magnets are not precision X/Y locators.

Use two datum features.

LOC_A:
- lower-left-side datum;
- controls X and Y reference.

LOC_B:
- lower-right or upper-side slot datum;
- controls rotation while allowing thermal/process expansion.

Use pin/slot or tongue/slot architecture.

Seed engagement:
- 1.0..1.5 mm.

No high-force snap engagement.

## 15. Locator tolerance philosophy
LOC_A:
close datum.

LOC_B:
elongated in one axis to avoid overconstraint.

Seed running clearance:
0.20..0.35 mm after print compensation.

Exact clearance is coupon-qualified.

## 16. Peel recess
Hidden release feature:
- lower edge near center but outside M3/M4.

Seed center:
**X160 mm**

Seed projected width:
**28 mm**

Seed depth into lower edge:
**4 mm**

Edge radii:
>=2 mm.

The user reaches the underside/rear edge, not the visible front face.

## 17. Peel geometry
The recess initiates local separation near the midpoint between M3 and M4.

Distance to each lower magnet is approximately 90 mm in X, supporting progressive peel rather than simultaneous normal pull.

Peel edge must not expose DML to finger contact.

Add internal finger-stop/guard if needed.

## 18. Sparse anti-sag supports
Baseline:
no central crossbar.

If fabric sag requires support, allow narrow local ribs:
- <=2 mm projected width seed;
- rounded top;
- located only after acoustic map.

Any support in active DML region is an acoustic optimization variable, not baseline.

## 19. Microphone windows
At each microphone projected acoustic path:
- no carrier material in defined port cone;
- no adhesive land;
- fabric only baseline.

Generate four parametric circular/rounded exclusion regions from VOICE mic coordinates.

## 20. Radar window
Generate carrier material exclusion or controlled thin unfilled-polymer window around radar forward projection.

No magnet pad or locator intersects it.

Exact size follows radar EM/radome solve.

## 21. OPT3004 window
Create optical exclusion region:
- no hard rib;
- no adhesive;
- fabric optical transmission calibrated.

Do not create a visibly obvious hole unless calibration proves unavoidable.

## 22. Carrier anti-warp strategy
Use perimeter section geometry before adding central material.

Allowed:
- local rear bead outside active acoustic aperture;
- magnetic station pads;
- locator pads.

Avoid:
- full-width braces;
- large central lattice;
- conductive reinforcement.

## 23. Fabric process datums
CAD defines:
ARTWORK_ORIGIN = (160,200)
ARTWORK_X_AXIS = +X
ARTWORK_Y_AXIS = +Y.

Add hidden rear fiducials for printing/tension fixture alignment.

Visible artwork has bleed beyond final wrap line.

## 24. Assembly process seed
1. print/inspect ASA carrier;
2. install/capture magnets with polarity irrelevant to steel target architecture;
3. place carrier in fabric tension fixture;
4. align artwork to CAD fiducials;
5. tension fabric to qualified process window;
6. bond rear perimeter land;
7. cure;
8. trim rear excess;
9. inspect gap/sag/artwork alignment;
10. install front assembly on product and verify peel force.

## 25. Service behavior
Front assembly is replaced as one FRU.

Workshop re-fabric may be possible but is not required for normal end-user service.

No adhesive must be broken to remove the front assembly from the product.

## 26. Preliminary carrier mass screen
A pure 318.4 x 398.4 mm rectangular ring:
- width 10 mm;
- thickness 1.8 mm

has geometric volume approximately:
**25.1 cm3** before local pads/reliefs.

At representative unfilled ASA density around 1.05..1.10 g/cm3 sensitivity:
**26..28 g** ring-only.

Allowing magnet pads, locators and peel geometry:
carrier target remains comfortably inside prior 35..60 g carrier budget.

Final CAD mass is authoritative.

## 27. Structural checks
Front carrier is not wall-mount structure.

Qualification loads:
- magnetic normal retention;
- peel removal;
- fabric tension;
- handling twist;
- drop/service handling as appropriate;
- thermal warp.

No DML contact allowed during these checks.

## 28. Automatic checks
C341 carrier outer boundary stays inside 320 x 400.
C342 ring width sweep 8/10/12 rebuilds.
C343 thickness sweep 1.6/1.8/2.2 rebuilds.
C344 fabric bonding land >=5 mm.
C345 no adhesive land enters mic exclusions.
C346 no adhesive land enters radar exclusion.
C347 no adhesive land enters optical exclusion.
C348 nominal fabric-DML gap 2.8 mm.
C349 tolerance budget preserves >=2.0 mm gap.
C350 all eight magnet pads generated.
C351 magnet pads do not violate DML hard clearance.
C352 magnets rear-loaded and mechanically captured.
C353 LOC_A and LOC_B generated.
C354 LOC_B prevents overconstraint via slot degree of freedom.
C355 peel recess centered near X160.
C356 peel recess clears M3/M4.
C357 peel access cannot contact DML directly.
C358 no central crossbar baseline.
C359 mic port cones clear carrier.
C360 radar region remains RF-legal.
C361 optical path remains clear.
C362 artwork origin fixed at product center.
C363 fabric fixture fiducials defined.
C364 front assembly removable without breaking fabric adhesive.
C365 final carrier mass derived from CAD before release.

## 29. State
Nominal carrier:
- unfilled ASA
- 318.4 x 398.4 mm
- 10 mm perimeter ring
- 1.8 mm base thickness
- local magnetic pads
- 6 mm rear bonding land
- 15 mm fabric trim allowance
- 2.8 mm nominal fabric-DML gap
- hidden 28 x 4 mm peel recess at lower center
- two geometric registration datums
- eight magnetic stations.

Status:
**FRONT_CARRIER_318P4X398P4 / 10MM_RING / 1P8MM_BASE / 2P8MM_GAP / C01_TO_C365 / CAD_SOLID_GENERATION_NEXT**.
