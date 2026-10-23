# AudioPicture Rev.E — DML panel specification

Status: **DESIGN_SPEC / NOT_AN_ACOUSTIC_MEASUREMENT**  
Authority: [`docs/architecture/v2.2-rev-e-dml-30mm.md`](../docs/architecture/v2.2-rev-e-dml-30mm.md)

## 1. Goal

A wall-hung mono radiator of **320 × 400 × ≤ 30 mm** with high-end bending-wave performance: deep usable bass without cones, wide coverage, and a decorative fabric face.

Commercial north star (not a clone): Amina Sapphire375 class — twin specialized exciters on a phenolic honeycomb diaphragm, ~50 Hz usable, ~34 mm invisible panel. Rev.E must do this as a **picture** (fabric, not plaster) and must integrate the room-node electronics inside the same envelope.

## 2. Diaphragm

| Parameter | Target |
| --- | --- |
| Outer product | 320 × 400 mm |
| Radiating aperture | ≥ 280 × 360 mm (frame lip ≤ 20 mm per side) |
| Construction | Phenolic / aramid honeycomb core with thin composite skins, or proven equivalent “Symphony Cell” class |
| Areal density | Low enough that exciter moving mass does not dominate driven modes |
| Damping | Built-in viscoelastic or constrained layer — enough to kill long ringing, not so much that bass dies |
| Front | Acoustically open fabric (ShowTex 3838 class); printable; no contact with panel at max drive |

Candidate matrix for first FEA + coupon set:

1. phenolic honeycomb + glass/epoxy skins;
2. aramid honeycomb + carbon/epoxy skins (stiffer, watch density);
3. aluminium honeycomb + thin composite (only if FEA shows controllable modes).

## 3. Exciters

| Role | Class | Placement rule |
| --- | --- | --- |
| EX_LF | LowFreq DML — large coil, spiderless coupler, high stroke for panel bass | From modal FEA; typically lower third, offset from symmetry lines |
| EX_WB | Wideband DML / BMR-class | From modal FEA; typically upper / offset; not stacked on EX_LF |

**Forbidden as Rev.E baseline:** generic consumer exciters whose magnet mass overwhelms the panel (Rev.A failure). Catalog Dayton DAEX may be used only as temporary laboratory actuators, never as the production acoustic claim.

OEM path: engage Tectonic / Amina-class suppliers or commission custom exciters with disclosed Thiele-small-like and mechanical coupler data.

Depth: coupler + motor must fit the thickness budget in Rev.E §1.1.

## 4. Frame and mounts

- Perimeter frame carries hang loads; panel floats on tuned compliant mounts.
- Mounts must not pin the panel into a piston-only regime that kills DML behaviour, nor leave it so free that it buzzes on the frame.
- French cleat on the rear: rated for product mass + **3×** static pull. First mass estimate after electronics CAD; until then design for **≥ 5 kg** working load.

## 5. Rear cavity

Shallow sealed volume behind the panel (remainder of 30 mm). Purpose: control rear radiation into the wall gap, reduce dipole cancellation at low frequency when hung with a small stand-off, and host the service rail. Not a classical bass-reflex box.

Wall mounting: product rear stands off the wall by a designed gap (cleat geometry); treat wall as infinite baffle in the acoustic model once gap is known.

## 6. Coexistence with sensors (non-negotiable)

Cutouts and windows are allowed only where FEA says modal impact is acceptable:

| Sensor | Mechanical note |
| --- | --- |
| 4-mic array | Thin flex or PCB strip on **frame**, not on high-velocity panel centre; acoustic ports to the room |
| Radar 60 GHz | Edge window, RF-transparent cover; keep metal frame out of the beam |
| SHT45 | Room vent on frame; thermal isolation from amp/PoE |
| OPT3004 | Optical slot on frame / corner |
| Mute / action | Edge buttons; rods must not chatter against panel |

## 7. Verification sequence

1. FEA modal map → proposed exciter coordinates.
2. Bare panel + exciters: impedance, near-field, laser/vibrometry if available.
3. Add fabric: insertion loss and HF tilt.
4. Add frame + electronics rail (powered idle): buzz hunt.
5. Factory DSP curve; limiter validation.
6. Multi-unit room delay/level with HA planner.

Evidence folder for this work: `evidence/rev-e/` (create with first FEA export).

## 8. Relationship to prior mechanical work

Historical DML FEA (Rev.FI and earlier) and P1 84 mm cone CAD remain in the tree as archive. They do **not** govern Rev.E geometry. New CAD for Rev.E starts from this document and `p1_params`-class params replaced by a `rev-e` parameter set when modelling begins.
