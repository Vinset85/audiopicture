# AudioPicture V2.2 retention compliant-interface geometry screen Rev.AY
# Architecture screen only; material, preload and production tolerances open.
import json,itertools,math
SEAT_D=10.0
SCREW_CLASS="M3"
# Parametric concentric stack seed
CLEAR_HOLE_D=3.6      # CAD seed, not released
HARD_STOP_OD=6.0      # tubular/shoulder envelope seed
COMPLIANT_OD=9.0      # annular compliant interface seed
LAND_RADIAL=(SEAT_D-COMPLIANT_OD)/2
ANNULUS_RADIAL=(COMPLIANT_OD-HARD_STOP_OD)/2
# Current dimensional sensitivity gap from Rev.AX
GAPS=[0.2,1.0,1.8]
# Screen candidate compliant free thicknesses and hard-stop heights.
# Compression = free thickness - actual gap, when positive.
rows=[]
for tfree,hstop in itertools.product([1.0,1.5,2.0],[0.6,0.8,1.0]):
 comp=[max(0,tfree-g) for g in GAPS]
 # hard stop caps geometric closure; this is topology only, not force model.
 rows.append({"compliant_free_mm":tfree,"hard_stop_height_mm":hstop,
 "compression_at_gap_0p2_1p0_1p8_mm":comp,
 "can_contact_at_max_gap":tfree>=max(GAPS),
 "hard_stop_below_nominal_gap":hstop<1.0})
assert CLEAR_HOLE_D < HARD_STOP_OD < COMPLIANT_OD <= SEAT_D
print(json.dumps({"seat_diameter_mm":SEAT_D,"screw_class":SCREW_CLASS,
"clearance_hole_d_seed_mm":CLEAR_HOLE_D,"hard_stop_od_seed_mm":HARD_STOP_OD,
"compliant_od_seed_mm":COMPLIANT_OD,"outer_land_radial_mm":LAND_RADIAL,
"compliant_annulus_radial_width_mm":ANNULUS_RADIAL,
"gap_sensitivity_mm":GAPS,"candidate_screen":rows,
"preferred_topology":"M3 clearance hole + concentric hard-stop sleeve/shoulder + annular compliant washer",
"release_state":"geometry architecture only; no material, force, torque, hard-stop height or hole diameter released",
"limitations":["3.6mm clearance is CAD seed only","no compression modulus/curve","no creep model","no screw-head/washer selected","actual gap capability unmeasured"]},indent=2))
