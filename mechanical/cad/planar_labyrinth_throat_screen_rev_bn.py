# AudioPicture V2.2 planar labyrinth throat screen Rev.BN
# Reduced-order geometry only; NOT CFD.
import json, math
GAP_Z=2.8
# New Rev.BK banks: left only; right symmetric.
# inlet bank projected extents from two x columns and 3 y groups
IN_BANK=(17.,27.,14.,150.)
OUT_BANK=(17.,62.,315.,346.)
# Candidate planar baffle architecture uses vertical ribs bonded to shell inner face,
# protruding only H into the 2.8 mm shell-frame nominal gap.
# H is swept; remaining under-rib bypass height = GAP_Z-H.
H_SWEEP=[0.8,1.0,1.2,1.4]
# two staggered ribs per bank; free lateral openings selected deliberately broad.
# These are throat widths normal to local flow, not production dimensions.
IN_FREE_WIDTH=14.0
OUT_FREE_WIDTH=20.0
results=[]
for h in H_SWEEP:
 rem=GAP_Z-h
 results.append({"baffle_height_mm":h,"remaining_z_bypass_mm":rem,
 "inlet_lateral_throat_proxy_mm2":IN_FREE_WIDTH*GAP_Z,
 "outlet_lateral_throat_proxy_mm2":OUT_FREE_WIDTH*GAP_Z,
 "under_baffle_bypass_proxy_mm2_per_mm_length":rem,
 "note":"lateral throat proxy uses full nominal Z gap; under-baffle value shows leakage path beneath a shell-mounted rib"})
print(json.dumps({"gap_z_nominal_mm":GAP_Z,"left_bank_extents":{"inlet":IN_BANK,"outlet":OUT_BANK},
"architecture":"two staggered shell-mounted planar ribs per bank; force two XY turns without spanning full 2.8 mm Z gap",
"sweep":results,
"limitations":["not CFD","no pressure-loss coefficient","frame exact local topology not imported","baffle height cannot be frozen until local Z/tolerance/process measurements exist","acoustic attenuation not predicted"]},indent=2))
