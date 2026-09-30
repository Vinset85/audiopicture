# AudioPicture V2.2 Rev.B — front carrier with perimeter-biased D-shaped magnet pads

Status: **REV_B_MAGNET_PAD_TOPOLOGY_FROZEN / DML_HARD_PROJECTION_PROTECTED / REAL_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Resolve the Rev.A front-carrier warning where nominal 12 mm circular magnet pads intruded into the projected DML perimeter.

The DML remains unchanged.

Solution:
- move magnet centers toward the product perimeter;
- replace circular local station pads with perimeter-biased D-shaped pads;
- enforce an explicit DML hard-clearance projection.

## 2. Authoritative global references
Product:
320 x 400 mm.

DML projection:
X=10..310 mm
Y=10..390 mm.

DML global Z:
3.3..9.3 mm nominal.

Front carrier uses product-global assembly transform; local CAD Z is not directly authoritative.

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

## 4. DML projected hard-clearance mask
Do not merely avoid mathematical overlap.

Define expanded DML projected keep-out:
K_DML_MAG = DML projection expanded outward by **0.5 mm**.

Therefore nominal forbidden XY rectangle for rigid magnet-pad material:
X=9.5..310.5
Y=9.5..390.5

where applicable to pad geometry.

Because the carrier perimeter itself necessarily surrounds the DML edge, this mask is specifically applied to local rear-thickened magnet-pad protrusions and target/capture hardware that could violate the DML functional gap.

## 5. D-shaped pad principle
Each local magnetic station uses a nominal 12 mm circular source profile, clipped on the DML-facing side.

The perimeter-facing half remains available for:
- local thickness;
- magnet pocket;
- mechanical capture.

The DML-facing rear-thickened portion is removed before final union.

The base 1.8 mm carrier ring remains governed by its own fabric/DML perimeter interface.

## 6. Top stations
For M1B/M2B:
DML-facing direction = -Y.

Rear-thickened pad geometry shall remain preferentially in:
Y >= 390.5 mm where physically possible.

Because center Y=388 cannot support a full 6 mm radius outside this line, the rear-thickened station cannot remain a simple centered D-shape while also carrying a centered 6 mm magnet pocket.

Therefore the magnet pocket itself must be biased toward +Y relative to the station datum.

## 7. Pocket-offset solution
Separate:
STATION_DATUM from MAGNET_CENTER.

For each station, shift actual magnet center toward product perimeter.

Seed offset:
**3.0 mm outward**.

Revised actual magnet centers:

Top:
M1C=(70,391)
M2C=(250,391)

Bottom:
M3C=(70,9)
M4C=(250,9)

Left:
M5C=(9,135)
M6C=(9,275)

Right:
M7C=(311,135)
M8C=(311,315).

These are packaging seeds and must remain inside the 318.4 x 398.4 carrier material after pocket-wall checks.

## 8. Carrier-boundary consequence
Rev.A carrier projected boundary:
X0.8..319.2
Y0.8..399.2.

For 6.6 mm pocket diameter:
radius 3.3 mm.

At x=9 or x=311:
pocket edge remains x=5.7 or 314.3, inside carrier boundary.

At y=9 or y=391:
edge remains y=5.7 or 394.3, inside carrier boundary.

Therefore all eight 6.6 mm pockets fit the carrier projected boundary with >4.9 mm minimum outer-edge material distance before local wall design.

## 9. DML-side pocket edge
With magnet/pocket center offset to 3 mm outside the DML nominal edge:

Top center y=391:
pocket inner edge y=387.7.

Bottom center y=9:
pocket inner edge y=12.3.

Left center x=9:
pocket inner edge x=12.3.

Right center x=311:
pocket inner edge x=307.7.

Thus the pocket itself still projects across the nominal DML rectangle.

This proves an important packaging fact:
**a 6.6 mm centered pocket cannot be placed fully outside the DML projection within the existing 10 mm product/DML border.**

## 10. Interpretation
The conflict cannot be solved purely in XY using a 6.6 mm magnet pocket and a 10 mm DML edge margin.

The correct solution is Z separation:
- base/front carrier and magnet hardware may overlap the DML projection in XY;
- they must remain forward of the DML front plane with guaranteed functional Z clearance;
- no rear-thickened pad may extend into the DML Z volume.

Therefore Rev.B collision rule becomes a true 3D rule, not a 2D projection rule.

## 11. 3D magnet station envelope
Global DML front:
Z=3.3 mm.

Required DML/front-frame rigid clearance seed:
>=0.5 mm local rigid clearance.

