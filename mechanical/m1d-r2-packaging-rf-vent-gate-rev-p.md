# AudioPicture V2.2 — M1D R2 packaging / RF / vent gate Rev.P

Status: **R2_MAIN_C_AND_CONSERVATIVE_ESP32_MASK_GEOMETRY_PASS / TOP_VENT_EXACT_BOOLEAN_BLOCKED_BY_MISSING_SLOT_COORDINATES / RF_TEST_OPEN**

## 1. Candidate
M1D preferred structural candidate:
- R2 tapered radial root;
- front radial depth 2.4 mm through DML overlap;
- root radial depth 4.0 mm;
- growth only behind DML Z>9.3;
- M1D station center X70/Y394.

## 2. MAIN-C
Authoritative MAIN-C envelope:
- X85..235;
- Y315..370.

M1D structural node nominal X span:
- approximately X65..75 for the 10 mm tangential blade/tab family.

Therefore nominal X separation to MAIN-C:
**10 mm**.

Result:
**MAIN-C hard-envelope geometry PASS at nominal coordinates.**

This does not include connector/service swept solids beyond the documented MAIN-C rectangle.

## 3. ESP32 conservative enclosure mask
Documented seed module body:
- X approximately 79..104.5;
- Y approximately 333.5..351.5;
- antenna at low-X end.

Using the documented conservative 15 mm enclosure expansion around that seed body gives a coarse bounding mask:
- X approximately 64..119.5;
- Y approximately 318.5..366.5.

This bounding construction is intentionally more conservative in X than an antenna-only exact mask.

M1D lies around:
- X65..75;
- Y390.4..394-class perimeter geometry.

Nominal Y separation from the coarse mask upper edge Y366.5 to the nearest M1D structural edge Y390.4:
**23.9 mm**.

Result:
**coarse mechanical intersection = none.**

This is not an RF release:
- exact antenna geometry is not represented;
- Z expansion is not fully reconstructed;
- final assembled throughput/range test remains mandatory.

## 4. DML
R2 design rule retains the DML-facing edge and delays radial growth until Z>9.3.

Nominal DML hard-volume intersection remains required:
**0 mm3**.

No stiffness credit may be obtained by moving inward over the DML.

## 5. Rear shell fit
Rear shell:
- product outer boundary 320 x 400;
- PC-CF frame inset from cosmetic edge;
- nominal shell/frame radial XY clearance seed 0.5 mm;
- rear shell inner plane Z37.8.

R2 remains within the existing PC-CF perimeter region and ends at rear-frame Z<=35.

Z clearance to shell inner plane remains positive.

However the exact shell side-wall wrap/profile is not represented by an executable shell B-rep in the current gate, so only the documented envelope/clearance architecture is checked.

Result:
**coarse shell envelope PASS / exact side-wall fit OPEN.**

## 6. Upper vent geometry
Rev.B freezes:
- 10 upper slots total;
- 5 left / 5 right;
- each 3 x 45 mm;
- gross outlet 1350 mm2;
- slot web >=3 mm;
- slot end R1.5;
- no outlet slot may intersect cleat islands, upper structural ring critical webs, or ESP32 keep-out.

But Rev.B does not provide exact XY/Z coordinates for the ten upper slots.

Therefore an exact R2-to-vent boolean cannot be executed from current authoritative data.

Result:
**TOP_VENT_EXACT_COLLISION = OPEN due to missing slot coordinates.**

Do not infer PASS from the area calculation.

## 7. Consequence for vent CAD
The next mechanical definition shall assign exact upper-slot bank coordinates around:
- left/right cleat islands;
- M1D/M2D local structural returns;
- MAIN-C;
- ESP32_RF_KO_A;
- rear shell edge/web constraints.

Because the shell is ASA and the primary structural return is PC-CF, the vent slots should route around the structural nodes rather than cutting the PC-CF return.

## 8. R2 decision
R2 passes the currently computable nominal packaging checks:
- MAIN-C rectangle;
- coarse 15 mm ESP32 bounding mask;
- global Z/shell inner plane;
- DML architecture.

R2 is therefore retained as the preferred structural candidate.

It is **not production-frozen** because:
- exact upper vent coordinates are missing;
- exact shell side-wall B-rep is missing;
- exact antenna STEP/mask and RF test remain open.

## 9. Automatic checks
C784 R2 M1D candidate retained.
C785 MAIN-C envelope X85..235/Y315..370 used.
C786 M1D nominal X65..75.
C787 nominal M1D-to-MAIN-C X separation 10 mm.
C788 MAIN-C nominal hard-envelope PASS.
C789 ESP32 seed body envelope used without pretending exact STEP.
C790 conservative 15 mm XY expansion constructed.
C791 coarse mask X64..119.5/Y318.5..366.5.
C792 M1D nearest Y edge approximately 390.4.
C793 coarse mask-to-M1D Y separation approximately 23.9 mm.
C794 coarse ESP32 mechanical intersection none.
C795 exact RF release remains open.
C796 assembled Wi-Fi/BLE test remains mandatory.
C797 rear shell inner Z37.8 retained.
C798 R2 rear extent remains <=Z35.
C799 coarse shell Z envelope PASS.
C800 exact shell side-wall fit remains open.
C801 Rev.B upper outlet 10x 3x45 geometry retained.
C802 Rev.B exact upper-slot coordinates absent.
C803 exact R2-to-vent boolean not claimable.
C804 vent collision gate remains open.
C805 vent slots shall route around PC-CF structural nodes.
C806 R2 preferred status retained but not frozen.

## 10. State
R2 has passed the packaging checks that can be computed from existing authoritative geometry.

The remaining blocker is no longer the structural taper itself; it is the lack of exact upper vent-bank placement and exact side-wall/RF release geometry.

Status:
**R2_COARSE_PACKAGING_PASS / MAIN_C_PASS / ESP32_COARSE_MASK_PASS_23P9MM_Y / SHELL_Z_PASS / TOP_VENT_COORDINATES_REQUIRED / RF_TEST_OPEN / C01_TO_C806**.
