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


## 15. Connector-envelope verification pass — 2026-09-29

### Molex 43650-0200
Authoritative manufacturer drawing family is available for Micro-Fit 3.0 right-angle PCB headers. The master CAD shall use the exact 2-circuit 43650-0200 drawing/3D model and include PCB-lock/THT geometry plus the 43645-0200 mating housing and wire-service envelope.

Audit state: **VERIFIED_MPN / MANUFACTURER_CAD_FAMILY_AVAILABLE / IMPORT_PENDING**.

### GCT USB4085
GCT publishes the USB4085 product with mechanical drawing and 3D-model access. The part is a USB Type-C receptacle with through-hole shell/retention features.

Audit state: **VERIFIED_MPN / MANUFACTURER_DRAWING_AND_3D_AVAILABLE / IMPORT_PENDING**.

### Coilcraft XAL7050-103MEC
Coilcraft publishes the exact XAL7050-103 mechanical data and 3D model.
For enclosure pre-CAD reserve a conservative body envelope:
- X approximately 8.0 mm;
- Y approximately 7.7 mm;
- Z 5.5 mm conservative until imported model is cross-checked.

Audit state: **VERIFIED_MPN / MANUFACTURER_3D_AVAILABLE / DERIVED_ENVELOPE_ACTIVE**.

### Panasonic EEU-FR1V471B
Use conservative collision envelope:
- nominal can diameter 10 mm;
- nominal body height 16 mm;
- seated/max collision allowance 17.5 mm pending exact lead-form reconciliation;
- local CAD pocket remains 12 x 12 x 19 mm.

Audit state: **VERIFIED_MPN / DERIVED_ENVELOPE_ACTIVE**.

### Remaining blockers
The exact mechanical source/model remains mandatory before full collision release for:
- EX25FHE2-4;
- Ag53024;
- TE 2-1734264-1 / exact RJ45 interface geometry;
- Würth 7490220121;
- Hirose FH12 service/bend envelopes.

The CAD release rule is unchanged: a manufacturer drawing-derived conservative solid is acceptable where no trustworthy native STEP is available.

Status: **CONNECTOR_AND_AUDIO_ENVELOPES_PARTIALLY_VERIFIED / EXCITER_POE_ETHERNET_ENVELOPES_REMAIN**.


## 16. EX25FHE2-4 successor mechanical closure — critical architecture impact

Dayton Audio Engineering Change Document dated 2024-02-20 confirms the successor geometry differs materially from DAEX25FHE-4.

### Legacy DAEX25FHE-4
- nominal main diameter: 50.5 mm;
- overall framed width envelope: approximately 58.3 x 56 mm including mounting structure;
- rear depth: 20.5 +/-0.5 mm;
- net mass: 110.9 g;
- Fs approximately 224 Hz.

### Successor EX25FHE2-4
Manufacturer change drawing gives approximately:
- framed outer envelope: 58.3 +/-0.5 x 56 +/-0.3 mm;
- rear depth: **25.5 +/-0.5 mm**;
- voice-coil diameter: 25 mm;
- Re 4.3 ohm;
- Le 0.10 mH;
- RMS power 24 W;
- Fs approximately **115 Hz**.
Current distributor data lists mass approximately 113 g.

### Mechanical consequence
The successor is about 5 mm deeper than the legacy reference. Therefore the previous >=23 mm rearward exciter keep-out is superseded for successor studies.

Use preliminary successor envelope:
- XY bounding box >=60 x 58 mm including tolerance/service margin before exact STEP;
- radial shorthand R=31 mm may be used only for coarse screening;
- Z rearward keep-out from DML mounting plane >=27 mm before terminal/wire service volume.

### 40 mm architecture consequence
With a working DML rear mounting plane near product Z=8 mm, the successor body may extend to approximately Z=34 mm. The prior MAIN seed with component-side plane at Z=34 mm and components facing the DML is therefore **not compatible with direct XY overlap** with the successor exciter.

This does not yet invalidate the 40 mm product envelope. It invalidates the assumption that useful component height exists directly behind successor exciter projections.

New rule:
- successor exciter projected XY regions are full-depth PCB/component/frame exclusion zones except where exact geometry proves a lateral cavity;
- MAIN tall and low components alike shall be routed around those projected bodies;
- bare PCB overlap is allowed only if exact STEP and board-plane geometry prove physical clearance, and is not assumed.

### Acoustic consequence
The successor's free-air Fs shift from approximately 224 Hz to 115 Hz is large enough that it requires its own electromechanical DML model. Legacy DAEX structural/acoustic tuning cannot be transferred unchanged.

Audit state: **EX25FHE2_4_MANUFACTURER_DRAWING_VERIFIED / STEP_IMPORT_PENDING / Z_STACK_REOPTIMIZATION_REQUIRED**.
