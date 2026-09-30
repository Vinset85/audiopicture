# AudioPicture V2.2 — labyrinth height robustness screen Rev.CB

Status: **HEIGHT_ROBUSTNESS_SCREEN_COMPLETE / H0P8_H1P0_PRE_CFD_SET / H1P0_EXECUTED_BASELINE / PRODUCTION_HEIGHT_OPEN**

## Purpose
Screen the Rev.BZ height sweep using geometry only.

This does not replace CFD, acoustic testing or physical dimensional qualification.

## Sensitivity input
Nominal shell-to-frame gap: 2.8 mm.

Engineering sensitivity cases:
2.0 / 2.4 / 2.8 / 3.2 mm.

These values are not production tolerances.

## Clearance results
At the most restrictive 2.0 mm sensitivity case:
- H0.8 -> 1.2 mm remaining;
- H1.0 -> 1.0 mm remaining;
- H1.2 -> 0.8 mm remaining;
- H1.4 -> 0.6 mm remaining.

At nominal 2.8 mm:
- H0.8 -> 2.0 mm;
- H1.0 -> 1.8 mm;
- H1.2 -> 1.6 mm;
- H1.4 -> 1.4 mm.

No candidate contacts the nominal/coarse frame in this sensitivity screen.

## Engineering decision
There is currently no measured acoustic or thermal evidence that justifies spending additional clearance on H1.2 or H1.4.

Therefore:
- H0.8 and H1.0 form the preferred pre-CFD candidate set;
- H1.0 remains the executed CAD baseline;
- H1.2 and H1.4 remain comparison cases;
- no production H is frozen.

This is a conservative geometry decision, not a claim that H0.8 or H1.0 is thermally/acoustically superior.

## Next simulation gate
CFD should compare at minimum:
- H0.8;
- H1.0;
- no-baffle Rev.BK reference.

Recommended outputs:
- inlet/outlet mass flow;
- pressure distribution across labyrinth;
- local velocity maxima;
- TPA/Pi component temperatures or thermal proxies under defined loads;
- recirculation/dead zones.

Acoustic prototype comparison should include H0.8 and H1.0 with the same vent topology.

## Physical release gate
Before production H freeze:
- measure actual shell/frame gap at relevant vent banks;
- measure shell warpage after representative ASA process;
- measure PC-CF frame rear-plane variation;
- establish a justified minimum no-contact clearance.

## Checks
C1392 Rev.BY robustness sweep executed.
C1393 no H contacts at nominal 2.8mm.
C1394 no H contacts at 2.0mm engineering sensitivity.
C1395 H0.8 minimum sensitivity clearance 1.2mm.
C1396 H1.0 minimum sensitivity clearance 1.0mm.
C1397 H1.2 minimum sensitivity clearance 0.8mm.
C1398 H1.4 minimum sensitivity clearance 0.6mm.
C1399 sensitivity values are not production tolerances.
C1400 H0.8/H1.0 selected as pre-CFD set.
C1401 H1.0 remains executed baseline.
C1402 H1.2/H1.4 retained as comparison only.
C1403 production H remains open.
C1404 CFD must include no-baffle reference.
C1405 physical gap/warpage measurement required before release.

Status:
**LABYRINTH_REV_CB / PRE_CFD_H0P8_H1P0 / H1P0_EXECUTED_BASELINE / PHYSICAL_AND_CFD_GATE / C01_TO_C1405**.
