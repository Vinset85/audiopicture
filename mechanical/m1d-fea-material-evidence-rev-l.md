# AudioPicture V2.2 — M1D FEA submodel and PC-CF material evidence Rev.L

Status: **M1D_SUBMODEL_KERNEL_READY / DATASHEET_SCREENING_PROPERTIES_IDENTIFIED / RELEASE_ORTHOTROPIC_DATA_OPEN**

## 1. M1D local model
The first local structural submodel is M1D, top station at X70/Y394.

It includes:
- front tab;
- complete local perimeter return;
- top rear-ring segment;
- nominal rear-ring half-span 40 mm each side.

Boundary sensitivity remains 30/40/60 mm each side.

The remote rear-ring cut faces are the boundary-condition surfaces. The return root itself shall not be directly fixed.

## 2. Kernel acceptance
M1D submodel must retain the Rev.J connectivity:
- one connected solid;
- positive rear-return overlap;
- positive return-tab overlap;
- DML intersection zero.

Generator:
mechanical/cad/generate_m1d_fea_submodel_rev_k.py

## 3. Manufacturer material evidence
Baseline material remains Prusament PC Blend Carbon Fiber.

Prusa Polymers' current technical datasheet identifies the material as a carbon-fiber-filled polycarbonate blend for FDM/FFF.

Manufacturer-reported printed-specimen values include:
- tensile yield strength approximately 63 MPa in the reported horizontal and vertical-xz specimen directions;
- tensile modulus approximately 1.9 GPa horizontal and 2.0 GPa vertical-xz;
- flexural strength approximately 88 MPa horizontal and 94 MPa vertical-xz;
- flexural modulus approximately 2.1 GPa horizontal and 2.2 GPa vertical-xz.

The same datasheet reports interlayer adhesion approximately 21 MPa and HDT approximately 113/93 C depending on load condition.

These values are manufacturer test evidence, not a complete orthotropic constitutive model.

## 4. Important limitation
The public manufacturer data does not provide the full release model required by Rev.K:
- E1/E2/E3 complete mapping for the selected product print orientation;
- G12/G13/G23;
- all Poisson ratios;
- directional compression allowables;
- directional shear strengths;
- temperature-dependent orthotropic curves for the exact process;
- strain-to-failure by required material axes.

Therefore no release-quality orthotropic FEA can yet be run without assumptions.

## 5. Allowed preliminary solver model
A debug/screening solve may use an isotropic elastic seed:
- E = 1.9 GPa conservative of the two published tensile-modulus directions;
- nu = sensitivity only, 0.30 / 0.35 / 0.40;
- density = use current manufacturer value only after confirming the exact selected spool/TDS revision.

This model may be used to:
- verify mesh;
- verify boundary conditions;
- compare 30/40/60 mm boundary span;
- identify gross root hot spots;
- estimate displacement order of magnitude.

It may NOT be used to claim:
- production safety factor;
- PC-CF directional failure margin;
- fatigue life;
- hot-condition release.

## 6. Strength use
The published ~63 MPa tensile yield value shall not be used as a universal isotropic allowable.

The ~21 MPa interlayer-adhesion value is evidence that layer/interface behavior requires separate treatment.

Final allowable values must come from coupons printed with the production process/orientation.

## 7. Coupon priority
Minimum Rev.L coupon program:
1. tensile along principal in-plane toolpath direction;
2. tensile transverse in-plane;
3. Z/interlayer tensile;
4. in-plane shear;
5. out-of-plane shear or equivalent characterization;
6. local 10x2.4 mm return-blade bending coupon;
7. return-to-ring root/gusset subassembly;
8. hot-condition repeats at selected design temperature.

The root/gusset subassembly is especially important because M1D is dominated by cantilever/root deformation rather than bulk uniaxial tension alone.

## 8. M1D loads
Retain:
- 5 N normal;
- 2 N tangential;
- 10 N normal proof seed;
- 5 N + 2 N combined;
- 5 N eccentric edge load.

Report target displacement and convert the normal component into G_EFF stack contribution.

## 9. RF caveat
M1D is also the station nearest the ESP32 RF-sensitive region.

Structural FEA optimization may not add PC-CF mass toward the antenna simply to reduce stress.

Any gusset growth must be checked against the exact RF mask.

## 10. Automatic checks
C709 M1D local submodel generator added.
C710 M1D rear-ring half-span seed 40 mm.
C711 30/40/60 mm boundary sensitivity retained.
C712 return root not directly fixed.
C713 one-solid local kernel required.
C714 DML intersection zero required.
C715 manufacturer PCCF printed tensile modulus evidence identified.
C716 manufacturer PCCF printed tensile strength evidence identified.
C717 manufacturer interlayer adhesion evidence identified.
C718 manufacturer public data not treated as complete orthotropic model.
C719 isotropic E=1.9 GPa allowed for debug only.
C720 Poisson 0.30/0.35/0.40 sensitivity allowed for debug only.
C721 63 MPa not used as universal release allowable.
C722 production coupons required.
C723 return-blade bending coupon added.
C724 return/root subassembly test added.
C725 hot-condition coupon repeat required.
C726 M1D RF mask remains coupled to structural optimization.
C727 no release FEA result claimed.

## 11. State
M1D is ready for local kernel extraction and preliminary solver/debug work.

The manufacturer datasheet materially improves the screening model, but it does not close the orthotropic material gate.

Status:
**M1D_FEA_SUBMODEL_READY / MANUFACTURER_SCREENING_EVIDENCE / ISOTROPIC_DEBUG_ALLOWED / ORTHOTROPIC_RELEASE_COUPONS_REQUIRED / C01_TO_C727**.
