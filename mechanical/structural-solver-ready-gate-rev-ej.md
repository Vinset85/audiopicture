# AudioPicture V2.2 — structural solver-ready gate Rev.EJ

Status: **LC1_TO_LC7_MANIFEST_READY / NUMERICAL_FEA_NOT_EXECUTED / COUPON_CALIBRATION_REQUIRED**

This revision converts the authoritative Rev.B FEA contract into a machine-readable solver manifest without changing its engineering meaning.

Artifact:
`mechanical/fea/rear-frame-solver-manifest-rev-ej.json`

The manifest freezes:
- LC1..LC7 including independent LC2 left/right variants;
- 70 N nominal structural design load;
- 50 N wall-normal and anti-lift cases;
- 30 N corner torsion;
- 100 N seating;
- 0.25/0.50/1.00 mm assembly-misfit sweep;
- MAT-A/B/C Ez sensitivity 0.20/0.35/0.50 x E_XY_REF;
- Gxz/Gyz sensitivity 0.25/0.40/0.60 x Gxy;
- 23/50/70 C temperature cases;
- five CG positions;
- mesh sizing and <5% convergence criterion;
- required nonlinear/contact and buckling cases;
- required outputs and prohibited pre-execution claims.

No LC1..LC7 numerical result is claimed. SciPy availability is not treated as a substitute for the specified solid/contact/orthotropic FEM.

Checks:
C1786 authoritative Rev.B structural contract preserved.
C1787 machine-readable LC1..LC7 manifest created.
C1788 independent LC2L/LC2R retained.
C1789 MAT-A/B/C and shear sensitivities retained.
C1790 temperature sensitivity retained.
C1791 CG sensitivity retained.
C1792 mesh convergence criterion retained.
C1793 nonlinear/contact cases explicitly identified.
C1794 buckling screens explicitly identified.
C1795 numerical FEM gate remains open.

Status: **STRUCTURAL_FEA_REV_EJ / SOLVER_READY_MANIFEST / NUMERICAL_GATE_OPEN / C01_TO_C1795**.
