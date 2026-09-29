# AudioPicture V2.2 Rev.A — TAS5825M PVDD bulk packaging

Status: **EEU_FR1V471B_RETAINED / HORIZONTAL_LAYDOWN_BASELINE / LEAD_FORM_RETENTION_AND_STEP_RELEASE_GATE**

## Decision
Retain Panasonic **EEU-FR1V471B**:
- 470 uF, 35 V
- 10 x 16 mm body
- 5 mm lead pitch
- 1.79 Arms ripple at 100 kHz
- 28 mOhm max impedance at 100 kHz
- -40..105 C
- 8000 h endurance
- ~2 g typical.

Do not prefer EEU-FR1V471LB 8 x 20 mm: it is longer and its published ripple rating is lower at 1.56 Arms.

## Electrical role
The 470 uF part is the PVDD reservoir. It does not replace the local high-frequency TAS5825M bypass capacitors.

Keep the ceramic PVDD network close to the amplifier pins. TI specifically requires close PVDD bypass placement to control ringing, EMI and reliability.

## Mechanical baseline
Mount the EEU-FR1V471B **horizontally**, body axis parallel to MAIN-P.

Replace the former vertical pocket:
- 12 x 12 x 19 mm

with initial horizontal mechanical envelope:
- **20 x 12 x 12 mm**

The reserve includes body, sleeve clearance, controlled lead forming and retention allowance.

## Z check
MAIN-P laminate:
- Z=18.0..19.6 mm

Generic rear component limit:
- ~Z=36.6 mm

Available rear-side height:
- ~17 mm

Horizontal capacitor envelope:
- ~12 mm

First-order residual:
- ~5 mm

Result:
**COARSE Z PASS**

## Lead forming
Do not bend leads tightly at the rubber seal.

Production requires a controlled forming fixture, relief length before bend, qualified bend radius, and no axial/torsional load into the seal.

Exact dimensions remain a manufacturer-drawing/process gate.

## Retention
Capacitor leads shall not be the sole mechanical support.

Provide a nonconductive cradle/saddle with compliant contact or an equivalently qualified retention system.

The restraint must prevent vibration, lead fatigue, can impact and buzz/rattle without deforming or fully thermally insulating the can.

## Placement
Keep the capacitor:
- near the TAS5825M/PVDD reservoir loop;
- outside exciter columns;
- away from the hottest TAS5825M/TPSM63603 zones where practical;
- clear of XAL7050 magnetic/thermal regions;
- out of the primary convection obstruction path.

## Alternatives
### EEU-FR1V471LB 8 x 20 mm
Not preferred: narrower XY but longer and lower ripple rating.

### Multiple smaller electrolytics
Not preferred unless exact CAD invalidates the single horizontal 470 uF solution.

### Ceramic-only reservoir
Not selected. Any replacement would need proven effective capacitance at 24 V DC bias, ripple behavior, cost and PCB area.

## Qualification
Before production release:
1. import exact Panasonic CAD/drawing;
2. freeze horizontal footprint and lead form;
3. design retention cradle;
4. verify PVDD/GND current loop;
5. run DML/shipping vibration and buzz-rattle checks;
6. obtain capacitor-body temperature from CFD;
7. perform ripple-current/lifetime calculation;
8. manufacturing assembly review.

CAD parameters:
- PVDD_BULK_LAYOUT = HORIZONTAL
- PVDD_BULK_BODY = DIA10 x L16 mm
- PVDD_BULK_MECH_ENVELOPE = 20 x 12 x 12 mm
- PVDD_BULK_RETENTION = REQUIRED
- PVDD_BULK_LEAD_FORM = CONTROLLED_PROCESS

Status: **EEU_FR1V471B_10X16_1P79ARMS_RETAINED / HORIZONTAL_20X12X12_ENVELOPE / COARSE_Z_PASS**.
