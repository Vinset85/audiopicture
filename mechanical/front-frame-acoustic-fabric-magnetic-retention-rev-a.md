# AudioPicture V2.2 Rev.A — removable front frame, acoustic fabric and magnetic retention

Status: **FRONT_FRAME_ARCHITECTURE_FROZEN / MAGNET_FORCE_REQUIREMENT_DEFINED / EXACT_MAGNET_MPN_AND_FABRIC_ACOUSTIC_DATA_OPEN**

## 1. Purpose
Define the removable cosmetic/acoustic front frame covering the complete 320 x 400 mm product front.

Requirements:
- printed acoustic fabric hides DML, microphones and sensors;
- no visible front screws;
- removable without damaging fabric or DML;
- stable against gravity, handling and DML vibration;
- does not interfere materially with radar, ESP32 or microphones;
- remains inside 40 mm product depth.

## 2. Front datum and Z stack
Product front:
Z=0.

Seed stack:
- fabric outer surface: Z=0..0.6 mm class
- front carrier/frame: primarily Z=0.6..1.8 mm local
- controlled air gap behind fabric before DML/front sensing surfaces
- DML front structural region begins behind front system per master Z stack.

Front-frame maximum rear intrusion is parametrically limited by DML/sensor keep-outs.

## 3. Frame material
Preferred:
unfilled ASA or equivalent nonconductive printable polymer.

Do not use PC-CF as continuous front perimeter near RF/sensing zones unless EM validation proves acceptable.

Reasons:
- cosmetic finish;
- RF transparency relative to carbon-filled polymer;
- lower risk of conductive/carbon interference.

## 4. Frame topology
Use thin perimeter carrier plus sparse local cross-support only where required for fabric tension.

No broad central grille directly over DML.

Nominal perimeter width:
8..12 mm.

Nominal carrier thickness:
1.6..2.2 mm depending local geometry.

Internal fabric support features:
- narrow;
- rounded;
- acoustically sparse;
- outside microphone acoustic ports where possible.

## 5. Fabric attachment
Preferred production concept:
fabric wraps around rear side of removable front carrier and is retained by controlled adhesive/bonding land.

Provide:
- continuous rear bonding land;
- corner relief;
- controlled stretch datum;
- trim allowance hidden on rear.

Do not bond fabric directly to DML.

Front frame must be replaceable as a complete service part.

## 6. Fabric tension
Tension shall be sufficient to:
- prevent visible sag;
- avoid contact with DML during vibration;
- avoid buzz/rattle.

But excessive tension shall not:
- warp the printed carrier;
- distort printed artwork;
- preload microphone/sensor regions.

Final tension is process-qualified using the selected fabric.

## 7. Fabric-to-DML clearance
Seed minimum static gap:
**2.0 mm**

Preferred nominal:
**2.5..3.0 mm**

Check under:
- fabric sag;
- frame warp;
- DML peak displacement;
- handling pressure;
- tolerance stack.

No normal operating condition may allow fabric to touch the active DML panel.

## 8. Acoustic transparency
Selected printed fabric requires measured:
- insertion loss 100 Hz..20 kHz;
- phase impact;
- high-frequency attenuation;
- angular response;
- effect of printing ink coverage;
- microphone attenuation;
- radar attenuation/phase impact where radar lies behind fabric.

Do not assume an unprinted-fabric datasheet remains valid after printing.

## 9. Microphone regions
Four microphone acoustic paths remain unobstructed by hard frame members.

Fabric is allowed over microphone apertures only after acoustic characterization.

No adhesive land directly over microphone acoustic ports.

No rigid carrier crossbar directly in front of a mic port.

## 10. Radar region
Radar is hidden behind fabric/front polymer.

In radar forward cone:
- no magnet;
- no steel target;
- no PC-CF;
- no metallic decorative element;
- no dense carrier rib.

Fabric print ink/pigment must be checked for RF impact if metallic/conductive pigments are used.

