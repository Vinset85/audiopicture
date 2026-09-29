# AudioPicture V2.2 Rev.A — internal harness and FPC routing

Status: **INTERNAL_ROUTING_CORRIDORS_DEFINED / EXACT_CONNECTOR_ORIENTATION_BEND_RADIUS_AND_EMC_RELEASE_GATE**

## 1. Purpose
Define three-dimensional routing corridors for:
- MAIN-C <-> MAIN-P power;
- MAIN-C <-> MAIN-P digital signals;
- VOICE FPC;
- RADAR FPC;
- ENV FPC;
- DML speaker harnesses;
- Ethernet connection-bay path;
- external 24 V connection-bay path;
- USB-C service path.

Routing is treated as swept volume, not a zero-width centerline.

## 2. Z routing layers
Define first-order harness layers.

### SIGNAL/FPC layer
Preferred:
**Z = 14..18 mm**

Used for:
- JCS;
- VOICE;
- RADAR;
- ENV low-power FPC.

### POWER/HARNESS layer
Preferred:
**Z = 20..26 mm**

Used for:
- JCP;
- 24 V internal wiring where required;
- Ethernet/USB remote service harness only if architecture requires it.

### SPEAKER layer
Preferred:
**Z = 20..28 mm**
in local corridors from MAIN-P to exciter terminal regions.

No cable may cross an exciter rear cap inside its Z=35 exclusion column.

## 3. MAIN-C to MAIN-P — JCS
Existing:
- 16-position Hirose FH12 FPC interface;
- seed developed length 220 mm.

Route:
- depart MAIN-C from lower/central edge;
- descend through central-left signal corridor;
- enter MAIN-P from upper P1/P2 edge.

Preferred product corridor:
- X approximately 145..170 mm where geometry permits;
- avoid L2 exciter box X83..145/Y166..226;
- avoid R1 X175..237/Y238..298.

The narrow corridor between L2 and R1 is intentional.

JCS remains in SIGNAL/FPC Z layer.

Do not route parallel immediately adjacent to speaker BTL wiring for long distances.

## 4. MAIN-C to MAIN-P — JCP
Existing:
- Micro-Fit 4-circuit power interconnect;
- seed harness 230 mm;
- two contacts +24V_POE_ISO;
- two contacts GND.

Route near but not bundled tightly with JCS.

Preferred corridor:
- X approximately 155..180 mm;
- POWER layer Z20..26.

Where JCP and JCS run near each other:
- maintain physical separation where possible;
- cross noisy/high-current routes at near 90 degrees if crossing is unavoidable.

## 5. VOICE FPC
VOICE board:
- X119..201/Y20..102.

Route from VOICE upper/right edge toward the central JCS corridor, then upward to MAIN-C.

Preferred:
- X approximately 200..220 from Y100 upward until clear of MAIN-P;
- then shift inward through free corridor.

Do not route across microphone acoustic channels.

Keep away from:
- MAIN-P switching node regions;
- TAS5825M output inductors;
- speaker harnesses.

## 6. RADAR FPC
RADAR:
- X249..287/Y184..216.

Route upward along right-side corridor toward MAIN-C.

Preferred:
- X approximately 285..298 where protected-perimeter/frame geometry permits;
- otherwise immediately inboard of the right structural rail.

FPC/copper shall not enter the radar forward RF cone.

Keep radar digital FPC separated from DML speaker harnesses.

## 7. ENV FPC
ENV:
- X252..294/Y35..59.

Route upward along right side but keep independent of:
- SHT45 room-air chamber openings;
- radar forward RF cone;
- hot exhaust;
- right exciter columns.

A staged path may run:
- upward from ENV to below R2;
- inward/around R2 exclusion;
- then upward through right-side free corridor.

Exact swept route waits shared CAD.

## 8. Speaker harness
TAS5825M and output LC remain on MAIN-P.

Do not move BTL output through MAIN-C.

Two channel harnesses:
- LEFT -> L1/L2 series branch;
- RIGHT -> R1/R2 series branch.

Each channel is a twisted pair after the final LC/output network where electrically appropriate.

Route speaker wires:
- short;
- close-coupled;
- away from microphones/FPC;
- away from radar;
- away from ESP32 antenna.

Series inter-exciter jumpers remain local to their channel side where possible.

No speaker wire runs across the center of the VOICE mic array.

## 9. Connection bay Ethernet
Preferred architecture:
RJ45 remains electrically on MAIN-C.

Because MAIN-C is upper and bay is lower, do not extend raw Ethernet MDI over a long internal harness.

Therefore baseline:
**do not remote the RJ45 through unqualified cable from MAIN-C.**

