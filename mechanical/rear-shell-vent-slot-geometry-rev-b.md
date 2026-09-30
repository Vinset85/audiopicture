# AudioPicture V2.2 Rev.B — rear-shell passive vent slot geometry

Status: **900MM2_EFFECTIVE_INLET_AND_1000MM2_EFFECTIVE_OUTLET_GEOMETRY_DEFINED / CFD_PENDING**

## 1. Objective
Revise the rear-shell passive ventilation geometry after the reduced-order airflow screen.

Targets:
- effective inlet >=900 mm2 preferred;
- effective outlet >=1000 mm2 preferred;
- retain 600/750 mm2 as absolute architecture minima only;
- hidden from frontal view;
- no direct acoustic bypass around DML;
- preserve wall mount, service, RF and harness access.

## 2. Effective-area policy
Gross CAD opening area is not treated as effective area.

Use preliminary blockage factor:
- inlet effective factor = 0.75
- outlet effective factor = 0.80.

These are conservative CAD sizing factors only and must be replaced by CFD/actual geometry.

Therefore gross targets:
- inlet gross >=1200 mm2 to guarantee 900 mm2 at 0.75 factor;
- outlet gross >=1250 mm2 to guarantee 1000 mm2 at 0.80 factor.

## 3. Lower inlet architecture
Use two hidden lower/rear slot banks rather than one central opening.

LEFT_INLET_BANK:
- positioned in lower-left rear shell region;
- outside central service recess;
- avoids L1 structural/exciter region through local segmentation.

RIGHT_INLET_BANK:
- positioned lower-right;
- avoids ENV room-air chamber and right structural rail;
- segmented around harness/support geometry.

Air enters from lower rear/wall-gap direction, not through the front fabric/DML perimeter.

## 4. Inlet slot module
Seed slot:
- width 3.0 mm
- clear length 40 mm
- gross area 120 mm2 per slot.

Use:
- 6 slots left
- 6 slots right

Gross:
12 x 120 = **1440 mm2**.

At 0.75 effective factor:
**1080 mm2 effective seed**.

This exceeds the preferred 900 mm2 target with approximately 20 percent area margin.

## 5. Inlet slot spacing
Seed:
- slot width 3.0 mm
- solid web between slots >=3.0 mm
- end radius 1.5 mm
- no sharp rectangular slot ends.

Slots may be staggered to avoid local shell weakness.

Do not create a perforation line that acts as a tear hinge across the entire shell.

## 6. Inlet acoustic labyrinth
No line-of-sight path from rear inlet to DML perimeter.

Use:
1. external lower/rear slot;
2. first internal baffle/turn;
3. vertical entry plenum;
4. second offset into electronics cavity.

Minimum:
**two direction changes** between room-facing opening and main internal cavity where packaging permits.

Baffles remain open enough not to destroy the pressure budget.

## 7. Central service recess
Service recess remains:
- X100..220
- Y20..48
- rear region.

It is not counted toward guaranteed thermal inlet area.

Reason:
installed Ethernet/power cables can unpredictably block it.

Any airflow through the service recess is bonus area only.

## 8. ENV exclusion
SHT45 chamber remains separate.

Do not use ENV chamber openings as part of the 1080 mm2 main inlet calculation.

This preserves environmental measurement quality.

## 9. Upper outlet architecture
Use hidden upper/rear slot banks exhausting into the wall gap.

Preferred:
- left upper bank;
- right upper bank;
- optional center segments only where cleat/MAIN-C geometry permits.

No outlet slot intersects:
- cleat load islands;
- M4 bosses;
- upper structural ring critical webs;
- ESP32 antenna keep-out.

## 10. Outlet slot module
Seed slot:
- width 3.0 mm
- clear length 45 mm
- gross area 135 mm2.

Use:
- 5 slots left
- 5 slots right

Gross:
10 x 135 = **1350 mm2**.

At 0.80 effective factor:
**1080 mm2 effective seed**.

This exceeds the preferred 1000 mm2 target.

