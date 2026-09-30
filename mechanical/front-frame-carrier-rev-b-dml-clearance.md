# AudioPicture V2.2 Rev.B — front carrier DML-clear magnetic stations

Status: **MAGNET_STATION_REV_B_GEOMETRY_DEFINED / DML_HARD_PROJECTION_PROTECTED / CAD_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Resolve the Rev.A front-carrier magnetic-pad overlap found by the integrated DMU audit.

Hard DML projected rectangle:
X=10..310 mm
Y=10..390 mm.

No rigid magnetic station pad may protrude into this hard projection unless a later detailed perimeter-interface model explicitly proves the region non-active and legal.

Baseline solution:
do not notch the DML.

## 2. Revised magnet centers
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

These are assembly/CAD seeds.

## 3. Geometry problem
A centered circular pad cannot satisfy both:
- magnet pocket around these centers;
- zero overlap with the DML hard rectangle.

Therefore the old symmetric 12 mm circular pad is retired.

## 4. Rev.B station architecture
Each station is a perimeter-facing local cassette.

The cassette extends primarily toward the product perimeter, not toward the DML.

Top stations:
material grows toward +Y.

Bottom:
toward -Y.

Left:
toward -X.

Right:
toward +X.

DML-facing edge is clipped by a hard construction plane.

## 5. Pocket placement
The 6 x 2 mm magnet candidate remains valid, but the magnet center itself cannot remain at only 2 mm from the DML hard boundary if its full circular body must remain outside that boundary.

Therefore the Rev.B coordinate above is interpreted as station locator seed, not final magnet center.

Actual magnet center must be shifted outward enough to keep its physical diameter outside the DML hard rectangle plus tolerance.

## 6. Minimum center offset
For 6.0 mm magnet:
radius=3.0 mm.

Add radial manufacturing/assembly margin:
0.5 mm seed.

Required magnet-center distance from DML hard boundary:
>=3.5 mm.

Thus revised actual magnet centers become:

Top:
M1C=(70,393.5)
M2C=(250,393.5)

Bottom:
M3C=(70,6.5)
M4C=(250,6.5)

Left:
M5C=(6.5,135)
M6C=(6.5,275)

Right:
M7C=(313.5,135)
M8C=(313.5,315).

These centers keep a nominal 0.5 mm margin between a 6 mm magnet body and DML hard projection.

## 7. Product-edge feasibility
Product outer edges:
X=0/320
Y=0/400.

At center 6.5 or 313.5:
magnet body reaches 3.5 mm from outer product edge.

At center Y6.5/393.5:
same.

This leaves space for a perimeter carrier/cassette wall but requires local edge geometry.

## 8. Pocket envelope
Process pocket nominal:
diameter 6.6 mm.

Pocket radius:
3.3 mm.

With center 6.5 mm from product edge:
outer-side remaining material to product boundary:
3.2 mm before cosmetic boundary allowance.

Because carrier outer boundary is inset to 0.8/319.2 and 0.8/399.2, actual remaining wall is:
~2.4 mm.

This is viable as a first structural seed but requires print/peel validation.

## 9. DML-side pocket margin
6.6 mm pocket radius=3.3.

Center-to-DML-boundary distance=3.5.

Nominal residual:
**0.2 mm**.

This is too small for robust printed wall if the pocket itself must be fully isolated from DML projection.

Therefore increase actual magnet center offset to:
**4.5 mm from DML boundary**.

Final Rev.B production-seed centers:

Top:
M1D=(70,394.5)
M2D=(250,394.5)

Bottom:
M3D=(70,5.5)
M4D=(250,5.5)

Left:
M5D=(5.5,135)
M6D=(5.5,275)

Right:
M7D=(314.5,135)
M8D=(314.5,315).

## 10. Final pocket margins
Distance center to DML boundary:
4.5 mm.

Pocket radius:
3.3 mm.

DML-side wall/margin:
**1.2 mm**.

Distance center to carrier outer boundary at 0.8/319.2:
4.7 mm.

Pocket radius:
3.3 mm.

Outer-side material:
**1.4 mm**.

This is tight but printable in ASA with local cassette reinforcement.

## 11. Cassette geometry
Each station uses a local rounded-rectangle/D-shaped cassette.

Seed dimensions:
- tangential length 12 mm;
- radial width 8.5 mm class;
- local Z thickness 3.2 mm;
- pocket 6.6 mm.

The cassette is merged into the 10 mm perimeter ring.

