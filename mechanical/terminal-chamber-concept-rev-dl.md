# AudioPicture V2.2 — terminal chamber dense-screen concept Rev.DL

Status: **TERMINAL_CHAMBER_DEFINED / DENSE_EDGE_BIASED_PRIMARY_SCREEN / FULL_RECHECK_AFTER_PASS**

Rev.DK replaces the exposed side-exit with a roofed terminal chamber.

Architecture:
- covered lateral duct;
- terminal chamber at duct end;
- chamber bounded on three sides plus roof;
- controlled opening on the +Y face;
- internal baffle overlaps the opening projection to block inlet-to-exit diagonals.

The parameter search directly uses the edge-biased source population introduced by Rev.DH.

To keep the multi-case search computationally bounded, the destination cloud is reduced but remains multi-X, multi-Y and multi-Z. Any zero-ray candidate must then pass the complete Rev.DH-scale independent recheck before CAD promotion.

Sweep:
- duct L 36/44 mm;
- duct W 48/60 mm;
- roof lower Z 36.5/36.8 mm;
- wall t 1.0/1.2 mm;
- chamber L 16/20/24 mm;
- chamber W 20/28/36 mm;
- exit width 8/12/16 mm;
- internal overlap 4/8/12 mm.

Total: 5,184 combinations.

Promotion sequence:
dense parameter screen -> full independent dense recheck -> actual CadQuery lower/upper mapping -> collision/connectivity -> thermal comparison.

Checks:
C1662 terminal chamber topology defined.
C1663 three-side-plus-roof chamber defined.
C1664 orthogonal +Y discharge defined.
C1665 internal overlap baffle defined.
C1666 dense edge-biased source population used as primary screen.
C1667 5184 parameter combinations defined.
C1668 nonzero geometric throat required.
C1669 full independent dense recheck required after zero candidate.
C1670 real-solid CAD remains gated.
C1671 no CFD/acoustic attenuation claim.

Status: **ACOUSTIC_REV_DL / TERMINAL_CHAMBER_DENSE_SWEEP_EXECUTION_NEXT / C01_TO_C1671**.
