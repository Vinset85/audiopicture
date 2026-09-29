# AudioPicture V2.2 Rev.A — MAIN-C mechanical envelope closure

Status: **MAIN_C_COMPONENT_HEIGHT_CLASSES_DEFINED / RJ45_CABLE_SERVICE_AND_AG53024_EXACT_CAD_RELEASE_GATE**

## 1. Scope
Close the first-order mechanical envelope of MAIN-C:
- Ag53024 PoE module;
- TE 2-1734264-1 RJ45;
- Wurth 7490220121 Ethernet magnetics;
- GCT USB4085 USB-C;
- W5500/ESP32/logic;
- connector mating/service volumes.

MAIN-C board:
- 150 x 55 mm;
- product X=85..235 mm;
- Y=315..370 mm;
- PCB Z=17.0..18.6 mm.

Generic rear component limit:
- approximately Z=36.6 mm.

Available nominal rear-side height:
**~18.0 mm**

## 2. Ag53024
Ag53024 remains the PoE module owned by MAIN-C.

Electrical anchors already frozen:
- isolated regulated 24 V output;
- 24 W continuous;
- 30 W peak;
- 1500 Vdc isolation.

Mechanical packaging class:
**H3, approximately 14 mm body-height class** pending exact manufacturer CAD/drawing import.

With PCB rear surface at Z=18.6 mm:
- 14 mm body -> Z~32.6 mm;
- residual to generic rear component limit ~4 mm.

First-order result:
**PASS WITH MARGIN, EXACT CAD REQUIRED**

No frame rib/rear-shell boss may occupy the module top/service volume.

## 3. TE 2-1734264-1 RJ45
The selected TE part is a shielded 8P8C modular jack family device.

Mechanical treatment:
- body envelope shall come from the TE manufacturer drawing/3D model;
- shield tabs/board retention are included in the exact CAD;
- cable plug and boot are a separate service volume.

Do not judge RJ45 compatibility from PCB-body height alone.

### RJ45 cable strategy
Preferred product architecture:
**side/downward cable egress**, not straight rearward toward the wall.

Reason:
a conventional RJ45 plug/strain-relief extending directly rearward can consume more depth than the connector body and conflict with the wall gap.

Therefore the rear shell shall include a recessed cable bay or edge exit that turns the Ethernet cable parallel to the wall/product plane.

Create:
- RJ45_BODY_ENVELOPE;
- RJ45_PLUG_ENVELOPE;
- RJ45_BOOT_BEND_VOLUME;
- ETH_CABLE_EXIT_CORRIDOR.

The cable must be installable without exceeding the intended wall installation envelope.

## 4. Wurth 7490220121 magnetics
Use exact manufacturer mechanical drawing/3D model in native CAD.

Mechanical class:
**H2/H3 low-profile magnetics region**, exact height from imported part.

Because it sits between W5500 and RJ45:
- keep MDI traces short;
- do not move magnetics solely for cosmetic cable routing;
- solve the connector bay around the electrical placement.

First-order Z is not expected to exceed the 18 mm rear-side allowance.

## 5. USB-C GCT USB4085
USB4085 remains the service USB-C receptacle candidate.

Known architecture:
- top-mount USB-C;
- through-hole retention;
- manufacturer drawing/3D available.

USB is a service interface, not the normal installed cable.

Preferred egress:
**bottom/side recessed service opening**.

Create:
- USB4085_BODY_ENVELOPE;
- USB_C_PLUG_SERVICE_VOLUME.

The product need not remain wall-flush with a USB cable permanently inserted, but the service cable must be insertable without disassembling the electronics.

## 6. ESP32-S3
ESP32-S3-WROOM-1-N16R8 remains in C3.

Mechanical rule dominates over height:
- antenna end faces outward;
- no metal/PC-CF/Ag53024/RJ45 shield in antenna keep-out;
- rear shell locally unfilled/nonconductive ASA or equivalent.

The module itself is not a Z blocker.

## 7. W5500 and low-profile logic
W5500, oscillator and passives are H0/H1 class relative to the 18 mm rear allowance.

They are not primary mechanical blockers.

## 8. MAIN-C local height map
C1:
- RJ45 body: exact-CAD gate;
- Ethernet magnetics: exact-CAD gate;
- PoE input/bridge: low/medium;
- Ag53024 input domain.

C2:
- Ag53024: H3 ~14 mm class;
- W5500: low profile;
- USB-C: connector/service-volume gate;
- JCP/JCS mating volumes.

C3:
- ESP32: low profile but RF keep-out dominant;
- daughterboard FPC connectors;
- low-power logic.

## 9. Rear-shell strategy
Do not make a uniform deep recess over all MAIN-C.

Use local shell geometry:
- connector bay at RJ45/USB;
- normal 2.0..2.4 mm shell elsewhere;
- no internal rib above Ag53024;
- preserve upper ventilation outlet area.

Connector bay must not weaken upper cleat nodes.

## 10. Ethernet installed-cable problem
This is now the dominant MAIN-C mechanical risk.

A straight rear-facing RJ45 cable is incompatible with a shallow wall-mounted product unless:
- a right-angle plug is mandated, or
- a recessed/side egress bay turns the cable before the wall plane.

Baseline decision:
**design the enclosure for standard cable compatibility via side/downward egress; do not require a proprietary Ethernet cable.**

A slim/right-angle cable may improve installation but shall not be the only supported cable unless explicitly productized.

## 11. External 24 V connector relationship
The external 24 V connector is on MAIN-P, not MAIN-C, but its cable exit shall share the lower/side service philosophy.

Ethernet and 24 V cable paths must not cross the radar RF cone or obstruct passive chimney flow.

## 12. Coarse Z verdict
Using the current MAIN-C Z plane:
- Ag53024 ~14 mm class: PASS coarse;
- W5500/logic: PASS;
- Ethernet magnetics: expected PASS, exact CAD open;
- USB4085 body: expected PASS, service volume open;
- RJ45 body: exact CAD open;
- RJ45 installed cable: requires recessed side/downward egress.

No evidence currently requires product depth >40 mm.

## 13. DMU checks to add
C21 RJ45 body inside product envelope.
C22 RJ45 standard plug can be inserted/removed.
C23 Ethernet cable can turn parallel to wall without violating bend/service envelope.
C24 USB-C service plug insertion path valid.
C25 Ag53024 top clearance >=1 mm to rigid shell/frame.
C26 MAIN-C connector bay does not weaken cleat load path.
C27 connector bay does not block upper thermal exhaust.
C28 Ethernet shield/metal remains outside ESP32 RF keep-out.

## 14. Exact release blockers
1. import Ag53024 manufacturer mechanical CAD/drawing;
2. import TE 2-1734264-1 exact STEP/drawing;
3. import Wurth 7490220121 exact STEP;
4. import GCT USB4085 exact STEP;
5. model a representative standard RJ45 plug + boot;
6. model Ethernet cable minimum practical bend corridor;
7. freeze RJ45 orientation on MAIN-C;
8. freeze connector-bay shell geometry;
9. rerun RF and thermal checks.

Status: **MAIN_C_18MM_REAR_ALLOWANCE / AG53024_COARSE_PASS / INSTALLED_RJ45_CABLE_EGRESS_IS_PRIMARY_MECHANICAL_GATE**.
