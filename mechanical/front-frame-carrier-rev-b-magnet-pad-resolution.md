# AudioPicture V2.2 Rev.B — front carrier magnetic-pad resolution

Status: **MAGNET_PAD_DML_CONFLICT_RESOLVED_BY_EDGE_CHANNEL_ARCHITECTURE / REV_B_CAD_CONTRACT_READY / REAL_KERNEL_REGENERATION_REQUIRED**

## 1. Trigger
The Rev.A 12 mm circular magnet pads overlap the DML projected hard region.

DML projection:
X=10..310 mm
Y=10..390 mm.

The Rev.B magnetic centers were moved toward the product perimeter:
M1B (70,388)
M2B (250,388)
M3B (70,12)
M4B (250,12)
M5B (12,135)
M6B (12,275)
M7B (308,135)
M8B (308,315).

A simple D-shaped 12 mm pad centered at those coordinates is still not sufficient to guarantee zero overlap because each center remains only 2 mm from the DML projected boundary.

## 2. Geometric finding
A 6 mm diameter magnet has radius 3 mm.

For a magnet itself to remain completely outside the DML projected rectangle, its center would need at least 3 mm beyond the relevant DML boundary.

Examples:
- top: center Y >=393 mm;
- bottom: center Y <=7 mm;
- left: center X <=7 mm;
- right: center X >=313 mm.

Those coordinates are geometrically possible inside the 320 x 400 product, but they leave very limited carrier edge material if a conventional circular pocket is used.

Therefore the correct solution is not merely a D-shaped pad at the Rev.B centers.

## 3. Rev.B architecture
Adopt an **edge-channel magnet cassette** architecture.

Each magnetic station uses:
- magnet axis normal to front plane;
- magnet center shifted into the outer 7 mm edge band;
- elongated local carrier reinforcement toward the product edge;
- DML-facing wall clipped to the DML hard boundary;
- rear retention cap integrated from the perimeter side.

The DML is not notched.

## 4. Revised magnet centers Rev.C seed
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

For magnet radius 3 mm:
- top magnet inner edge Y=392 > DML max Y390;
- bottom magnet inner edge Y=8 < DML min Y10;
- left magnet inner edge X=8 < DML min X10;
- right magnet inner edge X=312 > DML max X310.

Nominal magnet-to-DML projected clearance:
**2 mm**.

## 5. Pocket envelope
Candidate A magnet:
6 x 2 mm.

Process pocket seed:
diameter 6.6 mm.

Pocket radius:
3.3 mm.

Using the pocket itself as the hard envelope, nominal clearance becomes:
- top inner pocket edge 391.7 -> 1.7 mm beyond DML;
- bottom 8.3 -> 1.7 mm;
- left 8.3 -> 1.7 mm;
- right 311.7 -> 1.7 mm.

PASS nominal.

## 6. Edge material
At center coordinate 5 mm with a 3.3 mm pocket radius:
outer residual to product boundary:
1.7 mm.

At center 315 mm:
same 1.7 mm.

At top Y395:
1.7 mm to Y398.4-class carrier boundary depending exact local outline.

This is too thin to rely on as an unsupported circular boss wall.

Therefore each station uses an elongated tangential cassette/reinforcement integrated into the perimeter ring.

## 7. Cassette footprint
Seed local cassette:
- tangential length 18 mm;
- radial width 8.0 mm;
- local thickness 3.2 mm;
- pocket centered in cassette;
- DML-facing edge clipped at least 1.0 mm away from DML hard projection;
- outer edge merged into carrier perimeter.

Tangential orientation:
- top/bottom: long axis X;
- left/right: long axis Y.

## 8. DML-facing clipping
Define DML hard projection plus manufacturing guard:
G_DML_MAG = 1.0 mm.

Forbidden pad region:
X=9..311
Y=9..391
when applied to the relevant DML-facing side logic.

However the magnet pocket itself already sits outside the DML projection.

The structural cassette shall not protrude into the active DML front-clearance volume unless its Z is proven non-interfering.

Baseline:
clip cassette DML-facing geometry to remain outside DML projected boundary plus guard.

## 9. Important distinction
The fabric carrier perimeter can overlap the DML projection in XY if it remains entirely in the front perimeter stack and does not violate the fabric-DML gap.

The **rearward 3.2 mm magnet cassette** is the hard feature that must remain outside the DML collision region.

