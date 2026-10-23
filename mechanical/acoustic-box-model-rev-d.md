# AudioPicture Rev.D — first box model

Status: **MODEL_ONLY / NOT_AN_ACOUSTIC_MEASUREMENT**

Source: `tools/acoustic_box_model_rev_d.py`. Output: `evidence/rev-d/box-model.json` and the generated firmware header `firmware/components/room_audio/include/ap_model_curve_rev_d.h`. Re-run from the repository root:

```sh
python3 tools/acoustic_box_model_rev_d.py
```

## Model

Lumped electro-mechano-acoustic circuit: ND91-4 woofer, one sealed box, two ND90-PR passives, box leakage QL 7, half-space radiation at 1 m (the wall is the baffle), small signal. The model includes voice-coil inductance and does not include cone breakup, cabinet panel modes, cloth loss or room gain. Results are trusted to **500 Hz**. The tweeter is not modelled. Its pad comes from the sensitivity difference only.

## Net volume

Inner shell 300 × 380 × 53.3 mm = 6.08 L gross.

| Deduction | L |
| --- | ---: |
| Sealed electronics pocket, 300 × 70 mm | 1.12 |
| Two vertical braces | 0.38 |
| Hanger and cable recess | 0.20 |
| Driver bodies inside the box | 0.25 |
| **Net driver air** | **4.12** |

Magnet-to-rear-wall clearance: 4.3 mm. That is inside the 84 mm body.

## Tuning

The selection rule is DSP-aware. It maximizes the flat level reachable across 55–300 Hz, limited by woofer Xmax 4.6 mm, passive Xmax 9 mm and the 30 W rated voltage, with a DSP boost of at most 6 dB.

Without added mass the raw F3 is 69 Hz.

| Passive load | Flat max level, 55–300 Hz | DSP boost needed |
| --- | ---: | ---: |
| Optimum, 4.9 g each | 89.6 dB | 4.9 dB |
| **Build: one supplied Dayton disk, 7.3 g each** | **88.1 dB** | **5.5 dB** |

Heavier passives open a dip near 100 Hz. Raw F3 alone is the wrong target, so the Rev.D "F3 55–60 Hz before DSP" goal is replaced by the DSP-aware rule above.

Volume sensitivity of the flat level: 2.5 L → 91.0 dB, 3.0 L → 90.5 dB, 3.5 L → 90.1 dB, 4.1 L → 89.6 dB, 4.5 L → 89.4 dB. Larger volume buys extension, not level. Keep at least 3.5 L.

Minimum impedance 20 Hz–3 kHz: 4.39 Ω.

## DSP on the build tuning

| Stage | Setting |
| --- | --- |
| Subsonic | Butterworth 4th order, 45 Hz |
| Bass EQ | one peaking filter, 66.9 Hz, Q 1.16, +6.0 dB |
| Crossover | Linkwitz–Riley 4th order, 3 kHz, active |
| Tweeter pad | −5.0 dB |

Modelled woofer branch after DSP: **55–500 Hz within −0.7/+0.8 dB**, **F3 50.6 Hz**. Maximum flat level at 1 m: **88.4 dB**, limited by excursion at 65.9 Hz. Above 100 Hz the woofer alone reaches **91.1 dB** without boost, and 90 dB at 100 Hz needs 7.5 Vrms, inside the 11 V rating.

## Consequences

- The Rev.D objective of 90 dB from 100 Hz is met without bass boost. With the +6 dB bass EQ active the box tops out near 88 dB. A **dynamic bass limiter** must reduce the 67 Hz boost as level rises. It is still open.
- Order two ND90-PR and mount one supplied 7.3 g disk on each. Bench measurement decides the final mass.
- The bench must confirm the impedance curve, near-field response, excursion at the limiter threshold, and the tweeter pad.
