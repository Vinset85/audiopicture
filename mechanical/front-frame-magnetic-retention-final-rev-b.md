# AudioPicture V2.2 Rev.B — FINAL front-frame magnetic retention

Status: **MAGNET_ARCHITECTURE_FROZEN / S-04-01-N_4X1_N45 / 8_STATIONS / NO_DML_OVERLAP / FORCE_VALIDATION_ONLY**

## 1. Decision
The previous 6 x 2 mm magnet architecture is withdrawn.

Final baseline magnet:
**supermagnete S-04-01-N**
- NdFeB
- N45
- disc
- diameter 4.0 mm
- thickness 1.0 mm
- tolerance +/-0.1 mm
- axial magnetization
- Ni-Cu-Ni coating
- manufacturer attraction approximately 250 g / 2.45 N under its stated test condition
- manufacturer tangential force approximately 50 g / 0.492 N
- mass 0.096 g
- max operating temperature 80 C.

Quantity:
**8**

No 6/8/10 station sweep remains in the baseline.

## 2. Why this closes the packaging problem
DML projection:
X10..310
Y10..390.

The front carrier has a perimeter band outside the DML projection.

A 4 mm magnet permits a compact local pocket/pad that fits entirely in this perimeter band.

The previous 12 mm pad required by the 6 x 2 mm concept is deleted.

No DML notch is permitted or required.

## 3. Final station coordinates
Use centers 5.0 mm from the product edge.

Top:
M1 = (70,395)
M2 = (250,395)

Bottom:
M3 = (70,5)
M4 = (250,5)

Left:
M5 = (5,135)
M6 = (5,275)

Right:
M7 = (315,135)
M8 = (315,315).

These coordinates are the final nominal magnetic station centers.

## 4. Final magnet pocket
Nominal printed pocket diameter:
**4.4 mm**

Nominal pocket depth:
**1.15 mm**

Final compensated dimensions are determined by ASA process coupon, but the component architecture does not change.

Magnet is rear-loaded and mechanically captured.

Adhesive is secondary retention.

## 5. Local pad
Final local pad envelope:
**6.0 mm diameter nominal**

Maximum DML-facing radial extent:
3.0 mm from magnet center.

For top stations:
center Y395 -> inner pad edge Y392 > DML upper edge390.

Bottom:
center Y5 -> inner edge Y8 < DML lower edge10.

Left:
center X5 -> inner edge X8 < DML left edge10.

Right:
center X315 -> inner edge X312 > DML right edge310.

Therefore nominal geometric clearance from DML projected boundary:
**2.0 mm minimum**.

This eliminates the previous DML overlap.

## 6. Carrier local thickness
Base carrier:
1.8 mm.

A 1.0 mm magnet no longer requires a 3.2 mm rear magnetic boss.

Local magnet capture can remain within approximately:
**1.8..2.2 mm carrier thickness class**
depending final capture-lip process.

This removes the previous local 3.2 mm Z protrusion at magnetic stations.

## 7. Force budget
Manufacturer ideal attraction:
approximately 2.45 N each.

Eight-station arithmetic ideal upper reference:
8 x 2.45 = **19.6 N**.

This is not a guaranteed assembled product force because target thickness, polymer, coating, flatness and air gap reduce force.

The former 20..30 N target is therefore revised.

Final product retention target:
**14..20 N measured normal pull for the complete assembled front frame**.

Reason:
- front assembly mass is <<0.12 kg;
- gravity is only about 1.18 N at the old 120 g upper mass budget;
- 14 N gives >11x static-gravity ratio even at 120 g;
- eight distributed stations resist local vibration and buzz;
- lower force improves controlled peel service removal.

Production acceptance is based on measured assembled force, not catalogue multiplication.

## 8. Peel target
Hidden lower-center peel recess remains.

Target initial user peel:
**3..6 N local hand force**.

Sequential release is desired.

Do not increase magnet size merely to increase normal pull if peel already meets retention requirements.

## 9. Steel targets
Use eight discrete low-carbon steel targets.

