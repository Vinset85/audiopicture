# AudioPicture V2.2 Rev.A — master global Z map

Status: **GLOBAL_Z_DATUM_FROZEN / ALL_MAJOR_SUBSYSTEMS_REMAPPED / 40MM_NOMINAL_CLOSURE_PRESERVED / EXACT_STEP_COLLISION_GATE_OPEN**

## 1. Global datum
One product-global coordinate system is authoritative.

Z=0.0 mm:
visible outer fabric plane.

Positive Z:
toward wall.

Rear product limit:
Z=40.0 mm.

No local CAD Z value may be used directly in assembly collision checks without an explicit transform.

## 2. Front stack
FABRIC:
- outer Z = 0.0
- thickness seed = 0.5
- rear Z = 0.5.

FABRIC_DML_AIR_GAP:
- nominal = 2.8
- hard tolerance-closure minimum = 2.0.

DML:
- front Z = 3.3
- structural thickness nominal = 6.0
- rear Z = 9.3.

This supersedes historical DML Z~2..8 seed.

## 3. EX25FHE2
Conservative rear depth:
26.0 mm from DML rear/mount reference.

Envelope:
- front/mount reference Z = 9.3
- rear conservative Z = 35.3.

Preferred rigid rear clearance:
1.0 mm.

Clearance envelope ends:
Z=36.3.

Rear shell inner:
Z=37.8.

Nominal residual:
**1.5 mm**.

This is the governing product-depth region.

## 4. Rear shell
Nominal ASA:
2.2 mm.

- inner plane Z=37.8
- outer plane Z=40.0.

Thickness sweep:
2.0 / 2.2 / 2.4 mm requires automatic closure recheck.

## 5. MAIN-C remap
Retain board plane because it remains compatible with revised front datum:
- PCB front Z=17.0
- PCB rear Z=18.6.

Available rear component height to generic 1.2 mm shell-clearance plane Z36.6:
18.0 mm from PCB rear.

Ag53024 conservative body:
- reference from PCB rear
- H3 seed <=15 mm class
- conservative top <=33.6 mm.

Nominal to shell inner:
>=4.2 mm.

MAIN-C:
**GLOBAL_Z_PASS_COARSE**.

## 6. MAIN-P remap
- PCB front Z=18.0
- PCB rear Z=19.6.

Horizontal 470 uF envelope:
- rearward local envelope approximately 12 mm class
- conservative top approximately Z31.6.

Nominal shell-inner residual:
~6.2 mm.

XAL7050:
~5 mm component-height class from board surface and not Z governing.

MAIN-P:
**GLOBAL_Z_PASS_COARSE**.

## 7. VOICE remap
The old Z12.0..13.6 board seed is retained only if microphone acoustic path and carrier clearances pass.

Global nominal:
- PCB front Z=12.0
- PCB rear Z=13.6.

Distance from DML rear Z9.3 to VOICE PCB front:
**2.7 mm**.

This is less than the old informal ~4 mm statement.

Therefore old ~4 mm separation is withdrawn.

VOICE carrier/isolation must fit inside the 2.7 mm nominal inter-plane region or locally offset the PCB rearward where XY permits.

Preferred revised VOICE sweep:
- PCB front Z=12.5 / 13.0 / 13.5
- corresponding rear Z=14.1 / 14.6 / 15.1.

Mic acoustic port geometry remains coupled to front acoustic path and must not be blocked by moving the board rearward.

Status:
**VOICE_Z_SWEEP_REQUIRED / 12.0 OLD SEED NOT PRODUCTION_FROZEN**.

## 8. RADAR remap
Old PCB:
Z11.0..12.6.

Distance from DML rear:
1.7 mm at front surface.

Because radar sits in a dedicated XY region and needs controlled front radome/fabric spacing, the old seed is too close to DML for a generic carrier assumption.

Revised sweep:
- PCB front Z=12.0 / 12.5 / 13.0
- PCB rear Z=13.6 / 14.1 / 14.6.

Antenna is on front side.

Exact antenna-to-front-cover electrical distance is an EM/radome variable and is not frozen mechanically.

Status:
**RADAR_Z_SWEEP_REQUIRED / EM_MODEL_AUTHORITATIVE**.

## 9. ENV remap
Old:
Z12.0..13.6.

Retain as first seed:
- front Z12.0
- rear Z13.6.

SHT45:
uses separate room-air chamber; PCB Z may be locally adjusted to support thermally weak mounting.