## 11. Outlet slot spacing
- 3 mm slot
- >=3 mm web
- 1.5 mm end radius
- stagger if required around mount nodes.

Upper outlet geometry must not create a continuous weak hinge immediately below the cleat islands.

## 12. Outlet acoustic treatment
Outlet is rear-facing into wall gap.

Use offset baffle/louver geometry so there is no direct internal-to-room line of sight.

Do not use dense acoustic foam/filter as baseline because pressure budget is very small.

If mesh/filter is later required:
- characterize pressure drop;
- include it explicitly in CFD.

## 13. Wall-gap path
Nominal:
4 mm.

The outlet discharges into the rear wall gap and then to room edges.

Do not place a decorative rear lip that traps the hot plume above the outlet.

Wall-gap sweep remains:
3 / 4 / 5 mm.

## 14. Shell structural compensation
Vent banks weaken ASA shell but shell is not the primary wall-mount structure.

Still provide:
- local perimeter ribs around slot banks;
- staggered slot pattern;
- >=3 mm webs;
- radiused slot ends;
- no rib that blocks slot exit.

Do not transfer primary mount loads into vented ASA.

## 15. Water/dust interpretation
This product is not currently specified as an IP-rated sealed enclosure.

Hidden downward/rear-facing slots reduce direct ingress exposure but do not constitute an IP rating.

No IP claim without dedicated ingress design/test.

## 16. Acoustic implications
The DML perimeter remains sealed.

Vent path is:
room rear/lower -> labyrinth -> electronics cavity -> rear/upper labyrinth -> wall gap -> room.

It does not intentionally couple front and rear faces of the DML.

Acoustic validation shall check:
- vent whistle/chuffing;
- cavity resonance;
- leakage around DML;
- rear-slot radiation.

## 17. CFD cases updated
Inlet effective-area sweep:
- 600 mm2 legacy minimum
- 900 mm2 preferred threshold
- 1080 mm2 Rev.B seed
- 1200 mm2 stress/improved option.

Outlet:
- 750 mm2 legacy minimum
- 1000 mm2 preferred threshold
- 1080 mm2 Rev.B seed
- 1500 mm2 improved option.

## 18. Installed-cable case
Run CFD with:
- Ethernet cable present;
- 24 V cable present where applicable;
- harness sweep occupying worst credible lower path.

Rev.B inlet banks are outside the central service recess specifically to reduce sensitivity to cable blockage.

## 19. Geometry assertions
C246 gross inlet >=1440 mm2.
C247 effective inlet seed >=1080 mm2 using 0.75 CAD factor.
C248 gross outlet >=1350 mm2.
C249 effective outlet seed >=1080 mm2 using 0.80 CAD factor.
C250 service recess not credited toward guaranteed inlet.
C251 ENV chamber not credited toward main inlet.
C252 inlet has no direct DML line of sight.
C253 outlet has no direct cavity-to-room line of sight where baffle geometry is feasible.
C254 inlet path has >=2 direction changes.
C255 DML perimeter remains sealed.
C256 slot ends radiused.
C257 no continuous shell tear hinge.
C258 inlet banks clear primary lower structural nodes.
C259 outlet banks clear cleat bosses/load islands.
C260 outlet banks preserve ESP32 RF keep-out.
C261 installed-cable CFD case defined.
C262 no dense filter baseline.
C263 no IP rating inferred.
C264 wall-gap plume exit remains open.
C265 CFD uses real slot geometry, not equivalent area only.

## 20. Release interpretation
Rev.B vent geometry solves the reduced-order area concern at the CAD-target level:
- gross inlet 1440 mm2;
- estimated effective inlet 1080 mm2;
- gross outlet 1350 mm2;
- estimated effective outlet 1080 mm2.

The inlet is deliberately gross-larger than the outlet because its assumed blockage factor is worse.

CFD remains authoritative for pressure loss and natural-convection performance.

Status: **REAR_SHELL_REV_B_VENTS_1440_GROSS_IN_1350_GROSS_OUT / 1080_EFFECTIVE_SEED_BOTH / C01_TO_C265 / CFD_REQUIRED**.
