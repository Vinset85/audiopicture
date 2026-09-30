# AudioPicture V2.2 Rev.A — front-frame magnet candidate and coordinate map

Status: **8_STATION_COORDINATES_FROZEN_AS_SEEDS / MAGNET_CANDIDATES_REAL / ASSEMBLED_FORCE_VALIDATION_REQUIRED**

## 1. Candidate magnetic components
Candidate A:
- supermagnete S-06-02-N
- NdFeB N45
- diameter 6.0 mm
- thickness 2.0 mm
- axial magnetization
- tolerance +/-0.1 mm
- mass 0.43 g
- manufacturer stated attraction approximately 7.26 N under its test condition
- max operating temperature 80 C.

Candidate B:
- K&J D41
- NdFeB N42
- diameter 6.35 mm
- thickness 1.59 mm
- axial magnetization
- manufacturer Pull Force Case 1 1.19 lb / 0.54 kg equivalent under its defined thick-steel-plate test condition
- max operating temperature 80 C.

Neither catalogue pull value is an assembled front-frame retention value.

## 2. Selection direction
Mechanical CAD envelope baseline:
**MAGNET_ENV = diameter 6.6 mm x 2.2 mm**

This envelope accommodates Candidate A plus tolerance/assembly allowance and approximately accommodates Candidate B diameter with pocket adjustment.

Candidate A is the packaging reference because it is metric 6 x 2 mm.

Force is intentionally tuned by magnetic circuit/gap rather than assuming eight direct-contact stations.

## 3. Target
Use local low-carbon steel target tabs/discs only in legal non-RF perimeter regions.

Initial target envelope:
- 10 x 10 mm local tab or diameter 10 mm disc class
- thickness 0.8..1.2 mm sensitivity.

Exact alloy/coating/MPN open.

No continuous steel ring.

## 4. Magnetic gap
Define effective magnetic gap:
G_MAG = polymer/adhesive/air equivalent separation.

Sweep:
- 0.5 mm
- 0.8 mm
- 1.0 mm
- 1.2 mm.

Goal:
assembled total normal retention 20..30 N, not maximum possible pull.

## 5. Product coordinate system
Origin:
front lower-left.

X right.
Y up.

Product:
320 x 400 mm.

Magnet coordinates are center points.

## 6. Eight station seed coordinates
Top:
M1 = (70, 386)
M2 = (250, 386)

Bottom:
M3 = (70, 14)
M4 = (250, 14)

Left:
M5 = (14, 135)
M6 = (14, 275)

Right:
M7 = (306, 135)
M8 = (306, 315)

All coordinates remain parametric +/- local legal adjustment.

## 7. Distribution rationale
Top pair:
- separated from center;
- avoid central upper MAIN-C projection as much as possible;
- targets must remain outside ESP32 RF exclusion after exact antenna map.

Bottom pair:
- outside central service recess X100..220;
- do not obstruct lower peel/release feature.

Left pair:
- perimeter-biased;
- avoid microphone square and central DML active area.

Right pair:
- M7 below/away from radar center region;
- M8 upper-right but must be clipped against final ESP32/RF masks.

Exact radar/ESP32 masks remain authoritative.

## 8. Forbidden relocation
Automatic placement shall reject any station if target/magnet envelope intersects:
- MAG_KO_RADAR
- MAG_KO_ESP32
- MAG_KO_MIC_1..4
- MAG_KO_OPTICAL
- DML service/removal keep-out.

## 9. Pocket geometry
Front carrier magnet pocket seed:
- diameter 6.6 mm
- depth 2.2 mm for Candidate A class;
- local back wall/capture lip according to print orientation;
- mechanical lip or cap required;
- adhesive is secondary retention.

Candidate B pocket variant:
- diameter >=6.9 mm process-adjusted
- depth >=1.8 mm.

## 10. Mechanical capture
Preferred:
rear-loaded magnet pocket with printed retention cap/lip.

Requirements:
- magnet cannot fall inward toward DML if adhesive fails;
- magnet replacement possible at workshop level before final closure method;
- polarity irrelevant for magnet-to-steel architecture.

## 11. Target mounting
Steel target attaches to product-side structural/cosmetic interface only where:
- RF legal;
- structurally supported;
- cannot detach into electronics;
- target does not bridge DML compliant perimeter.

Target retention must be mechanical or mechanically trapped plus adhesive.

## 12. Force budget
Target total assembled normal force:
20..30 N.

Eight equal stations imply:
2.5..3.75 N average/station.

Candidate A catalogue attraction is about 7.26 N under the manufacturer's stated condition, so direct ideal contact at eight stations would exceed the product target.

Therefore use controlled G_MAG/target geometry and measure the actual assembly.

No production release from catalogue multiplication.

## 13. Peel behavior
Normal total force and peel-removal force are different.

Removal begins from lower hidden relief near center/side but not directly adjacent to one station.

Target local peel:
- initial release comfortable by hand;
- no sudden snap that lets frame strike DML;
- sequential station release.

Evaluate 6/8/10 station layouts if peel curve is poor even when total force is correct.

## 14. Mass
Candidate A:
8 x 0.43 g = 3.44 g magnets.

Targets estimated separately.

Magnetic hardware remains comfortably within the prior 10..25 g magnetic-system budget.

## 15. Temperature
Both cited magnet candidates are 80 C class.

Front-frame operating temperature should remain far below this in normal use, but thermal qualification still checks demagnetization/adhesive/capture at elevated product temperature.

## 16. RF verification
Before production:
- near-field/RF comparison without magnetic hardware;
- magnets only;
- magnets + steel targets;
- full front frame.

Radar and Wi-Fi performance must be checked separately.

## 17. CAD checks
C321 all eight magnet centers generated.
C322 Candidate A envelope fits 6.6 x 2.2 pocket seed.
C323 M3/M4 remain outside service recess.
C324 no continuous steel ring.
C325 each target is discrete.
C326 G_MAG sweep 0.5/0.8/1.0/1.2 supported.
C327 total retention target remains 20..30 N.
C328 catalogue pull values not summed as production proof.
C329 magnet capture survives adhesive failure.
C330 target capture survives adhesive failure.
C331 exact radar keep-out clips/rejects stations automatically.
C332 exact ESP32 keep-out clips/rejects stations automatically.
C333 microphone hard regions reject stations.
C334 optical hard region rejects stations.
C335 magnetic hardware mass included in front-frame budget.
C336 peel feature remains clear of M3/M4.
C337 6/8/10 station variants remain regenerable.
C338 thermal qualification includes magnet/adhesive/capture.
C339 RF test includes steel targets.
C340 final station coordinates require exact RF-mask pass.

## 18. Release state
Candidate A:
**S-06-02-N / 6 x 2 mm / N45 / packaging reference**

Candidate B:
**D41 / 6.35 x 1.59 mm / N42 / lower-profile alternative**

Station seeds:
M1 (70,386)
M2 (250,386)
M3 (70,14)
M4 (250,14)
M5 (14,135)
M6 (14,275)
M7 (306,135)
M8 (306,315)

Status:
**REAL_MAGNET_CANDIDATES_SELECTED / 8_STATION_XY_SEED_MAP / CONTROLLED_GAP_REQUIRED / C01_TO_C340 / RF_AND_FORCE_TEST_GATE_OPEN**.
