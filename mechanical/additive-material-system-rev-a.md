# AudioPicture V2.2 Rev.A — Additive manufacturing material system

Status: **DUAL_MATERIAL_ARCHITECTURE_SELECTED / EXACT_GRADE_AND_PRINT_PROCESS_QUALIFICATION_OPEN**

## 1. Architecture
Do not require one polymer to perform every mechanical, cosmetic, thermal and RF function.

Baseline:
- rear structural frame/spines/bosses: carbon-fibre reinforced PC-family engineering filament;
- cosmetic rear shell/front-frame non-RF-critical parts: ASA-family unfilled polymer;
- 60 GHz radar forward window/carrier region: unfilled non-conductive polymer, independently EM-qualified;
- compliant DML interface: PORON 4701-30 family as defined separately.

## 2. Structural-frame reference material
First qualification reference: Prusament PC Blend Carbon Fiber or mechanically equivalent characterized PC-CF.

Manufacturer-published reference points include approximately:
- temperature resistance 114 C;
- improved dimensional stability and creep resistance versus unfilled PC;
- hardened nozzle required;
- nominal nozzle temperature around 285 C and bed around 110 C.

These values are process/material references, not automatic properties of the final printed AudioPicture frame. Printed-part properties remain orientation/process dependent.

## 3. Cosmetic-shell reference material
First qualification reference: Polymaker ASA / equivalent characterized ASA.

Published reference properties are approximately:
- Tg 98 C;
- Vicat 105 C;
- HDT about 100 C at 1.8 MPa;
- XY Young modulus about 2.38 GPa for the referenced dataset;
- enclosure/chamber recommended by the supplier.

ASA is preferred over PLA as the baseline cosmetic enclosure material because of temperature/environmental margin. Exact color, texture and grade remain open.

## 4. PA-CF alternative
PAHT-CF remains a high-temperature structural alternative, not the primary baseline.

Published reference for Bambu PAHT-CF includes:
- density about 1.06 g/cm3;
- flexural modulus about 4.12 GPa;
- HDT about 194 C;
- moisture conditioning/drying requirements.

Use it only if structural/thermal FEA shows PC-CF margin is insufficient or if print/process testing shows a clear benefit.

## 5. Radar rule
Carbon-filled polymers shall be treated as RF-risk materials around the BGT60TR13C forward field.

No PC-CF structural rib, boss, insert or carbon-filled cosmetic layer is allowed inside RADAR_RF_KEEP_OUT unless 60 GHz EM analysis or measurement qualifies it.

Provide a replaceable unfilled-polymer RF window in the front/rear structural path as required by the final radar orientation.

## 6. Initial structural CAD assumptions
For the PC-CF rear frame, start CAD sensitivity with:
- nominal structural wall: 2.4 mm;
- primary perimeter beam/rib wall: 2.4..3.0 mm;
- local boss wall around inserts: >=2.5 mm radial material beyond insert envelope;
- fillet at rib/boss roots: >=1.5 mm where geometry permits;
- minimum three effective perimeter lines around critical structural sections before infill contribution is credited.

These are modeling starts, not manufacturing minima.

## 7. Print anisotropy
Structural FEA shall not use an isotropic bulk-PC material card.

Use orthotropic/anisotropic printed-part allowables derived from:
- supplier printed-specimen data where applicable;
- conservative Z-direction reduction;
- actual planned layer orientation;
- local raster/perimeter strategy.

Wall-mount and insert pull-out load paths should lie primarily in strong printed directions.

## 8. Print orientation
Preferred rear-frame orientation shall minimize:
- Z-direction tension at wall-mount features;
- layer splitting around inserts;
- warpage over the 320 x 400 mm envelope.

If the complete frame cannot be printed with acceptable dimensional stability, split it into mechanically keyed structural subframes. A split shall not cross a high DML-reaction or wall-mount load path without a qualified joint.

## 9. Inserts and fasteners
Use heat-set threaded inserts only in sufficiently massive PC-CF/ASA bosses.

Rules:
- do not place insert heat zones near PORON datum surfaces;
- no insert installation load into DML;
- radar-zone metallic inserts prohibited unless RF-cleared;
- repeated-service connectors shall react into PC-CF structural features, not cosmetic ASA walls.

Exact insert series remains open.

## 10. Thermal model
Use PC-CF structural frame as mechanically heat-tolerant support, but do not assume it is an effective heat sink.

The thermal simulation shall separately model:
- PCB copper spreading;
- air cavity;
- rear-shell conduction/convection;
- polymer conductivity sensitivity;
- PoE/DC-DC/TAS5825M losses.

SHT45 chamber remains thermally isolated.

## 11. Qualification coupons
Before production print freeze, manufacture coupons with the same printer/nozzle/layer height/chamber and raster strategy intended for the frame.

Minimum tests:
- dimensional shrink/warpage;
- tensile/flexural comparison in relevant XY/Z orientations;
- heat-soak dimensional stability;
- insert pull-out;
- sustained-load creep;
- screw/boss cycling;
- vibration/buzz/rattle;
- foam hard-stop dimensional repeatability.

This is process qualification, not a separate acoustic prototype requirement.

## 12. Release rule
PC-CF becomes the production structural material only after structural/thermal FEA and print-process coupon qualification. ASA becomes the production cosmetic material only after dimensional, surface, temperature and assembly qualification.

Status remains open for exact manufacturer/SKU so equivalent characterized materials can be compared before procurement lock.
