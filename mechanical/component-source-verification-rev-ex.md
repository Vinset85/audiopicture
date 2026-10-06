# Source verification Rev.EX — 2026-09-30

Classification: manufacturer data / calculated checks; no production release.

## PC-CF provenance correction
The current [Prusament product page](https://prusament.com/materials/prusament-pc-blend-carbon-fiber/)
links to [TDS version 2.0-OY, 2023-04-19](https://prusament.com/wp-content/uploads/2023/04/TDS_Prusament-PCCF_2023_EN.pdf).
It reports density 1.22 g/cm3 and printed tensile moduli 2.6/3.2 GPa for its
specified horizontal/vertical-xz specimen process. The old Rev.L statements
1.9/2.0 GPa are not supported by this current linked source. Preserve 1900 MPa
only as the explicitly assumed screening modulus used in existing
runs; do not attribute it to this TDS or silently replace past solver inputs. A value below two catalog moduli is not a guaranteed conservative bound for a different process, print direction or temperature.
No complete orthotropic card, hot curves, directional allowables or product
process qualification follows from the TDS. No strength margin is released.

The Rev.EU.4 solid volume is 346084.3665 mm3. Multiplication by the catalog
1.22 g/cm3 gives **422.223 g** for a homogeneous full-density interpretation,
above the frame target 250 g. This is a calculated catalog-density estimate,
not a weighed printed part. Reducing infill would invalidate the homogeneous
FEA assumption and requires a new effective-material/model qualification.

## Silvertel Ag53024
Authority: [Ag53000 datasheet V1.1, 2026-06-22](https://silvertel.com/images/datasheets/Ag53000-Datasheet.pdf),
selector page 3 identifies Ag53024. Do not use Ag5324/Ag5300 geometry.
The package drawing, page 17, was visually inspected. Maximum dimensions A/B/C
are 58.28 / 15.02 / 13.00 mm; D/E maxima 1.76 / 1.78 mm describe the substrate
and opposite protrusion. A conservative isolated module bounding box may use
58.28 x 16.54 x 18.40 mm including the 3.38 mm maximum pin projection. The host
PCB seating plane and orientation must be explicit; pin height is not body
height above the host PCB. The body-height allowance of 15.00 mm is not exact:
B maximum is 15.02 mm. No final global placement is frozen by this envelope.

For Ag53024 the output-capacitance table on page 15 specifies 180/220/330 uF
minimum/typical/maximum. The generic typical-connection discussion mentions
470 uF, so the variant-specific table must be preserved in review. The downstream
470 uF audio bulk alone exceeds 330 uF if the source-switch path makes it directly
visible to the module. This is a **stability/inrush qualification gate**, not proof
of measured instability. Analyze total connected capacitance and source-switch
sequence, then validate startup/load steps on the real module. Do not assume
that adding the local 220 uF capacitor automatically closes stability.

## RJ45 and USB
[TE 2-1734264-1](https://www.te.com/en/product-2-1734264-1.html) provides its exact
customer drawing and STEP download. STEP retrieval here returned HTTP 403;
no import is claimed. Manufacturer lists 13.2 mm connector height and 1.6 mm
recommended PCB. Plug/boot/latch and insertion envelopes remain separate.
[GCT USB4085](https://gct.co/connector/usb4085) identifies USB4085-GF-A and a
3.46 mm profile, 9.17 mm body length, 2.10 mm shell stake. Exact variant/footprint,
full manufacturer drawing import and global installation remain OPEN.

## PoE control contract
The repository's frozen application continuous budget is 22.5 W. The old
firmware emergency description near 23 W violated that policy. Rev.EW accepts
no configured PoE emergency ceiling above 22.5 W and shuts the amplifier down
at that threshold in its host-tested control core. This is not evidence that
hardware transient power never exceeds the limit; latency/energy, amplifier
actuation and real load tests remain required.

## Audio MPN reconciliation — Rev.EY, 2026-10-01
The BOM retained generic descriptions despite two existing selections in the
repository. C901 now names Panasonic EEU-FR1V471B, matching
`hardware/audio/pvdd-bulk-packaging-rev-a.md`. The [manufacturer model page](https://industrial.panasonic.com/ww/products/pt/aluminum-cap-lead/models/EEUFR1V471B) identifies 470 uF, 35 V, diameter 10 mm, length 16 mm, lead pitch 5 mm. The
selected horizontal lead forming, actual ripple and thermal life remain unverified.

L901–L904 now name Coilcraft XAL7050-103MEC, matching the existing audio selection.
The [manufacturer datasheet](https://www.coilcraft.com/getmedia/13a991b3-4273-4be3-81ba-f3cf372b4691/xal7050.pdf) lists **7.1 A typical saturation current**, not 12.1 A.
12.1 MHz is the typical self-resonant frequency. The earlier document conflated
these columns and is corrected. Catalog DCR is 25/29 mOhm typical/maximum;
6.3/8.5 A RMS correspond to 20/40 degree C rise in the manufacturer's conditions.
None of these values establish loss or temperature inside AudioPicture.

The CSV round-trip preserved 74 rows and all cells except the MPN/status of these
two references. There remain **26 active rows without an exact orderable MPN**
and 5 optional/removed rows. Native circuit/layout verification remains absent.