Seed target:
- 6 x 6 mm square OR 6 mm diameter
- 0.5..0.8 mm thick.

Exact target thickness is selected from force test.

No continuous steel ring.

No second magnet baseline.

## 10. RF
Discrete 4 mm magnets and 6 mm class targets greatly reduce metallic area relative to the withdrawn architecture.

Nevertheless:
- radar RF keep-out remains mandatory;
- ESP32 antenna keep-out remains mandatory;
- exact RF validation remains a release test.

If a nominal station intersects an exact RF hard keep-out after antenna/radar CAD is frozen, the station may translate ALONG its same perimeter edge only; magnet type/count/size remain frozen.

## 11. Mass
Magnets:
8 x 0.096 g = **0.768 g**.

Even with eight small steel targets, magnetic retention mass is negligible relative to the front-frame mass budget.

## 12. Removed concepts
The following are retired:
- S-06-02-N as baseline;
- K&J D41 as baseline;
- 12 mm circular magnetic pads;
- D-shaped 12 mm pads;
- controlled 0.5..1.2 mm gap used to weaken oversized magnets;
- 6/8/10 station count optimization;
- 20..30 N mandatory assembled target.

They remain historical design-study information only.

## 13. CAD consequence
Regenerate front carrier Rev.B with:
- eight 4.4 mm pockets;
- eight 6.0 mm local pad envelopes;
- station centers defined in section 3;
- local magnetic thickness <=2.2 mm target;
- lower-center peel recess;
- no DML overlap.

The prior front-carrier Rev.A STEP is obsolete for magnetic station geometry.

## 14. Verification gates
Only the following remain before production release:
1. ASA pocket-fit coupon.
2. Actual magnet + selected steel target normal-pull measurement.
3. Peel-force measurement on assembled front frame.
4. RF/radar comparison.
5. vibration/buzz check.

These are validation gates, not architecture-selection gates.

## 15. Automatic checks
C431 magnet MPN S-04-01-N frozen.
C432 magnet size 4 x 1 mm frozen.
C433 magnet count 8 frozen.
C434 all centers 5 mm from corresponding product edge.
C435 local pad diameter 6 mm nominal.
C436 bottom pad inner edge <=Y8.
C437 top pad inner edge >=Y392.
C438 left pad inner edge <=X8.
C439 right pad inner edge >=X312.
C440 DML projected boundary remains X10..310/Y10..390.
C441 nominal DML-pad projected clearance >=2 mm.
C442 no DML notch.
C443 magnet pocket diameter 4.4 mm nominal.
C444 magnet pocket depth 1.15 mm nominal.
C445 magnet mechanically captured.
C446 eight discrete steel targets.
C447 no continuous steel ring.
C448 magnetic station local carrier thickness target <=2.2 mm.
C449 previous 3.2 mm magnet boss removed.
C450 assembled normal retention acceptance 14..20 N.
C451 local peel target 3..6 N.
C452 catalogue force not treated as assembled-force guarantee.
C453 total magnet mass 0.768 g.
C454 S-06-02-N baseline retired.
C455 D41 baseline retired.
C456 12 mm pad architecture retired.
C457 D-shaped pad workaround retired.
C458 gap-to-weaken-oversized-magnet strategy retired.
C459 6/8/10 station optimization retired.
C460 front carrier Rev.B regeneration required.

## 16. Final state
The magnetic-retention architecture is no longer an open optimization problem.

Final:
- **8 x S-04-01-N**
- **4 x 1 mm N45**
- **4.4 mm pockets**
- **6 mm local pads**
- **2 mm nominal projected clearance from DML**
- **14..20 N measured assembled normal-retention acceptance**
- **3..6 N local peel target**
- **8 discrete steel targets**
- **no DML modification**
- **no oversized-magnet gap tuning**

Status:
**FINAL_MAGNET_S04_01_N / 8X_4MM_X1MM / 6MM_PAD / DML_CLEARANCE_2MM / C01_TO_C460 / VALIDATION_NOT_ARCHITECTURE_OPEN**.