OPT3004:
an unobstructed front optical path is a requirement, not a verified result.
Rev.EZ geometric audit finds the entire ENV seed X252..294/Y35..59 behind
the DML hard volume Z3.3..9.3. All 25 normal rays intersect 6 mm of that
volume; a Z-only sweep does not remove it. A defined perimeter/front optical
path or light-sensor relocation must be verified before placement release.
This audit does not assign an optical transmittance to the unqualified DML stack.

Revised sweep:
- PCB front Z12.0 / 12.5 / 13.0
- rear Z13.6 / 14.1 / 14.6.

Status:
**ENV_Z_SWEEP_REQUIRED / SENSOR_PATHS_AUTHORITATIVE**.

## 10. PC-CF structural frame transform
The real frame B-rep has local structural depth 8 mm.

Do not place it globally as a uniform 8 mm slab.

The frame is a sparse topology around subsystem keep-outs.

Define nominal structural Z band:
**Z=27.0..35.0 mm**
for generic perimeter/rail portions where legal.

Exceptions:
- cleat/boss nodes may use dedicated rear geometry;
- bridges are clipped around tall components;
- no frame in EX25 full-depth columns;
- radar forward region remains PC-CF-free;
- VOICE isolation remains independent.

This placement uses the rear structural half of the enclosure while preserving electronics/front sensing volumes.

Exact frame transform must be applied to the real B-rep before final collision release.

## 11. Wall cleats
Metal cleats are rear-side mount hardware and must remain compatible with:
- rear shell openings/recesses;
- 4 mm wall gap;
- ESP32/radar RF exclusions.

Cleat structural interfaces attach to PC-CF upper nodes.

Their exact global Z is derived from final rear-shell/wall-interface CAD, not assigned as a free floating plate.

No full-width metal at rear.

## 12. RJ45
RJ45 remains on MAIN-C.

Electrical connector body follows MAIN-C Z.

Mating direction:
downward in Y.

Cable tunnel:
nominal Z corridor **22..36 mm** where XY permits.

This remains compatible with shell inner Z37.8, but plug/boot exact STEP is required.

No rearward plug egress baseline.

## 13. JCP / JCS / FPC
JCP power harness:
rearward routing corridor nominal:
Z20..26.

JCS/FPC signal:
nominal:
Z14..18.

After global remap:
- FPC corridor starts above DML rear Z9.3 with >4 mm nominal separation;
- power corridor remains below rear structural/shell region.

These are corridors, not solid full-area layers.

## 14. Speaker harness
Nominal:
Z20..28.

Route directly MAIN-P to exciters.

At each exciter:
transition locally to terminal/service region without entering rigid rear-clearance envelope.

No loose wire may occupy the final 1.5 mm exciter-to-shell residual zone.

## 15. Ethernet cable tunnel
Nominal:
Z22..36.

At the worst exciter regions the tunnel is excluded entirely.

Cable bend/boot is an XY/Z swept solid, not a line.

Final conventional molded boot remains a mechanical gate.

## 16. Ventilation domain
Rear airflow uses remaining connected free volume around:
- PC-CF frame;
- boards;
- harnesses;
- cable tunnel.

Nominal chimney is not assigned one uniform Z thickness.

CFD uses actual remapped solids.

## 17. Front carrier global transform
Carrier local B-rep:
base 1.8 mm, local magnet station 3.2 mm.

Global placement is constrained by fabric seating and DML clearance.

The carrier occupies perimeter-only volume behind fabric.

No central carrier slab exists.

Magnet station pads must be reshaped/moved so their rear intrusion does not enter DML hard region.

Until redesigned:
**FRONT_CARRIER_GLOBAL_TRANSFORM_PARTIALLY_BLOCKED_BY_MAGNET_PAD_GATE**.

## 18. Magnetic station Rev.B seed
Use:
M1B (70,388)
M2B (250,388)
M3B (70,12)
M4B (250,12)
M5B (12,135)
M6B (12,275)
M7B (308,135)
M8B (308,315).

Station pad becomes D-shaped/perimeter-biased.

DML-facing pad edge shall remain outside DML hard-clearance projection.

## 19. Global Z occupancy summary
FRONT FABRIC:
0.0..0.5

AIR GAP:
0.5..3.3 nominal

DML:
3.3..9.3

VOICE/RADAR/ENV:
~12.0..15.1 sweep class

FPC:
14..18 corridors

MAIN-C:
17.0..18.6 PCB + rear components

MAIN-P:
18.0..19.6 PCB + rear components

POWER HARNESS:
20..26 corridors

SPEAKER HARNESS:
20..28 corridors

RJ45/ETH TUNNEL:
22..36 local corridor

PC-CF FRAME:
~27..35 sparse legal regions

EXCITERS:
9.3..35.3 hard columns