Metallic-effect inks are prohibited baseline until tested.

## 11. Ambient-light region
OPT3004 optical path requires:
- defined fabric optical transmission;
- no opaque frame rib;
- no adhesive;
- calibration with final printed artwork.

Artwork may require a controlled optical window pattern invisible to normal viewing.

## 12. Magnetic retention architecture
Use distributed small magnets/targets around the perimeter, outside RF keep-outs.

Do not use a continuous steel ring.

Reasons:
- RF;
- mass;
- uncontrolled magnetic field;
- acoustic/vibration behavior.

Magnet pockets are parametric and replaceable before production freeze.

## 13. Front-frame mass budget
Initial front-frame assembly budget:
- polymer carrier: 35..60 g
- fabric/print/adhesive: 15..30 g
- magnets/targets: 10..25 g

Working mass:
**60..115 g**

Design target:
**<=120 g**

This is a subsystem budget, not measured final mass.

## 14. Required retention force
Gravity of 120 g frame:
~1.18 N.

Gravity alone is not governing.

Define design cases:
MR1 gravity: 1.2 N
MR2 handling/peel disturbance: 10 N
MR3 vibration/inertial retention: 15 N equivalent distributed
MR4 deliberate removal pull: target user-removable
MR5 corner peel: 8 N local seed.

Target total normal retention:
**20..30 N assembled**

Target:
- secure in normal operation;
- removable by hand using defined edge/release feature;
- no tool required for normal front-frame removal.

Exact force is validated on assembled magnetic circuit, not magnet free-air datasheet force.

## 15. Magnet count seed
Initial:
**8 magnetic stations**

Candidate distribution:
- top: 2
- bottom: 2
- left: 2
- right: 2.

Avoid:
- radar zone;
- ESP32 RF zone;
- mic ports;
- optical path;
- service/removal feature.

Alternative 6/10-station layouts remain parametric.

## 16. Per-station force
For 8 stations and 20..30 N total assembled retention:
nominal assembled contribution:
**2.5..3.75 N per station average**.

Do not select magnets solely from nominal direct-contact pull-force ratings.

Account for:
- air/polymer gap;
- target thickness;
- lateral offset;
- pocket tolerance;
- adhesive;
- temperature;
- magnet grade;
- peel geometry.

## 17. Magnet circuit options
Preferred options to evaluate:
A. magnet in front frame + discrete steel target on non-RF structural region;
B. magnet in rear/product frame + discrete steel target in front frame.

Avoid magnet-to-magnet baseline unless required because polarity/orientation and assembly complexity increase.

Target steel pieces are local, not continuous.

## 18. Magnetic station pocket
Parametric pocket variables:
MAG_D
MAG_T
MAG_GAP
TARGET_T
TARGET_XY.

Pocket includes:
- positive mechanical capture;
- adhesive secondary retention;
- anti-rattle preload.

A magnet must not be retained by adhesive alone if release could allow it to contact electronics/DML.

## 19. Removal feature
Provide hidden finger/release feature on lower or side edge.

No visible front tab.

Removal sequence:
1. engage hidden edge relief;
2. initiate local peel;
3. sequentially release magnetic stations;
4. lift front frame without touching DML.

Corner peel force shall be lower than unsafe fabric/carrier deformation.

## 20. Anti-rattle interface
Use sparse compliant perimeter pads where needed.

Pads:
- prevent hard plastic buzz;
- define front-frame seating plane;
- avoid overconstraining warped printed parts.

Do not create continuous thick foam seal unless acoustic/thermal impact is intended.

## 21. Registration
Use non-load-bearing geometric locators:
- two datum features control X/Y;
- magnetic stations provide normal retention;
- locators prevent lateral creep.

Locators must not require high insertion force.

## 22. Artwork registration
Define printable artwork datum from front-frame CAD:
- centerline X=160;
- centerline Y=200;
- trim/bleed region hidden on rear wrap.

