# AudioPicture V2.2 Rev.A — ASA rear-shell parametric part

Status: **REAR_SHELL_PARAMETRIC_ARCHITECTURE_FROZEN / 40MM_ENVELOPE_PRESERVED / MAGNET_AND_FASTENER_MPN_GATES_OPEN**

## 1. Purpose
Define the printable ASA rear shell as a real assembly part around the validated PC-CF structural frame.

The rear shell:
- closes and protects the electronics;
- provides hidden passive ventilation;
- provides service/cable openings;
- provides cosmetic rear surfaces;
- interfaces to the PC-CF frame;
- does not replace the primary PC-CF wall-mount load path.

## 2. Master envelope
Product maximum:
- X 320 mm
- Y 400 mm
- Z 40 mm absolute target.

Rear shell outermost surface:
**Z <=40.0 mm**

Nominal rear-shell outer plane:
**Z = 40.0 mm**

Nominal inner plane for 2.2 mm shell:
**Z = 37.8 mm**

This is consistent with the existing ~37.6..38.0 mm inner-plane seed.

## 3. Shell thickness
Baseline:
**2.2 mm ASA**

Parametric sweep:
- 2.0 mm
- 2.2 mm
- 2.4 mm.

Use local ribs/beads rather than globally increasing wall thickness.

Local bosses/interfaces may exceed 2.4 mm where required, but must respect component keep-outs.

## 4. Perimeter geometry
Rear shell projected outer size:
- nominal 320 x 400 mm external product boundary.

Use:
- rounded external rear edge;
- local edge radius seed 2.0..3.0 mm;
- no cosmetic feature may exceed product envelope.

The PC-CF frame remains inset from cosmetic outer edge.

## 5. Frame-to-shell clearance
Non-precision perimeter fit seed:
- radial/XY clearance 0.5 mm nominal;
- CAD sweep 0.4..0.7 mm.

Z clearance:
- avoid broad hard contact with hot/high-vibration components;
- local structural contact only at intentional interfaces.

ASA shrink/warp/process compensation is applied after print coupons.

## 6. Shell retention philosophy
Rear shell is removable for service.

Preferred:
- hidden mechanical screws/clips into PC-CF frame;
- no adhesive-only permanent closure;
- no load-bearing snap feature as sole retention.

Seed:
- 6 to 8 perimeter retention points.

Final screw/insert MPN remains open.

Do not reuse the four wall-cleat M4 nodes as cosmetic shell fasteners.

## 7. Retention-node locations
Initial eight-point pattern:
- top: X80, X160, X240 at Y382
- sides: X12/Y200 and X308/Y200
- bottom: X80, X160, X240 at Y18.

Exact nodes are clipped/moved around:
- vent banks;
- service recess;
- RF zones;
- structural frame legal attachment points.

A six-point variant may be selected if stiffness/warp tests pass.

## 8. Local shell stiffening
Use shallow rear-surface beads/ribs:
- 1.2..1.8 mm added rib height;
- 1.2..1.8 mm rib width seed;
- broad radiused roots.

Avoid:
- full-width horizontal ribs blocking chimney;
- ribs in radar RF forward zone;
- ribs contacting DML/exciters;
- ribs over Ag53024/tall MAIN-C regions.

Shell ribs are anti-drum/anti-warp features, not primary wall-mount members.

## 9. Vent banks
Import Rev.B vent geometry.

Lower inlet:
- 12 slots total;
- each 3 x 40 mm;
- gross 1440 mm2;
- effective seed ~1080 mm2.

Upper outlet:
- 10 slots total;
- each 3 x 45 mm;
- gross 1350 mm2;
- effective seed ~1080 mm2.

Slot ends:
- R1.5 mm.

Solid web:
- >=3 mm seed.

No direct DML acoustic line of sight.

## 10. Vent baffles
Baffles are separate internal ASA features fused to rear shell where manufacturable.

Rules:
- at least two direction changes inlet-to-main-cavity where packaging permits;
- do not reduce effective inlet below CFD target;
- no baffle contacts moving/vibrating DML;
- no dense foam/filter baseline.

Baffle thickness:
- 1.6..2.0 mm seed.

## 11. Service recess
Central lower service recess:
- X100..220
- Y20..48
- rear/service Z region.

Functions:
- Ethernet cable exit;
- 24 V service/access path as applicable;
- USB service access.

It is not credited as guaranteed thermal inlet area.

Edges:
- radiused;
- reinforced locally;
- no sharp shell notch.

## 12. RJ45 tunnel interface
RJ45 remains on MAIN-C.

Rear shell provides:
- guided passive cable recess/tunnel;
- no electrical extension;
- no raw-MDI remote harness.

Cable must be insertable/removable with ordinary flexible Cat5e/Cat6 patch lead.

Latch access must remain possible.

## 13. Wall gap
Nominal installed wall gap:
**4 mm**

Rear shell/support geometry must not locally close the hot-air escape path.

Sweep:
3 / 4 / 5 mm.

Lower supports remain structurally tied to PC-CF, not cosmetic ASA alone.

## 14. RF regions
ESP32:
- avoid metal target/fastener near antenna keep-out;
- minimize carbon-filled frame behind/around antenna according to RF review.

