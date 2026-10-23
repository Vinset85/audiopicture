# Rev.E OEM RFQ pack — DML panel and exciters

Status: **READY_TO_SEND / NOT_A_PURCHASE_ORDER**

Send this pack to at least two suppliers in each category (panel laminate, LowFreq exciter, wideband/BMR exciter). Prefer partners with shipping DML/BMR products (Tectonic Audio Labs class, Amina-class OEM, specialized transducer houses).

## 1. Product summary

AudioPicture is a **320 × 400 × ≤ 30 mm** wall picture that is also a mono loudspeaker and a Home Assistant room node. Acoustics are **dual-exciter DML**. Target: ~50 Hz–20 kHz after DSP, ≥95 dB short-term at 1 m, decorative fabric face (no plaster).

Authority: `docs/architecture/v2.2-rev-e-dml-30mm.md`.

## 2. Panel RFQ

| Item | Requirement |
| --- | --- |
| Radiating aperture | 284 × 364 mm (±1 mm) |
| Thickness | 10 mm nominal (8–12 mm acceptable if stack still ≤30 mm) |
| Construction | Phenolic or aramid honeycomb + thin composite skins |
| Areal density | Target ~1.5–2.2 kg/m² (disclose measured) |
| Damping | Loss factor ≥ 0.03 midband or supplier damping recipe |
| Qty prototype | 10 panels, 3 material variants if available |
| Qty production intent | 500 / year year-1 (indicative) |
| Deliverables | Material datasheet, modal test or FEA, flatness, moisture rating |

## 3. Exciter RFQ

### EX_LF (bass)

| Item | Requirement |
| --- | --- |
| Class | LowFreq DML / spiderless coupler preferred |
| Depth behind panel | ≤ 14 mm |
| Moving mass | ≪ panel modal mass; disclose Mms |
| Z | 4 Ω nominal |
| Power | ≥ 30 W RMS thermal with coupler |
| Qty proto | 20 |

### EX_WB (mid/high)

| Item | Requirement |
| --- | --- |
| Class | Wideband DML or BMR |
| Depth | ≤ 14 mm |
| Z | 4 Ω nominal |
| Power | ≥ 15 W RMS |
| Qty proto | 20 |

Ask for coupler drawings, recommended drive-point guidance, and Thiele–Small / mechanical parameters.

## 4. NDA / IP

Buyer owns product industrial design and DSP curves. Supplier retains transducer IP. Dual-source preferred before tooling freeze.

## 5. Evaluation criteria

1. Measured or credible modelled extension to ~50 Hz on a panel of our size.
2. Depth compliance.
3. Sample lead time ≤ 8 weeks.
4. Unit price at 500 and 2000 / year.
5. Willingness to support placement FEA / vibrometry.