Printing process must control:
- scale;
- rotation;
- stretch;
- color;
- optical sensor local transmission.

## 23. Serviceability
Front frame is a replaceable FRU.

No need to remove wall mount for:
- front-frame replacement;
- fabric replacement as complete front assembly;
- visual inspection of DML/front sensing system.

Individual fabric rewrapping may be workshop service, not end-user service.

## 24. Preliminary magnetic layout exclusions
Create exclusion masks:
MAG_KO_RADAR
MAG_KO_ESP32
MAG_KO_MIC_1..4
MAG_KO_OPTICAL
MAG_KO_DML_EDGE_SERVICE.

Automatic placement searches only legal perimeter arcs.

## 25. Acoustic validation cases
A0 no fabric reference.
A1 selected unprinted fabric.
A2 printed fabric average artwork.
A3 worst ink-coverage region.
A4 full front-frame assembly.

Measure:
- SPL delta;
- frequency-response delta;
- microphone transfer;
- buzz/rattle;
- DML/fabric contact.

## 26. Radar validation cases
R0 no front cover.
R1 carrier only.
R2 unprinted fabric.
R3 printed fabric.
R4 full magnetic front assembly.

Measure presence/range/false detection impact.

## 27. Tolerance seeds
Front carrier dimensional tolerance seed:
+/-0.30 mm after process calibration.

Magnet pocket:
process-compensated coupon required.

Seating-plane compliance:
designed to absorb small print warp without visible front distortion.

Fabric-DML minimum clearance remains hard requirement after worst-case tolerance.

## 28. Automatic checks
C291 front frame mass budget <=120 g.
C292 fabric not bonded to DML.
C293 fabric-DML static gap >=2.0 mm.
C294 nominal fabric-DML gap 2.5..3.0 mm target.
C295 no hard carrier member blocks microphone port.
C296 no magnet in radar RF keep-out.
C297 no steel target in radar RF keep-out.
C298 no PC-CF front member in radar cone baseline.
C299 no magnet/steel in ESP32 RF keep-out.
C300 no adhesive over microphone port.
C301 optical sensor path clear.
C302 printed-fabric optical calibration required.
C303 metallic/conductive ink prohibited baseline.
C304 total retention target 20..30 N.
C305 eight-station seed supports per-station 2.5..3.75 N assembled target.
C306 magnetic pull rating not used as assembled-force proof.
C307 magnet mechanically captured.
C308 front frame removable without tools.
C309 hidden peel/release feature exists.
C310 X/Y locators separate from magnetic normal retention.
C311 anti-rattle pads do not form unintended continuous seal.
C312 artwork datum defined.
C313 front assembly acoustic A0..A4 validation defined.
C314 radar R0..R4 validation defined.
C315 exact magnet/target MPN remains open until assembled-force/RF validation.
C316 worst-case tolerance preserves fabric-DML clearance.
C317 front frame remains within product Z envelope.
C318 front frame is replaceable FRU.
C319 magnet station count remains parametrically 6/8/10 capable.
C320 no continuous steel perimeter ring.

## 29. State
Front-frame architecture:
**FROZEN**

Baseline:
- unfilled polymer carrier;
- printed acoustic fabric;
- 2.5..3.0 mm nominal fabric-to-DML gap;
- <=120 g subsystem target;
- 8 distributed magnetic stations;
- 20..30 N assembled normal retention target;
- hidden peel feature;
- no continuous steel ring;
- RF/mic/optical exclusion masks.

Open gates:
- exact fabric;
- print process;
- measured acoustic loss;
- exact magnet/target MPN;
- assembled magnetic-force test;
- RF/radar validation;
- final artwork optical calibration.

Status: **FRONT_FRAME_8_STATION_MAGNETIC_SEED / 20_TO_30N_RETENTION / FABRIC_GAP_2P5_TO_3P0MM / C01_TO_C320 / COMPONENT_SELECTION_AND_VALIDATION_OPEN**.
