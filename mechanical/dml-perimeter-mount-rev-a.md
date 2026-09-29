# AudioPicture V2.2 Rev.A — DML compliant perimeter mount

Status: **MOUNT_ARCHITECTURE_BASELINE_FROZEN / EXACT_FOAM_GRADE_AND_COMPRESSION_FEA_GATE**

## 1. Function
The DML panel shall be retained by a compliant perimeter interface, not hard-clamped directly to the printed enclosure.

The mount must:
- locate and retain the 300 x 380 mm DML assembly;
- provide controlled normal preload;
- permit panel-edge motion needed by the DML;
- reduce structure-borne transfer into the rear frame and VOICE support;
- tolerate manufacturing variation;
- remain compatible with the 40 mm maximum product depth.

## 2. Material family baseline
Primary candidate family: **PORON 4701-30 very-soft polyurethane foam** or a mechanically equivalent characterized microcellular polyurethane.

Rogers publishes PORON 4701-30 as a very-soft formulation intended for vibration management/sealing with low compression-set behavior. Exact thickness/density variant is not production-frozen until the load-deflection curve for the selected stock is checked against the final panel/frame preload.

Do not substitute generic EVA, silicone foam or unnamed TPU solely by Shore hardness. Static compression force, compression set, temperature/humidity behavior and dynamic loss are the relevant release properties.

## 3. Geometry baseline
Use a continuous perimeter support path for sealing/retention but avoid a broad rigid bonded flange.

Initial section for CAD/FEA:
- nominal foam width: 6 mm;
- nominal uncompressed thickness: 2.0 mm;
- target installed compression: 15..25%;
- nominal design point: 20% = 0.40 mm compression;
- DML structural edge overlap/support land: approximately 5..6 mm;
- hard frame stop shall limit over-compression during assembly.

The foam shall not be relied upon as the sole drop/safety retention mechanism. Add hidden mechanical capture that does not hard-preload the active panel in normal operation.

## 4. Segmentation and bridges
The acoustic support behaves as a compliant continuous perimeter. Structural hard features shall be sparse and clearance-gapped in normal operation.

No hard bridge is permitted from the active DML panel to:
- PCB-B VOICE carrier;
- microphone array support;
- radar carrier;
- environmental chamber.

Harnesses crossing the panel/frame interface require flexible service loops and strain relief on the frame side.

## 5. FEA parameterization
Until exact material dynamic data is available, sweep the perimeter as distributed translational/rotational stiffness rather than assigning a guessed modulus.

Three calibrated cases:
- SOFT = lower load-deflection envelope;
- NOMINAL = selected foam at approximately 20% compression;
- STIFF = upper tolerance/aging/compression envelope.

The mount model shall include normal and in-plane compliance. Rotational restraint shall emerge from mount width/geometry or be represented by an equivalent spring where necessary.

## 6. Compression design rule
Target compression is 15..25%, with 20% nominal.

Reject a stack-up if worst-case tolerances drive any substantial perimeter segment below 10% compression or above 30% compression in normal assembly.

Use hard stops in the rear-frame geometry so screw/clip force cannot crush the foam beyond the designed gap.

## 7. DML edge condition
Do not bond both DML skins rigidly into a deep enclosure groove.

Preferred section:
front cosmetic/fabric frame
-> free active-panel field
-> narrow panel edge land
-> compliant foam interface
-> rear structural frame
-> hard over-travel stop with clearance at nominal assembly.

The visible fabric/front frame shall not become a second rigid DML clamp.

## 8. VOICE isolation relationship
PCB-B VOICE shall mount to the rear structural frame through its own isolation system, mechanically downstream of the DML perimeter foam.

Do not share DML clamp screws/posts with the microphone carrier.

The full harmonic FEA shall report reaction force transmitted through the perimeter in the microphone-array frequency band and at dominant DML modes.

## 9. Depth allocation baseline
Within the 40 mm maximum product depth, reserve approximately:
- front fabric + cosmetic allowance: 1.0..2.0 mm;
- DML sandwich A1: about 6.0 mm before adhesive/fabric refinements;
- rear exciter projection: use actual selected-exciter CAD, approximately 20.5 mm legacy reference;
- local rear clearance over exciter: >=2 mm nominal;
- rear shell/wall and tolerances: remaining budget.

This shows why electronics must occupy zones between/around exciter volumes rather than stacking directly behind the tallest exciter.

No production depth stack is frozen until the successor-exciter mechanical drawing and rear-shell CAD are reconciled.

## 10. Environmental and durability gates
Before production freeze validate:
- compression set at sustained installed compression;
- temperature/humidity aging;
- adhesive-backed foam creep if PSA is used;
- buzz/rattle under sweep;
- panel centering after thermal cycling;
- service/reassembly behavior;
- flammability requirement for the final market.

## 11. Release gate
Exact foam grade, thickness and perimeter geometry may freeze only after:
1. supplier load-deflection curve is mapped into FEA spring stiffness;
2. tolerance stack confirms 10..30% worst-case compression;
3. Candidate A/B modal comparison includes the mount;
4. structure-borne force at VOICE support is acceptable;
5. enclosure hard-stop geometry is frozen.