EXCITER CLEARANCE:
35.3..36.3

GENERIC RIGID LIMIT:
~36.6

REAR SHELL INNER:
37.8

REAR SHELL:
37.8..40.0.

## 20. No-layer interpretation
The summary above is not a set of full-area stacked plates.

Most regions are sparse and overlap in Z because they are separated in XY.

The design remains a 2.5D packaging architecture.

## 21. Clearance classes
HARD:
- exciter columns;
- DML active clearance;
- radar RF cone;
- shell outer envelope.

SERVICE:
- RJ45 plug/latch;
- USB;
- harness bend/removal.

SOFT:
- airflow volumes;
- compliant pads;
- cable dressing where controlled.

Collision checker must report classes separately.

## 22. Updated depth risk
The governing Z risk is now:
**EX25FHE2 + front acoustic gap + DML thickness**.

Not:
- MAIN-P capacitor;
- Ag53024;
- PCB thickness.

Therefore any future depth optimization should first target:
- front fabric gap tolerance;
- DML structural thickness if acoustically/structurally permissible;
- exciter mounting reference/actual STEP.

Do not thin rear shell below structural/process needs merely to hide an unresolved exciter stack.

## 23. Automatic checks
C401 one global Z datum used.
C402 historical DML 2..8 seed retired.
C403 DML global 3.3..9.3 nominal.
C404 exciter conservative rear <=35.3 nominal.
C405 exciter clearance envelope <=36.3.
C406 shell inner 37.8 nominal.
C407 shell outer <=40.
C408 exciter nominal residual >=1.5.
C409 MAIN-C coarse rear clearance positive.
C410 MAIN-P coarse rear clearance positive.
C411 VOICE old 4 mm separation statement retired.
C412 VOICE Z sweep defined.
C413 RADAR Z sweep defined.
C414 ENV Z sweep defined.
C415 frame generic structural band 27..35 only where XY legal.
C416 no frame in exciter columns.
C417 no PC-CF in radar forward region.
C418 FPC corridor globally remapped.
C419 power harness globally remapped.
C420 speaker harness globally remapped.
C421 RJ45 tunnel globally remapped.
C422 no cable in final exciter rear-clearance zone.
C423 front carrier local/global transform explicit.
C424 magnetic Rev.B centers adopted as next CAD seed.
C425 no full-area interpretation of overlapping Z corridors.
C426 hard/service/soft collision classes defined.
C427 exact STEP collision remains required.
C428 rear shell thickness sweep triggers closure rebuild.
C429 VOICE/RADAR/ENV Z choice cannot be frozen without functional validation.
C430 future depth optimization prioritizes governing exciter/front-stack chain.

## 24. State
Global Z architecture is now coherent.

Nominal product depth:
**40.0 mm**

Governing residual:
**~1.5 mm behind conservative EX25FHE2 clearance envelope**

Major electronics:
coarse PASS.

Open:
- exact EX25 STEP;
- exact tall-component STEP;
- VOICE/RADAR/ENV functional Z optimization;
- front magnet-pad redesign;
- real transformed full-assembly collision solve.

Status:
**GLOBAL_Z_MAP_FROZEN / DML_3P3_TO_9P3 / EXCITER_TO_35P3 / SHELL_INNER_37P8 / 1P5MM_GOVERNING_MARGIN / C01_TO_C430**.

## 25. Verified optical relocation candidate — Rev.FA, 2026-10-06

The Rev.EZ geometric audit rejects an unobstructed normal optical path from
the existing ENV seed behind the DML. Changing its Z from 12 to 13 cannot
resolve that overlap. The separately tested Rev.FA candidate reserves only
the light-sensor island at X311.3..316.5/Y43..51/Z3.35..4.15, with the OPT3004
maximum body extending forward to Z2.70. It does not change the DML hard
projection or its Z3.3..9.3 band, nor the SHT45 region.

The front carrier uses the later Rev.F +0.5 global Z transform and Rev.D
station centers. Its new 6.6 x 8.4 mm opening passes a conservative +/-35-degree
cone from the whole maximum sensor projection. Full mounting/interconnect,
PCB, tolerances, light sealing and fabric calibration remain OPEN; these
candidate coordinates are not a fabrication freeze. See
`optical-perimeter-candidate-rev-fa.md` and `../evidence/rev-fa/execution.json`.

A hypothetical ASA right wall beginning at Z0.5 intersects the removable
carrier. The optical study therefore reserves a rearward wall starting at
Z4.1; the enclosure wall/front joint itself is still unbuilt. Do not treat
that clearance reservation as closure of the complete enclosure or CFD domain.
