# AudioPicture V2.2 retention hard-stack tolerance sweep Rev.AW
# Sensitivity study only: process capability not yet qualified.
import json,itertools
# Nominal global planes
SHELL_INNER=37.8
SEAT_H=1.8
FRAME_REAR=35.0
nom_gap=(SHELL_INNER-SEAT_H)-FRAME_REAR
# Engineering sensitivity sweeps, explicitly NOT manufacturing tolerances.
# Positive shell shift increases gap; positive frame shift toward wall/rear increases frame Z and reduces gap.
shell_shift=[-0.30,0.0,0.30]
seat_h_error=[-0.20,0.0,0.20]
frame_z_shift=[-0.30,0.0,0.30]
rows=[]
for ds,dh,df in itertools.product(shell_shift,seat_h_error,frame_z_shift):
 seat_front=(SHELL_INNER+ds)-(SEAT_H+dh)
 frame=FRAME_REAR+df
 gap=seat_front-frame
 rows.append(gap)
gmin=min(rows);gmax=max(rows)
# Candidate nominal limiter heights. Positive residual = shell/frame gap remaining after limiter.
cands=[]
for L in [0.6,0.8,1.0,1.2,1.4]:
 residual=[g-L for g in rows]
 cands.append({"limiter_mm":L,"residual_min_mm":min(residual),"residual_max_mm":max(residual),
 "interference_possible":min(residual)<0,"free_gap_possible":max(residual)>0})
print(json.dumps({"nominal_gap_mm":nom_gap,
"sensitivity_inputs_mm":{"shell_plane_shift":shell_shift,"seat_height_error":seat_h_error,"frame_rear_z_shift":frame_z_shift},
"resulting_gap_range_mm":[gmin,gmax],"candidate_limiter_sweep":cands,
"interpretation":"No fixed limiter height can guarantee both zero interference and zero free gap across this unqualified +/- sensitivity stack.",
"required_architecture":"use a controlled compliant interface or post-process/measure matched hard spacer; do not release a fixed 1.0 mm hard spacer yet.",
"limitations":["input sweeps are engineering sensitivity seeds, not measured process capability","fastener preload not modeled","ASA creep not modeled","PC-CF insert compliance not modeled"]},indent=2))
