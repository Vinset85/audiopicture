# AudioPicture V2.2 — passive CFD solver-ready gate Rev.EK

Status: **CFD_MANIFEST_READY / REAL_APERTURES_REQUIRED / NUMERICAL_SOLVER_GATE_OPEN**

Rev.EK converts the authoritative rear-chimney CFD contract and current Rev.BK/EC geometry into a machine-readable numerical manifest.

Artifact:
`mechanical/cfd/passive-convection-solver-manifest-rev-ek.json`

Key safeguards:
- CFD must mesh the real Rev.BK apertures;
- 75% inlet and 80% outlet effective-area proxies are reduced-order assumptions only and shall not be imposed as CFD boundary conditions;
- gravity, natural convection, solid conduction and radiation are mandatory;
- pure conduction cannot close the passive-convection gate;
- component and aggregate heat sources may not be double-counted;
- AIR_SHT45_CHAMBER remains separate;
- wall plane/gap is explicit.

Priority matrix remains CFD01..CFD05: 5W/30C/4mm, 8W/30C/4mm, 10W/35C/4mm, 8W/35C/3mm, 8W/35C/5mm.

Mesh convergence manifest:
M0 bulk 6.0 mm / slots 1.5 mm / hot surfaces 2.0 mm;
M1 bulk 4.0 mm / slots 1.0 mm / hot surfaces 1.5 mm;
M2 bulk 3.0 mm / slots 0.75 mm / hot surfaces 1.0 mm.
At least three cells through the wall gap where applicable. Numerical convergence target is <5% on the specified thermal/flow metrics.

No CFD result is claimed.

Checks:
C1796 authoritative CFD contract preserved.
C1797 Rev.BK real gross apertures encoded.
C1798 reduced-order area proxies excluded from CFD boundary conditions.
C1799 CFD01..CFD05 matrix encoded.
C1800 gravity/natural convection/conduction/radiation mandatory.
C1801 heat-source double-counting rule encoded.
C1802 three-level mesh sequence encoded.
C1803 <5% mesh-convergence target encoded.
C1804 required obstructions and outputs encoded.
C1805 numerical CFD solver gate remains open.

Status: **THERMAL_CFD_REV_EK / SOLVER_READY_MANIFEST / NUMERICAL_GATE_OPEN / C01_TO_C1805**.
