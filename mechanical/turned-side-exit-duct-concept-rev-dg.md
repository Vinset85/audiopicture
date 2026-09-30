# AudioPicture V2.2 — turned side-exit duct concept Rev.DG

Status: **TURNED_SIDE_EXIT_SWEEP_DEFINED / EXIT_ORIENTATION_IS_PRIMARY_VARIABLE / DENSE_RECHECK_REQUIRED_AFTER_PASS**

Rev.DF retains the covered lateral duct but changes the terminal discharge.

The final opening is shielded by:
- a terminal wall;
- an elbow cheek extending back along the duct;
- a return wall that turns the discharge away from the direct vent-to-cavity cone.

Sweep variables:
- duct length 36/44/52 mm;
- width 48/60 mm;
- roof lower Z 36.5/36.8 mm;
- wall thickness 1.0/1.2 mm;
- Y shift 0/8 mm;
- elbow length 8/12/16 mm;
- shielding overlap 2/4/6 mm;
- nominal discharge slot 10/12/16 mm.

Total combinations: 2592.

Promotion sequence:
1. coarse Rev.DF sweep must find zero sampled LOS with non-zero throat;
2. choose compact/high-throat candidates;
3. run a denser independent LOS sample around vent and exit edges;
4. only then build actual CadQuery solids mapped to lower/upper banks.

No candidate is acoustically qualified by LOS alone.

Checks:
C1634 turned side-exit geometry defined.
C1635 terminal wall included.
C1636 elbow cheek included.
C1637 return wall included.
C1638 2592-case sweep defined.
C1639 nonzero throat required.
C1640 zero sampled LOS required.
C1641 dense independent recheck required after coarse pass.
C1642 real-product CAD mapping remains subsequent gate.
C1643 no CFD/acoustic attenuation claim.

Status: **ACOUSTIC_REV_DG / TURNED_EXIT_SWEEP_EXECUTION_NEXT / C01_TO_C1643**.
