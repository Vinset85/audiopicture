# AudioPicture V2.2 Rev.A — Component envelope audit

Status: **CRITICAL_ENVELOPE_AUDIT_STARTED / EXACT_3D_IMPORTS_AND_OPEN_MPNS_REMAIN**

## 1. Classification
Every mechanical component model shall be tagged:
- VERIFIED_STEP — manufacturer or authorized-source 3D model matched to exact MPN;
- VERIFIED_DRAWING — exact manufacturer mechanical drawing is authoritative;
- DERIVED_ENVELOPE — conservative solid built from a verified drawing;
- PLACEHOLDER — not allowed for final collision release.

## 2. DML exciters
### Legacy DAEX25FHE-4
State: VERIFIED_DRAWING / DERIVED_ENVELOPE permitted.

Known project baseline:
- nominal body diameter approximately 50.5 mm;
- overall rear projection approximately 20.5 mm;
- mass 110.9 g.

CAD rule:
- retain current conservative radial keep-out R=30 mm until exact terminal/wire egress is included;
- retain >=23 mm rearward keep-out from DML rear mounting plane;
- model adhesive/contact footprint separately from body envelope.

### Successor EX25FHE2-4
State: EXACT DRAWING/3D IMPORT REQUIRED.

It is a lifecycle/mechanical variant and shall not inherit the legacy DAEX25FHE-4 envelope. Production placement cannot freeze until the successor mechanical model is compared.

## 3. External 24 V connector
Selected engineering baseline:
- PCB header Molex 43650-0200;
- mating housing Molex 43645-0200;
- Micro-Fit 3.0 family.

State: VERIFIED_MPN / EXACT MANUFACTURER DRAWING OR STEP IMPORT REQUIRED.

Collision model must include:
- PCB header body;
- board-lock/THT tails;
- mating plug;
- wire exit;
- bend/strain-relief service volume.

The external mating/service envelope is as important as the PCB body envelope.

## 4. USB-C service connector
Selected baseline:
- GCT USB4085.

State: VERIFIED_MPN / EXACT MANUFACTURER CAD-DRAWING IMPORT REQUIRED.

Model:
- receptacle shell;
- through-hole retention features;
- PCB thickness relationship;
- external USB-C plug insertion volume;
- finger/service access.

## 5. Ethernet connector and magnetics
Selected PCB-side baseline includes:
- TE 2-1734264-1;
- Würth 7490220121 magnetics.

State: VERIFIED_MPN / EXACT CAD IMPORT REQUIRED.

The enclosure model shall treat RJ45 plug insertion and cable bend as an external service envelope. Shield tabs/THT tails must be included in PCB keep-outs.

## 6. PoE module
Selected:
- Ag53024.

State: VERIFIED_MPN / MANUFACTURER MECHANICAL DRAWING/3D IMPORT REQUIRED.

This is a critical MAIN height/thermal envelope. Do not use the obsolete Ag5324 mechanical assumption.

Record exact:
- L/W/H;
- pin projection;
- keep-out/creepage needs;
- orientation;
- thermal clearance.

## 7. TAS5825M
Selected:
- TAS5825MRHBR;
- RHB VQFN-32, 5 x 5 mm class package.

State: PACKAGE ENVELOPE VERIFIED; mechanically non-critical alone.

The dominant audio-board mechanical items are instead:
- four 10 uH output inductors;
- PVDD bulk capacitor;
- local high-voltage MLCC stack;
- speaker harness connector/egress.

Exact output-inductor MPN is still OPEN and therefore its mechanical envelope is PLACEHOLDER only.

## 8. PVDD bulk capacitor
Electrical baseline:
- 470 uF / 35 V low-ESR.

State: EXACT MPN OPEN -> PLACEHOLDER.

Mechanical CAD shall reserve a conservative capacitor cylinder/box until MPN freeze. This part is a likely height driver and must be selected jointly for ESR/ripple/current/lifetime and enclosure height.

## 9. 5 V / power-stage components
Known high-interest parts:
- TPSM63603V5RDHR;
- C5VIN 1210 ceramics;
- protection MOSFETs;
- fuse/TVS;
- INA228 shunt.

Most ICs/passives are low-profile; however exact inductor/module, connector and PoE heights shall be imported into the MAIN height map.

## 10. Daughterboard FPC connectors
Selected:
- J101 FH12-16S-0.5SH(55);
- J201 FH12-12S-0.5SH(55);
- J301 FH12-8S-0.5SH(55).

State: VERIFIED_MPN / exact Hirose mechanical models required.

Model both connector body and minimum practical FPC bend/service volume.

## 11. MAIN height-map rule
Before board outline freeze, classify every MAIN component into height bands measured from PCB component-side surface:
- H0: <=2 mm;
- H1: >2..5 mm;
- H2: >5..10 mm;
- H3: >10..15 mm;
- H4: >15 mm.

No H3/H4 part may be placed under an exciter rear keep-out unless the local Z-stack proves clearance.

The PCB itself and solder/lead protrusion on the opposite side shall be included.

## 12. Required source register
For each critical imported model record:
- exact MPN;
- manufacturer;
- source document/CAD URL;
- document revision/date if available;
- nominal critical dimensions;
- CAD filename;
- import transform into master CAD;
- audit state.

Do not treat aggregator-generated CAD as authoritative without dimensional cross-check to the manufacturer drawing.

## 13. Immediate open mechanical decisions
The following now block exact enclosure collision release:
1. EX25FHE2-4 exact mechanical model;
2. Ag53024 exact L/W/H model;
3. exact 10 uH TAS5825M output inductor MPN;
4. exact 470 uF / 35 V bulk capacitor MPN;
5. exact RJ45/24 V/USB-C/FPC CAD import and plug-service envelopes;
6. final MAIN PCB placement/outline.

## 14. Release rule
The first detailed rear-frame solid may be generated with DERIVED_ENVELOPE objects, but production mechanical release requires all collision-critical components to be VERIFIED_STEP or VERIFIED_DRAWING/DERIVED_ENVELOPE and matched to the BOM.
