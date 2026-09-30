# AudioPicture V2.2 — sculpted four-bank mapping Rev.DU

Status: **LOWER_DEEP_GEOMETRY_SELECTED / UPPER_RAISED_GEOMETRY_SELECTED / REAL_SOLID_BUILD_DEFINED**

Rev.DS occupancy screening supports differentiated treatment rather than a uniform Z35.1 penalty.

Design direction:
- lower banks: retain the deeper Rev.DO-style geometry where frame clearance permits;
- upper banks: use Z35.1 conservative lower plane because the upper region is influenced by the cleat islands;
- mirror left/right only within the same lower or upper family.

Rev.DT constructs four real-product CadQuery solids against the authoritative Rev.C frame kernel.

The build explicitly measures raw frame overlap and post-sculpt overlap for each bank and exports each bank separately for inspection.

This is still a mechanical integration gate. It does not yet prove fluid connectivity or actual-product LOS.

Next after a clean solid build:
1. fuse/legalize shell attachment features;
2. verify all 22 Rev.BK vent apertures remain open;
3. build fluid channels and check connectivity;
4. rerun dense LOS using actual lower/upper coordinates;
5. compare minimum real throat lower vs upper.

Checks:
C1709 Rev.DS occupancy result supports differentiated lower/upper mapping.
C1710 lower deep geometry retained as candidate.
C1711 upper Z35.1 fallback used for first real build.
C1712 four real CadQuery bank solids defined.
C1713 frame intersection measured before/after sculpt.
C1714 separate STEP outputs defined.
C1715 fluid connectivity remains open.
C1716 actual-product LOS remains open.

Status: **MECHANICAL_REV_DU / FOUR_BANK_SCULPTED_SOLID_EXECUTION_NEXT / C01_TO_C1716**.