Radar:
- ASA/unfilled polymer is allowed subject to radome/EM validation;
- no PC-CF/metal introduced in forward RF cone;
- shell thickness in radar window remains controlled and locally uniform.

Define:
RADAR_WINDOW_T = 2.0..2.2 mm seed.

No cosmetic rib crosses the radar window.

## 15. ENV interfaces
SHT45:
- separate room-air microchannel/chamber;
- not main chimney;
- thermally weak connection.

OPT3004:
- separate optical tunnel through front system;
- rear shell does not create uncontrolled light leakage.

## 16. Print orientation
Primary candidate:
- rear cosmetic face on/parallel to build plane only if surface quality and warping are acceptable.

Alternative:
- edge/tilted orientation if dimensional stability improves.

Because the shell is 320 x 400 mm, printer build-volume and warp capability are manufacturing gates.

No orientation is frozen until ASA coupon/large-panel warp test.

## 17. Print process seeds
ASA baseline:
- enclosed printer required/preferred;
- controlled chamber/ambient;
- dry filament/process control;
- brim/fixture strategy as required.

Exact temperatures follow qualified filament/printer profile, not this CAD document.

## 18. Assembly tolerance stack
Seed clearances:
- shell/frame XY: 0.5 mm nominal;
- removable rigid component/service clearance >=1.0 mm where feasible;
- vent baffle/frame clearance >=1.0 mm;
- cable tunnel clearance determined from actual cable/boot sweep;
- rear shell to tallest rigid component >=1.0 mm static target.

No interference is accepted merely because ASA can flex.

## 19. Front-frame magnetic interface boundary
Rear shell may provide target/support datum for front-frame retention only where mechanically appropriate.

However:
- magnet MPN open;
- target material/geometry open;
- holding force open pending front-frame mass and pull-off target.

Create parametric pockets only after magnetic system selection.

Do not place magnetic steel in radar/ESP32 RF keep-outs.

## 20. Service sequence
Target:
1. remove front frame if required by service operation;
2. release hidden rear-shell retention;
3. lift/remove rear shell without disturbing DML;
4. disconnect only service-relevant harnesses;
5. access MAIN-C/P/daughterboards;
6. reassemble without adhesive replacement.

Wall-mount cleats remain independent from shell service retention.

## 21. Cosmetic/rear labels
Allowed recessed/embossed rear labels:
- model/revision;
- ETH;
- 24 V;
- USB/service;
- regulatory marks when applicable.

Labels must not reduce wall-gap airflow or create thin weak sections.

## 22. Z-stack check
With rear outer plane at Z40 and 2.2 mm shell:
- inner plane Z37.8.

EX25FHE2 coarse rear keep-out:
- approximately to Z35;
- nominal shell clearance ~2.8 mm.

Ag53024 conservative top:
- approximately Z33.6;
- nominal shell clearance ~4.2 mm.

Generic rigid component target:
- <=Z36.6;
- nominal clearance to 2.2 mm shell inner plane ~1.2 mm.

Therefore:
**40 mm envelope remains conditionally closed at nominal 2.2 mm shell thickness.**

Exact STEP collision remains authoritative.

## 23. Automatic checks
C266 rear shell outer Z <=40.0 mm.
C267 nominal shell thickness 2.2 mm.
C268 2.0/2.2/2.4 thickness sweep rebuilds.
C269 shell/frame nominal XY clearance 0.5 mm.
C270 rear shell is not primary wall-mount load path.
C271 shell service retention independent of wall-cleat M4 nodes.
C272 six/eight retention-node variants supported.
C273 shell ribs do not block vertical chimney.
C274 shell ribs clear radar RF window.
C275 Rev.B inlet geometry retained.
C276 Rev.B outlet geometry retained.
C277 service recess not credited as thermal inlet.
C278 RJ45 remains directly on MAIN-C.
C279 ordinary Ethernet plug/latch removal sweep preserved.
C280 4 mm nominal wall gap preserved.
C281 radar window thickness controlled.
C282 SHT45 chamber separate.
C283 shell/component static clearance >=1 mm target.
C284 EX25FHE2 coarse shell clearance positive.
C285 Ag53024 conservative shell clearance positive.
C286 no magnet/steel target introduced before RF-compatible placement.
C287 rear shell removable without adhesive destruction.
C288 wall mount remains functional with shell removed where service concept requires.
C289 print orientation remains qualification gate.
C290 exact manufacturer-solid collision required before release.

## 24. State
Rear-shell architecture:
**FROZEN AS PARAMETRIC PART**

Nominal:
- ASA
- 2.2 mm wall
- Z inner 37.8
- Z outer 40.0
- hidden Rev.B vents
- removable service closure
- 4 mm installed wall gap.

Open gates:
- exact retention fastener MPN;
- large-panel ASA warp qualification;
- CFD;
- exact component STEP collision;
- RF/radome validation;
- front-frame magnetic system.

Status: **ASA_REAR_SHELL_2P2MM / Z37P8_TO_40 / REMOVABLE / REV_B_VENTS / C01_TO_C290 / 40MM_CONDITIONALLY_CLOSED**.