Therefore any rigid magnet pocket/pad rear surface overlapping DML in XY shall satisfy:
**Z_REAR_MAG <= 2.8 mm**.

This leaves 0.5 mm rigid separation to DML front.

The fabric/DML acoustic gap remains separately governed.

## 12. Rev.B local thickness
Rev.A local magnetic pad thickness 3.2 mm is not legal if referenced directly behind Z0 in an XY-overlap region.

Rev.B maximum global rear surface for magnetic stations:
**Z=2.8 mm**.

After accounting for fabric/front wrap and assembly transform, local carrier geometry must be built to this global limit.

This may require:
- magnet pocket opening toward the front/perimeter side;
- thinner capture cap;
- steel target moved to product perimeter counterpart;
- reduced local pad thickness.

## 13. Preferred magnetic architecture update
Preferred:
- 6 x 2 mm magnet remains in removable front carrier;
- magnet axis normal to front;
- magnet pocket positioned near perimeter;
- rear surface of carrier magnetic station <=Z2.8 where overlapping DML;
- discrete steel target resides on fixed perimeter structure in corresponding forward legal Z region.

If this cannot deliver 20..30 N total assembled retention with legal gap, evaluate thinner Candidate B magnet.

## 14. Candidate B packaging advantage
K&J D41 class:
6.35 x 1.59 mm.

Relative to 2.0 mm Candidate A:
~0.41 mm thinner.

This is meaningful because front magnetic station Z, not XY, is now the packaging constraint.

Candidate B therefore becomes a serious packaging alternative rather than merely a secondary magnet.

## 15. Rev.B carrier topology
Base ring:
- 10 mm nominal;
- 1.8 mm nominal.

Magnet station:
- perimeter-biased;
- clipped/D-shaped reinforcement;
- no 3.2 mm rear protrusion in DML-overlap region;
- rear global surface <=Z2.8 when overlapping DML projection.

Local reinforcement may extend farther rearward only outside DML XY hard projection and outside sensor/RF keep-outs.

## 16. DML safety
No DML notch.

No hard contact.

No magnet or target touches DML.

No magnetic station transfers retention load into the compliant DML perimeter.

Magnetic loads close through front carrier to fixed perimeter structure.

## 17. RF constraints
All Rev.B stations remain subject to:
- MAG_KO_RADAR
- MAG_KO_ESP32
- microphone exclusions
- OPT3004 exclusion.

3D legality does not override RF legality.

## 18. CAD regeneration requirements
Generate real Rev.B B-rep with:
- base carrier;
- peel recess;
- eight perimeter-biased station reinforcements;
- actual magnet pocket cuts;
- local rear surface clipped to global Z2.8 where DML-overlap exists;
- locator features when their geometry is finalized.

Report:
- solid count;
- validity;
- volume;
- mass;
- bbox;
- minimum rigid clearance to DML;
- minimum pocket wall;
- pocket-to-outer-edge wall;
- station-to-station connectivity.

## 19. Automatic checks
C431 Rev.B station datums generated.
C432 actual magnet centers may be independently offset from station datums.
C433 all magnet pockets remain inside carrier outer boundary.
C434 2D-only DML collision criterion rejected as insufficient.
C435 no DML notch used.
C436 3D rigid clearance criterion defined.
C437 overlapping magnet station rear surface <=Z2.8.
C438 DML front remains Z3.3.
C439 local rigid DML clearance >=0.5 mm.
C440 base ring remains 1.8 mm nominal.
C441 old 3.2 mm local rear protrusion prohibited in DML-overlap region.
C442 magnetic load path excludes DML.
C443 Candidate B promoted as Z-packaging alternative.
C444 RF exclusions remain independently authoritative.
C445 real Rev.B kernel regeneration required.
C446 minimum pocket wall must be reported.
C447 pocket outer-edge wall must be reported.
C448 assembled force target remains 20..30 N.
C449 fabric-DML acoustic clearance remains separately >=2.0 mm worst-case.
C450 no production release until 3D station collision pass.

## 20. State
The Rev.B redesign resolves the conceptual error in treating the magnet/DML issue as purely planar.

The 10 mm DML border is too narrow to place a 6.6 mm pocket completely outside the DML projection while preserving practical carrier walls.

Therefore the production architecture uses controlled **3D Z separation**:
magnetic hardware may overlap the DML in XY but remains forward of it with >=0.5 mm rigid clearance.

Status:
**MAGNET_DML_CONFLICT_RECLASSIFIED_3D / MAG_STATION_REAR_Z_LE_2P8 / DML_FRONT_Z3P3 / C01_TO_C450 / REAL_REV_B_BREP_NEXT**.
