# AudioPicture V2.2 — digital validation checkpoint Rev.EN–ES

Status: **PARTIAL_DIGITAL_VALIDATION / NOT_PRODUCTION_RELEASE / FULL_PRODUCT_FEA_CFD_OPEN**

Base `main` HEAD verified before operations:
`19a436701211b5135ecb1b672eae44f177894629`.
Repository inventory covers 269 tracked files and indexes 999 historical
unresolved text statements. These are statements, not 999 independent gates.
Historical PASS labels are not promoted to new verified results.

## Rev.EN: regenerated export and falsification of treatment

CadQuery 2.8.0 reproduced Rev.EM:
solid 287929.522 mm3; fluid 640018.572 mm3; both valid single solids.
The exporter now reports solid count/volume, SHA256, independently reimported
STEP volumes, bounding boxes, Z extents and failure exit code. Output byte
sizes need not match historical files; STEP metadata/STL tessellation can differ.

Independent audit of the regenerated STEP found:
- fully footprint-covered vents: **4/22**;
- area-weighted footprint coverage: **53.9616929%**;
- open axial rays into the audit cavity: **22/22**.

This falsifies universal geometric LOS blockage. The old Rev.EF sample rays
aim at distant cavity points; blocking those shallow rays does not exclude
short, near-normal paths. Cutting vent profiles through chamber roofs without
a closed offset bottom path leaves an axial short circuit.

The Rev.EM fluid is Z33..40.25 mm, not the complete product, exterior room,
wall gap or conjugate solid/fluid domain. Export-valid is not solver-ready
for the full Rev.EK physics.

## Rev.EO rejected; Rev.EQ new parallel-cell candidate

The first collector candidate blocked axial/sampled LOS but has an upper
gate only 5.1 mm2 per side. It is rejected as an airflow-area candidate.

Rev.EQ creates a stepped cell per aperture, preserving Rev.BK nominal capsules:
- floor Z29..30;
- intermediate baffle Z33..34;
- shell inner/outer remain Z37.8/Z40;
- walls 1 mm and opposed openings 2 mm are **candidate dimensions**, not
  qualified process tolerances;
- aggregate geometric minimum sections: inlet **960 mm2**, outlet **900 mm2**;
- **22/22** complete aperture cell coverage;
- **2574** finite rays tested; no open ray;
- all nominal vents remain open and connected in the audited complement;
- BREP/export/reimport and coarse-frame collision/clearance checks executed.

A continuous straight-ray bound supplements sampling. A ray crossing the
inlet at Z37.8 with local short-axis coordinate u in [0,3] and the bottom
outlet at Z30 with u in [-2,0] must cross Z34 at u in
[-0.974359,1.538462]. The solid intermediate baffle occupies u=[-3,2].
End/side walls close alternate escape paths. This bound applies to the
nominal modeled cell; manufacturing errors require coupon validation.

No airflow, acoustic attenuation or thermal capacity follows from these
geometric sections. Rev.EQ remains a candidate, not frozen production CAD.
Its internal complement lacks electronics/harnesses and room/wall domains.
Paired lower/upper process coupons are exported as valid STEP/STL.

## Rev.ES: conservative RF frame correction

The regenerated Rev.J kernel intersected the documented conservative
ESP32 mask X64..119.5 / Y318.5..366.5 by **1798 mm3**.
Rev.ES subtracts that mask: zero overlap, one valid solid, volume **144202 mm3**.
Exact antenna/radar RF masks and assembled RF testing remain OPEN.
Removing this material changes the frame load path; full structural analysis
must use the corrected frame. The RF correction does not create missing
fastener/boss/contact geometry.

## Rev.EP: executed local FEM, scope strictly limited

Gmsh 4.15.2 and CalculiX 2.23 were installed/compiled in the workspace.
SPOOLES and ARPACK are linked. The uniaxial unit cube gives analytical
displacement 1/1900 mm with relative numerical error **2e-8**.

M1D is a **5 N front-retention subcomponent**, not a 70 N complete frame.
Remote cut faces fixed; equal nodal load on the tab; isotropic debug
E=1900 MPa and nu=0.35 as permitted by Rev.L, not qualified material data.
Three quadratic-tetrahedron meshes: 5150 / 10791 / 34036 elements.
Direct-solver peak target displacements: 0.0237501 / 0.0238297 / 0.0241058 mm.
M1->M2 displacement change **1.1453%**; reactions close the 5 N load.
Raw peak stress is not a qualified orthotropic failure index and its convergence
is not closed. Early iterative solves had up to 1.29% reaction residual;
the direct repeats supersede those values.

Also executed **27 normalized local material cases**: MAT-A/B/C E3/E1 ratios
0.20/0.35/0.50 crossed with G13/G12 and G23/G12=0.25/0.40/0.60.
E1=E2=1900 MPa, all Poisson seeds 0.35, G12=E1/[2(1+nu)] are explicitly
assumed screening inputs. Positive-definite reciprocal compliance checked.
Target displacement range 0.0321598..0.0581529 mm. No strength margin,
temperature qualification, LC1–LC7, nonlinear/contact or buckling result claimed.

## CFD runtime and remaining prerequisites

Native Elmer built from official source commit
`4b49ea695ff021e9a046b403f5ebf6df8ec317c4` with workspace-local installation.
Official radiation regression relative reference error **4.44e-10**.
Official natural-convection regression relative reference error **1.88e-7**,
but it reports coupled-system nonconvergence. Extended/direct/gauge trials
do not yet close coupled convergence; one trial failed with NaN. These are
solver tests, not AudioPicture CFD or thermal results.

Required next order:
1. complete corrected structural frame interfaces and exact DMU/RF/cable inputs;
2. qualify material/contact/thermal data or explicitly source screening models;
3. mesh full conjugate product/room/wall-gap domain with every required obstruction;
4. qualify coupled buoyancy/conduction/radiation solver setup;
5. execute Rev.EJ LC1–LC7 and Rev.EK CFD01–CFD05, mesh convergence and balances;
6. correlate physical coupons/subassemblies, rerun and freeze production geometry.

No proxy 75/80% vent fractions were imposed as CFD conditions. No project
thermal temperature, pressure loss, flow rate, stagnant volume or CFD PASS reported.

## Electronics, software and physical release

BOM: 74 rows, with 35 rows containing VALIDATE/VERIFY/PLACEHOLDER/OPEN/DNP.
Even other FROZEN rows can retain open coordinates/interfaces. Exact manufacturer
land patterns and native electrical verification remain necessary.
No native KiCad schematic/PCB or firmware/Home Assistant implementation files
were present in the pinned repository. Their documentation is not executable validation.
No Gerbers, production BOM verification, firmware test completion or build-ready
first article is claimed.

The user confirmed no missing coupon/exact CAD data are available.
`test/physical-qualification-rev-er.json` defines the physical work, provenance,
existing numeric acceptance limits and limits still OPEN. It does not invent
physical results, process tolerances or unspecified acceptance thresholds.

Primary solver references:
- [CalculiX official source](https://www.dhondt.de/)
- [Elmer official source](https://github.com/ElmerCSC/elmerfem)
- [Elmer physics manual](https://ftp.csc.fi/pub/files/index/elmer/doc/ElmerModelsManual.pdf)

Historical EX25FHE2 mechanical naming differs from the frozen DAEX25FHE-4
BOM/user specification. Keep the conservative 26 mm depth envelope as a
packaging assumption until exact mounted geometry is reconciled; no device
substitution or tolerance release is authorized by that old name.