DML-facing side is flat/clipped and never crosses hard DML projection.

Outer-facing side follows carrier edge/radius.

## 12. Local reinforcement
Because outer pocket wall is only ~1.4 mm at the narrowest seed:
- add tangential shoulders;
- use >=2 mm corner radii where possible;
- avoid sharp notch roots;
- orient print/toolpath so pocket hoop strength is not solely interlayer.

Do not globally thicken carrier.

## 13. Mechanical capture
Magnet remains rear-loaded.

Rev.B capture:
- front floor;
- side wall;
- rear printed cap/lip or separate nonmagnetic polymer retainer.

Minimum retained floor/lip thickness is process-qualified.

Adhesive remains secondary.

## 14. Fabric bonding land interaction
Magnetic cassette locally interrupts the nominal 6 mm bonding land.

Fabric bond path must route around cassette while preserving:
>=5 mm effective bonded width or equivalent validated bonded area.

No visible front discontinuity.

## 15. DML clearance policy
For automatic collision:
DML_KO_XY = [10,310] x [10,390].

MAG_CASSETTE_DML_FACING_FACE:
must lie strictly outside this rectangle.

Tolerance reserve:
0.5 mm preferred beyond hard projection where geometry permits.

No DML notch.

## 16. Target side
Steel target must also remain outside DML hard projection.

Target geometry follows perimeter cassette and may be smaller/asymmetric.

Do not use a 10 mm circular target if it violates DML keep-out.

Preferred:
rounded rectangular low-carbon steel tab aligned tangentially.

Exact target magnetic circuit remains force-test gate.

## 17. RF policy
All station coordinates remain subject to:
- radar hard RF exclusion;
- ESP32 antenna exclusion;
- mic/optical exclusions.

If an RF mask rejects a station, move it tangentially along its same perimeter edge before moving radially inward.

Radial inward motion toward DML is last resort and requires geometry requalification.

## 18. Peel recess
Lower-center peel recess at X160 remains clear.

Bottom stations at X70 and X250 provide ~90 mm horizontal separation from peel center.

Progressive peel architecture preserved.

## 19. Expected mass impact
Rev.B cassettes are smaller/asymmetric compared with eight 12 mm full circular pads.

Carrier mass should remain near previous ~28..30 g class.

Real kernel mass is authoritative after regeneration.

## 20. CAD regeneration requirements
Regenerate:
AP22_FRONT_CARRIER_REV_B_DMU.step

Required outputs:
- solid count;
- validity;
- volume;
- mass sensitivity;
- bbox;
- DML intersection volume;
- minimum DML-side XY clearance;
- minimum outer-edge pocket wall.

## 21. Acceptance
PASS only if:
- one connected solid;
- valid B-rep;
- DML rigid intersection volume = 0;
- pocket remains printable/capturable;
- peel recess remains connected/legal;
- carrier stays inside product envelope.

## 22. Automatic checks
C431 Rev.A 12 mm circular station pad retired.
C432 no DML notch baseline.
C433 magnet physical body remains outside DML hard projection.
C434 pocket remains outside DML hard projection.
C435 cassette rigid body remains outside DML hard projection.
C436 actual magnet center radial offset >=4.5 mm from DML boundary.
C437 pocket DML-side margin >=1.2 mm nominal.
C438 pocket outer-side wall >=1.4 mm nominal.
C439 cassette merges into perimeter ring.
C440 cassette local Z <=3.2 mm seed.
C441 fabric bond reroutes around cassette.
C442 effective local fabric bond maintained.
C443 steel target remains outside DML hard projection.
C444 RF rejection moves station tangentially first.
C445 peel recess remains clear.
C446 carrier remains one-part architecture.
C447 real CAD kernel regeneration required.
C448 DML intersection volume must equal zero.
C449 exact minimum clearances reported from kernel.
C450 Rev.B STEP remains DMU until force/RF/process validation.

## 23. State
Rev.B production-seed magnet centers:
- (70,394.5)
- (250,394.5)
- (70,5.5)
- (250,5.5)
- (5.5,135)
- (5.5,275)
- (314.5,135)
- (314.5,315).

Status:
**D_SHAPED_PERIMETER_CASSETTES / MAGNET_CENTERS_4P5MM_OUTSIDE_DML_BOUNDARY / 1P2MM_DML_SIDE_POCKET_MARGIN / C01_TO_C450 / REAL_KERNEL_REGENERATION_NEXT**.
