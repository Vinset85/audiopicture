# AudioPicture V2.2 Rev.A — front carrier real CAD-kernel generation

Status: **REAL_OPENCASCADE_FRONT_CARRIER / ONE_VALID_SOLID / MASS_28P2_TO_29P6G_CARRIER_ONLY / DMU_STEP_GENERATED**

## 1. Method
The front carrier was generated with CadQuery 2.8 using the OpenCASCADE kernel available in the engineering runtime.

This is a real B-rep generation, not a mesh approximation.

## 2. Geometry generated
Nominal carrier:
- 318.4 x 398.4 mm outer projected size;
- 10 mm perimeter ring;
- 1.8 mm base structural thickness;
- eight local magnet station pads;
- 6.6 mm class rear-loaded magnet pockets;
- local station thickness to 3.2 mm in this first kernel model;
- lower-center 28 x 4 mm peel recess.

Magnet centers:
- M1 (70,386)
- M2 (250,386)
- M3 (70,14)
- M4 (250,14)
- M5 (14,135)
- M6 (14,275)
- M7 (306,135)
- M8 (306,315).

## 3. Kernel result
Primary solid count:
**1**

Kernel validity:
**PASS**

Volume:
**26,887.56 mm3 = 26.888 cm3**

Bounding box:
**318.4 x 398.4 x 3.2 mm**

The 3.2 mm Z extent occurs only at local magnetic station thickening; the base ring remains 1.8 mm.

## 4. Carrier-only mass sensitivity
Using unfilled ASA density sensitivity only:
- 1.05 g/cm3 -> 28.23 g
- 1.075 g/cm3 -> 28.90 g
- 1.10 g/cm3 -> 29.58 g.

Working CAD carrier-only mass:
**~28.2..29.6 g**

This excludes:
- fabric;
- printing ink;
- adhesive;
- eight magnets;
- steel targets;
- compliant anti-rattle pads.

## 5. Budget interpretation
Previous carrier budget:
35..60 g.

The real first B-rep is below that range, leaving useful mass headroom for:
- locator features;
- final magnet mechanical caps;
- fabric process features;
- local anti-warp reinforcement if required.

Do not add material merely to consume the budget.

## 6. Peel-recess result
The lower-center peel recess does not disconnect the perimeter ring.

Therefore:
- carrier remains one connected solid;
- progressive peel architecture remains geometrically viable.

Exact edge radii/finger guard remain a detail-feature gate.

## 7. Magnet-pocket result
All eight station pads remain connected to the carrier.

Pocket geometry retains a front-side floor in this diagnostic model.

Final release still requires:
- mechanical capture lip/cap detail;
- print-process compensated pocket diameter;
- G_MAG force tuning;
- RF keep-out clipping with exact masks.

## 8. STEP artifact
Generated artifact:
**AP22_FRONT_CARRIER_REV_A_DMU.step**

This STEP is a G2/front-system DMU artifact, not a manufacturing release.

## 9. Integration into master DMU
Next assembly checks:
- front carrier vs DML front plane;
- 2.8 mm nominal fabric-DML gap;
- local magnet-pad rear intrusion;
- microphone port cones;
- radar RF cone;
- OPT3004 optical path;
- front-frame removal sweep;
- artwork/fabric wrap envelope.

## 10. Release limits
The STEP may be used for:
- master DMU assembly;
- mass/CG update;
- collision checks;
- front-frame handling studies.

It shall not yet be used as production print release because:
- exact fabric is open;
- magnet mechanical capture detail is open;
- exact RF masks are open;
- print warp/process compensation is open;
- assembled magnetic-force validation is open.

## 11. Automatic checks
C366 real front-carrier B-rep generated.
C367 front-carrier solid count == 1.
C368 kernel validity PASS.
C369 CAD volume recorded.
C370 CAD carrier-only mass sensitivity recorded.
C371 carrier-only mass below 60 g budget.
C372 peel recess preserves ring connectivity.
C373 all eight magnet pads remain connected.
C374 local station Z extent recorded.
C375 base ring remains 1.8 mm nominal.
C376 STEP artifact generated.
C377 STEP marked DMU, not manufacturing release.
C378 fabric/adhesive/magnets/targets excluded from carrier-only mass.
C379 master-DMU collision pass required next.
C380 exact RF-mask clipping required before production release.

## 12. State
Real CAD carrier:
**PASS**

One valid B-rep:
**PASS**

Volume:
**26.888 cm3**

Carrier-only mass:
**28.2..29.6 g**

Bounding box:
**318.4 x 398.4 x 3.2 mm**

Status:
**OPEN_CASCADE_FRONT_CARRIER_ONE_SOLID / 26P888CM3 / 28P2_TO_29P6G / C01_TO_C380 / MASTER_DMU_INTEGRATION_NEXT**.