Collision checks therefore operate on 3D solids, not only 2D projection.

## 10. Global Z
Visible fabric:
Z=0.

DML front:
Z=3.3.

Rearward cassette maximum local thickness must be transformed so its rear face remains strictly forward of DML front minus required local clearance, unless it lies outside DML XY.

Because Rev.C cassette lies outside DML XY, it may extend rearward locally without entering the DML solid.

## 11. Locator compatibility
LOC_A/LOC_B remain separate from magnets.

Do not move locators into the thin edge channel simply because magnets moved.

Locators attach to robust perimeter segments away from radar/optical/mic exclusions.

## 12. Peel compatibility
Lower-center peel recess remains centered X160.

M3C/M4C remain X70/X250, so peel initiation stays ~90 mm from each lower magnet.

Progressive release architecture preserved.

## 13. Magnetic force consequence
Moving magnets outward does not inherently change the magnet-to-target normal gap.

Target tabs move with the station.

G_MAG sweep remains:
0.5/0.8/1.0/1.2 mm equivalent.

Retention target remains:
20..30 N total assembled.

## 14. RF consequence
More perimeter-biased magnetic hardware is preferred relative to central RF-sensitive regions.

Nevertheless:
- exact ESP32 antenna keep-out remains authoritative;
- radar cone remains authoritative;
- M8C must be checked particularly against upper-right RF architecture.

No magnetic station is frozen for production until exact RF mask pass.

## 15. Printability
1.7 mm outer residual around the circular pocket is not treated as a standalone wall.

Tangential cassette spreads load into:
- perimeter ring;
- adjacent local thickening.

Minimum printed wall around captured magnet shall be process-qualified.

Magnet capture remains mechanical plus adhesive secondary retention.

## 16. Rev.B carrier geometry changes
From Rev.A carrier:
- replace M1..M8 centers with M1C..M8C;
- remove 12 mm circular rear bosses;
- add eight tangential edge cassettes;
- retain base perimeter ring;
- retain peel recess;
- retain artwork datum;
- retain fabric bonding land except local cassette relief;
- retain two independent locators.

## 17. Expected mass
Removing eight 12 mm circular pads and replacing them with clipped 18 x 8 mm local cassettes will modestly change mass.

Carrier-only target remains:
<35 g preferred;
<60 g hard budget.

Exact OpenCASCADE mass is required.

## 18. Real CAD regeneration acceptance
The next kernel build must report:
- one valid solid;
- exact volume;
- exact mass sensitivity;
- bounding box;
- all eight pocket solids/cuts present;
- no cassette/DML hard collision;
- peel recess connected;
- minimum outer wall;
- minimum DML-side clearance.

## 19. Automatic checks
C431 Rev.B center-only D-shaped concept identified as insufficient.
C432 magnet radius clearance condition derived.
C433 pocket radius clearance condition derived.
C434 Rev.C centers generated.
C435 M1C/M2C Y=395.
C436 M3C/M4C Y=5.
C437 M5C/M6C X=5.
C438 M7C/M8C X=315.
C439 nominal 6 mm magnet projected DML clearance >=2 mm.
C440 nominal 6.6 mm pocket projected DML clearance >=1.7 mm.
C441 1.7 mm outer residual not accepted as standalone boss wall.
C442 tangential edge cassette defined.
C443 top/bottom cassette long axis X.
C444 side cassette long axis Y.
C445 cassette local thickness 3.2 mm seed.
C446 DML not modified/notched.
C447 peel architecture preserved.
C448 G_MAG sweep preserved.
C449 retention target preserved.
C450 exact RF mask still required.
C451 LOC_A/LOC_B remain independent.
C452 real kernel regeneration required.
C453 carrier mass target <35 g preferred.
C454 carrier hard mass budget <60 g.
C455 3D collision, not only 2D projection, is release authority.

## 20. State
The previous Rev.B center shift alone is withdrawn as the final geometry solution.

New baseline:
**perimeter edge-channel magnetic cassettes** with Rev.C station centers.

This provides real geometric separation between the 6.6 mm magnet pocket and the 300 x 380 mm DML projection without cutting the DML.

Status:
**EDGE_CHANNEL_MAGNET_CASSETTE_BASELINE / REV_C_CENTERS / 1P7MM_POCKET_TO_DML_PROJECTION_CLEARANCE / C01_TO_C455 / OPENCASCADE_REGENERATION_NEXT**.
