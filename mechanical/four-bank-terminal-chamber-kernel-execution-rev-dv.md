# AudioPicture V2.2 — four-bank terminal chamber kernel execution Rev.DV

Status: **FOUR_BANK_REAL_KERNEL_PASS / ONE_SOLID_PER_BANK / ZERO_PC_CF_OVERLAP / SHELL_FUSION_NEXT**

Rev.DT was actually executed with CadQuery 2.8.0.

Results:
- LL: valid, 1 solid, raw PC-CF overlap 0.0 mm3, post-sculpt overlap 0.0 mm3, volume 2240.4 mm3.
- LR: valid, 1 solid, raw PC-CF overlap 0.0 mm3, post-sculpt overlap 0.0 mm3, volume 2240.4 mm3.
- UL: valid, 1 solid, raw PC-CF overlap 0.0 mm3, post-sculpt overlap 0.0 mm3, volume 2039.1 mm3.
- UR: valid, 1 solid, raw PC-CF overlap 0.0 mm3, post-sculpt overlap 0.0 mm3, volume 2039.1 mm3.

The selected real placements therefore do not require frame subtraction in the current Rev.C coarse-frame model.

Lower banks retain zlow 34.0 mm.
Upper banks retain zlow 35.1 mm.

Decision:
promote Rev.DT as the mechanical baseline for the next shell-integration gate.

Next:
- union the four chamber solids with authoritative Rev.BK shell;
- verify one valid shell solid;
- verify all 22 vent apertures remain unreclosed;
- measure chamber-shell fusion/contact;
- then build the real fluid volume and rerun LOS.

Checks:
C1717 Rev.DT actually executed with CadQuery 2.8.0.
C1718 LL valid one solid.
C1719 LR valid one solid.
C1720 UL valid one solid.
C1721 UR valid one solid.
C1722 raw PC-CF overlap zero for all banks.
C1723 post-sculpt PC-CF overlap zero for all banks.
C1724 lower bank volume 2240.4mm3 each.
C1725 upper bank volume 2039.1mm3 each.
C1726 Rev.DT promoted to mechanical baseline.
C1727 shell fusion and vent-reclosure gate next.

Status: **MECHANICAL_REV_DV / FOUR_BANK_KERNEL_PASS / SHELL_INTEGRATION_NEXT / C01_TO_C1727**.
