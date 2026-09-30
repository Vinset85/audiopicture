# AudioPicture V2.2 — covered lateral duct concept Rev.DD

Status: **COVERED_LATERAL_DUCT_SWEEP_DEFINED / LOS_AND_THROAT_SCREEN / EXECUTION_NEXT**

The previous partial-height Z-wall families failed to eliminate sampled 3D LOS.

Rev.DC changes the governing mechanism: the internal discharge is displaced laterally from the external vent projection and the direct rearward region is roofed.

Parameters:
- lateral duct length: 28 / 36 / 44 / 52 mm;
- duct width: 36 / 48 / 60 mm;
- roof lower Z: 36.2 / 36.5 / 36.8 mm;
- wall thickness: 1.0 / 1.2 mm;
- Y shift: 0 / 8 / 16 mm.

Total combinations: 288.

The first sweep uses a normalized left-bank model. Symmetry is intended for the right bank only after a candidate passes.

A geometric discharge-throat proxy is tracked alongside LOS. It is not the system effective vent area and is not a CFD result.

Promotion requires:
- zero sampled straight 3D LOS in the normalized model;
- non-zero throat;
- no shell/frame hard bridge in the subsequent real-solid build;
- successful mapping to the actual lower and upper vent banks.

Checks:
C1616 covered lateral duct normalized model defined.
C1617 lateral displacement replaces thin-wall Z labyrinth mechanism.
C1618 288 combinations defined.
C1619 LOS and geometric throat screened together.
C1620 zero sampled LOS required.
C1621 normalized throat not treated as effective vent area.
C1622 real-solid mapping required after screening.
C1623 no CFD/acoustic attenuation claim.

Status: **ACOUSTIC_REV_DD / COVERED_DUCT_SWEEP_EXECUTION_NEXT / C01_TO_C1623**.