Instead the mechanical architecture shall provide either:
A. a vertical internal connector-access channel allowing the MAIN-C RJ45 to face a side/bottom cable path; or
B. reposition/orient MAIN-C/RJ45 within the board outline so the external cable reaches it through a molded cable tunnel.

Raw MDI remote daughterboard is not baseline.

This may require revising the connection-bay exact X/Y geometry after shared CAD.

## 10. Connection bay USB-C
USB is service-only.

Preferred:
- USB4085 remains on MAIN-C;
- shell provides a service tunnel/access path.

Do not create an unnecessary internal USB extension unless direct mechanical access proves impossible.

If an extension becomes necessary:
- preserve USB 2.0 differential impedance;
- ESD protection location must be re-reviewed;
- shield/ground strategy must be explicit.

## 11. Connection bay 24 V
24 V belongs to MAIN-P and is electrically less sensitive to a short internal harness than Ethernet MDI.

Preferred if direct board-edge access is impossible:
- short two-wire harness from bay connector to MAIN-P protected input;
- keyed locking connector;
- adequate wire gauge;
- strain relief at bay;
- fuse/protection location remains electrically close enough to input to protect downstream wiring as intended.

However, if the bay connector is panel-mounted ahead of PCB protection, the internal lead itself must be considered unprotected and routed/insulated accordingly.

Preferred production solution is to minimize unprotected wire length.

## 12. Thermal chimney preservation
Create a no-bundle vertical airflow zone through the main rear chimney.

No harness may form a full-width horizontal curtain.

Use:
- side clips;
- narrow vertical bundles;
- local perforated supports.

Target:
**no cable bundle occupies more than 20 percent of local chimney cross-section** without CFD re-analysis.

## 13. Harness fixation
Provide printed clips/guides on PC-CF/ASA carriers.

Rules:
- no loose cable touching DML;
- no loose cable touching exciter moving/mechanical structures;
- no cable rubbing sharp PCB/shell edges;
- no adhesive-only primary retention;
- serviceable where practical.

Use compliant anti-rattle contact where a cable passes close to shell/frame.

## 14. EMC segregation
Classify:
A. HIGH-DI/DT:
- TAS5825M BTL/output region;
- switching regulator local loops.

B. POWER:
- 24 V;
- JCP.

C. DIGITAL:
- I2S/I2C/control FPC.

D. SENSITIVE:
- VOICE/mic;
- radar;
- ENV.

Rules:
- A kept local to MAIN-P;
- B separated from D where practical;
- C may share corridor with controlled spacing;
- D avoids A;
- unavoidable crossings approximately orthogonal.

## 15. Bend/service rules
Every FPC/harness CAD object shall include:
- connector mating volume;
- straight exit length;
- minimum bend radius;
- dynamic assembly bend path where applicable;
- clip/retention envelope.

Do not freeze bend radius generically. Use the selected cable/FPC vendor construction.

## 16. DMU checks
Add:
C41 JCS swept volume clears exciters/frame.
C42 JCP swept volume clears exciters/frame.
C43 VOICE FPC clears acoustic channels and MAIN-P noisy zone.
C44 RADAR FPC stays outside RF cone.
C45 ENV FPC does not obstruct SHT45 air chamber.
C46 speaker harness avoids VOICE array/RF zones.
C47 no cable enters exciter mechanical clearance.
C48 no harness creates full-width chimney obstruction.
C49 all harnesses have positive retention.
C50 all FPC bend radii meet selected cable specification.
C51 RJ45 remains electrically local to Ethernet magnetics/MAIN-C.
C52 any unprotected 24 V internal lead is minimized and mechanically protected.
C53 USB service path preserves signal/ESD architecture.
C54 installed cables cannot contact DML during vibration.

## 17. Architecture consequence
The initial connection-bay concept remains valid as a mechanical service zone, but **Ethernet shall not be casually remote-connected from MAIN-C to that bay**.

Shared CAD must now solve the physical tunnel between MAIN-C RJ45 and external cable egress.

If this cannot be achieved cleanly, preferred redesign order is:
1. rotate/reposition RJ45 on MAIN-C;
2. adjust MAIN-C outline/placement;
3. adjust bay geometry;
4. only then consider an Ethernet connector daughterboard with a fully requalified MDI path.

## 18. Release gates
1. freeze connector orientation on all PCBs;
2. select actual FPC constructions;
3. generate swept cable solids;
4. solve RJ45 direct-access tunnel;
5. solve 24 V protected/unprotected boundary;
6. route speaker harness in shared CAD;
7. rerun C01..C54;
8. EMC review;
9. CFD with installed harnesses;
10. vibration/buzz-rattle review.

Status: **FPC_Z14_18 / POWER_Z20_26 / SPEAKER_Z20_28 / RAW_ETHERNET_MDI_REMOTE_HARNESS_PROHIBITED_BASELINE**.
