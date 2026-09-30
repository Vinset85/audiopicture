# AudioPicture V2.2 Rev.B — front carrier real CAD-kernel generation

Status: **REV_B_ONE_VALID_SOLID / DML_PAD_OVERLAP_REMOVED / GLOBAL_DMU_SOURCE_CANDIDATE**

## 1. Purpose
Close the magnet-pad/DML collision found by the integrated master DMU audit.

Rev.B supersedes Rev.A for assembly collision work.

## 2. Authoritative DML projected keep-out
DML projected rectangle:
- X = 10..310 mm
- Y = 10..390 mm.

Magnetic station structural material shall remain outside this projected hard region unless a later exact perimeter model explicitly creates a legal non-active land.

No DML notch is used.

## 3. Rev.B station centers
Top:
- M1B = (70,388)
- M2B = (250,388)

Bottom:
- M3B = (70,12)
- M4B = (250,12)

Left:
- M5B = (12,135)
- M6B = (12,275)

Right:
- M7B = (308,135)
- M8B = (308,315).

## 4. D-shaped/perimeter-biased station pads
The prior 12 mm circular station pad is withdrawn for assembly use.

Rev.B station pad is generated as:
1. local pad stock around each magnet pocket;
2. pad clipped by the legal perimeter region outside the DML projected keep-out;
3. local blending/connection to the 10 mm carrier perimeter ring;
4. rear-loaded magnet pocket retained.

The DML-facing side is therefore flat/clipped rather than circular.

## 5. Magnet pocket
Packaging reference remains:
- 6.6 mm pocket diameter class;
- 2.2 mm depth class;
- local station thickness approximately 3.2 mm class.

The pocket is biased toward the product perimeter so the required surrounding polymer remains on the legal side of the DML keep-out.

Exact mechanical capture lip/cap remains a detail gate.

## 6. Kernel generation result
Generated with the same CadQuery/OpenCASCADE workflow as Rev.A.

Result:
- primary solid count: **1**
- B-rep validity: **PASS**
- DML projected pad intersection: **0**
- peel recess connectivity: **PASS**
- all eight stations connected to carrier: **PASS**.

Diagnostic volume:
**approximately 26.3 cm3**

The exact final volume may change with capture-lip fillets and process compensation.

## 7. Mass implication
Using the same unfilled ASA density sensitivity:
- 1.05 g/cm3 -> approximately 27.6 g
- 1.075 g/cm3 -> approximately 28.3 g
- 1.10 g/cm3 -> approximately 28.9 g.

Carrier remains far below the 60 g carrier budget.

## 8. Global-Z interpretation
Rev.B remains a local B-rep and is transformed into the frozen product-global Z datum.

Authoritative global front stack:
- fabric outer Z0.0
- fabric rear ~Z0.5
- nominal fabric/DML gap 2.8 mm
- DML front Z3.3
- DML rear Z9.3.

Local magnetic station rear intrusion is accepted only where its XY footprint remains outside the DML hard projection.

Therefore the previous front-carrier global-transform blocker from magnet-pad overlap is closed at the coarse DML-rectangle level.

## 9. Remaining front-carrier gates
Still open:
- exact DML edge/perimeter support geometry;
- magnet mechanical capture detail;
- selected magnet/steel target assembled-force test;
- exact radar/ESP32 RF masks;
- microphone acoustic cone clipping;
- OPT3004 optical mask;
- ASA process compensation;
- fabric process.

## 10. Master DMU source rule
For subsequent master-DMU assembly:
- use Rev.B front carrier;
- do not use Rev.A magnet-pad geometry for collision conclusions.

Rev.A remains historical diagnostic evidence.

## 11. Automatic checks
C431 Rev.B carrier generated in real CAD kernel.
C432 solid_count == 1.
C433 B-rep validity PASS.
C434 Rev.B station centers used.
C435 circular 12 mm assembly pad withdrawn.
C436 pad material clipped outside DML projected keep-out.
C437 DML projected pad intersection == 0.
C438 no DML notch introduced.
C439 all eight magnet stations remain connected.
C440 magnet pocket remains rear-loaded.
C441 peel recess preserves carrier connectivity.
C442 carrier mass remains below budget.
C443 global Z datum unchanged.
C444 fabric/DML gap requirement unchanged.
C445 Rev.B supersedes Rev.A in master DMU.
C446 exact RF masks remain release gate.
C447 exact mic masks remain release gate.
C448 exact optical mask remains release gate.
C449 magnetic assembled-force validation remains release gate.
C450 exact DML edge model remains release gate.

## 12. State
The collision found at C390/C391 is closed at the current authoritative coarse DML projected keep-out.

Status:
**FRONT_CARRIER_REV_B / ONE_VALID_BREP / ZERO_COARSE_DML_PAD_INTERSECTION / APPROX_26P3CM3 / C01_TO_C450 / EXACT_FUNCTIONAL_MASKS_NEXT**.
