# AudioPicture V2.2 Rev.B — front carrier magnetic perimeter correction

Status: **MAGNET_CENTERS_MOVED_TO_TRUE_10MM_PERIMETER / DML_PROJECTED_OVERLAP_REMOVED_ANALYTICALLY / REAL_BREP_REGENERATION_REQUIRED**

## 1. Problem found
DML projection:
X=10..310
Y=10..390 mm.

Magnet candidate A:
diameter 6 mm, radius 3 mm.

The previous Rev.B center proposal at 12 mm from the product edge is not sufficient.

Example left station:
center X=12 -> magnet reaches X=15.

Because DML begins at X=10, the magnet itself—not only its 12 mm support pad—overlaps the DML projected region by 5 mm.

Therefore D-shaped support pads alone cannot solve the problem if the magnet center remains at 12 mm.

## 2. Governing geometry
For a left-side 6 mm magnet to remain fully outside DML projection:
X_center + 3 <= 10.

Therefore:
X_center <= 7 mm.

Right:
X_center - 3 >= 310
therefore X_center >=313 mm.

Bottom:
Y_center + 3 <=10
therefore Y_center <=7 mm.

Top:
Y_center -3 >=390
therefore Y_center >=393 mm.

## 3. Carrier boundary feasibility
Carrier projected boundary:
X=0.8..319.2
Y=0.8..399.2.

At center coordinate 7 mm:
magnet edge reaches 4..10 mm.

This remains inside the carrier projected boundary with >3 mm gross distance from the carrier outer boundary.

At center coordinate 313 mm:
magnet spans 310..316 mm.

Also inside carrier boundary.

Equivalent top/bottom geometry is feasible.

## 4. Revised station centers Rev.C seed
Use 7 mm boundary centers for simple exact DML tangency:

Top:
M1C=(70,393)
M2C=(250,393)

Bottom:
M3C=(70,7)
M4C=(250,7)

Left:
M5C=(7,135)
M6C=(7,275)

Right:
M7C=(313,135)
M8C=(313,315).

The nominal 6 mm magnet envelope is tangent to the DML projected boundary but does not enter it.

## 5. Manufacturing clearance
Exact tangency is not a production clearance.

Therefore CAD shall introduce a positive DML-side clearance.

Preferred center offset:
**6.5 mm from the applicable product edge** where carrier geometry permits.

Then:
left magnet inner edge = 9.5 mm
right magnet inner edge =310.5 mm
bottom inner edge=9.5 mm
top inner edge=390.5 mm.

Nominal projected DML clearance:
**0.5 mm**.

Alternative:
center=6.0 mm -> 1.0 mm projected clearance.

The 6.0/6.5/7.0 sweep is required.

## 6. Revised support pad
A circular 12 mm pad cannot remain outside the 10 mm DML border.

Replace it with a perimeter-biased D-shaped or obround station base.

Requirements:
- magnet pocket remains circular 6.6 mm class;
- support material expands toward product exterior/perimeter direction;
- DML-facing hard edge remains <=X9.5, >=X310.5, <=Y9.5, or >=Y390.5 as applicable for nominal 6.5 mm center;
- local fillets preserve printability;
- no hard station geometry enters DML projected keep-out.

## 7. Corner avoidance
Stations remain away from corners to avoid:
- fabric wrap concentration;
- corner warp;
- locator conflicts.

Tangential coordinates along each side remain:
70 / 250 mm top/bottom;
135 / 275 mm left;
135 / 315 mm right.

These tangential coordinates may still move under exact RF masks.

## 8. Magnetic force consequence
Moving the magnet closer to the outer edge does not inherently change normal magnetic force if:
- target alignment follows;
- G_MAG remains unchanged;
- target geometry remains equivalent.

Peel behavior may improve because stations are closer to the carrier free edge.

This must be measured.

## 9. Structural consequence
The narrower inner ligament means local station reinforcement must grow outward/tangentially rather than inward over DML.

Do not thicken toward DML.

If printed ASA strength is insufficient:
1. lengthen station base tangentially;
2. add local fillets;
3. increase local Z only if global front stack permits;
4. only then consider smaller magnet diameter.

Do not notch DML baseline.

## 10. Locator interaction
LOC_A/LOC_B must not occupy the same narrow 10 mm perimeter segment as a magnetic pocket unless combined geometry is explicitly solved.

Keep at least one station pitch away from locator features where practical.

## 11. Fabric bonding land
The 6 mm bonding land and magnet station compete for the 10 mm perimeter.

At each magnetic station:
- bonding land may locally neck/route around the pocket;
- minimum adhesive load path must remain continuous;
- no magnet is bonded through the fabric.

Local bonding-land reduction below 5 mm requires process validation and shall not become a continuous weak segment.

## 12. Real B-rep regeneration requirements
Generate Rev.B carrier with:
- 318.4 x 398.4 outer boundary;
- 10 mm ring;
- 1.8 mm base;
- magnet center sweep 6.0/6.5/7.0 mm;
- D-shaped station pads;
- 6.6 mm pocket;
- lower peel recess;
- no DML projected overlap.

For each variant record:
- solid count;
- validity;
- volume;
- mass;
- minimum DML projected clearance;
- minimum outer-wall ligament;
- minimum fabric bonding-land width.

## 13. Acceptance
Preferred:
center=6.5 mm if all carrier ligaments and fabric land pass.

Accept center=6.0 mm if more DML clearance is required and outer-edge structure remains adequate.

Reject center=7.0 mm for production if zero nominal DML clearance remains after exact tolerances.

## 14. Automatic checks
C431 12 mm station-center concept rejected.
C432 magnet physical envelope included in DML collision test.
C433 left center <=7 mm geometric requirement.
C434 right center >=313 mm geometric requirement.
C435 bottom center <=7 mm geometric requirement.
C436 top center >=393 mm geometric requirement.
C437 6.0/6.5/7.0 center sweep defined.
C438 6.5 mm preferred seed gives 0.5 mm nominal DML projected clearance.
C439 6.0 mm alternative gives 1.0 mm nominal DML projected clearance.
C440 7.0 mm exact tangency not production-frozen.
C441 12 mm circular station pad retired.
C442 perimeter-biased D-shaped pad required.
C443 support growth directed outward/tangentially.
C444 no DML notch baseline.
C445 bonding land reroutes locally around magnet pocket.
C446 magnet remains mechanically captured.
C447 target follows revised station coordinates.
C448 RF masks remain authoritative.
C449 real B-rep regeneration required.
C450 real B-rep must report minimum DML clearance.

## 15. State
Previous MxB centers at 12 mm:
**REJECTED FOR DML CLEARANCE**.

New preferred normal offset:
**6.5 mm from product edge**.

Nominal 6 mm magnet projected clearance to DML:
**0.5 mm**.

Next:
real OpenCASCADE Rev.B carrier regeneration and tolerance screen.

Status:
**TRUE_PERIMETER_MAGNET_LAYOUT / 6P5MM_CENTER_SEED / 0P5MM_DML_CLEARANCE / C01_TO_C450 / BREP_REGENERATION_NEXT**.
