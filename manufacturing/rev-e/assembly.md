# AudioPicture Rev.E — assembly procedure

Status: **PROCEDURE_DRAFT / FIRST_ARTICLE_REQUIRED**

## 0. Safety

Unpowered assembly until §6. ESD strap for MAIN and voice. Do not drive exciters without the limiter curve loaded.

## 1. Frame and hanger

1. Inspect `AP-E-FRAME` for flash, flatness, rail integrity.
2. Install French cleat hardware; torque per fastener spec (TBD after mass weigh).
3. Fit compliant panel mounts MT1–MT8 in FEA-approved locations only.

## 2. Panel and exciters

1. Bond or screw EX_LF and EX_WB to panel at coordinates from `rev_e_params.json` (update after vibrometry).
2. Verify depth: fabric plane to rear of motor ≤ budget in Rev.E §1.1.
3. Drop panel onto mounts; confirm no fabric contact at ± rated stroke proxy (gentle push).
4. Route exciter leads to service rail with strain relief; no lead glued across panel antinodes.

## 3. Electronics

1. Install MAIN in service rail; antenna keep-out clear.
2. Connect Ethernet/PoE edge, USB-C, DC jack as fitted.
3. Mate voice flex / XVF stack; verify mute switch kills mic rail.
4. Mount mic bar, radar window module, SHT45 vent, OPT3004 island on frame.
5. Connect INA228 path; no reverse polarity.

## 4. Fabric

1. Stretch ShowTex 3838 class over front; no wrinkles over aperture.
2. Confirm optical and mic ports not occluded beyond design.

## 5. Closure

1. Rear skin / cover; label UUID QR and regulatory marks (after certification).
2. Weigh unit; record mass for hanger derating.

## 6. First power (bench only)

1. External 24 V through fixture or jack; PoE later.
2. Flash diagnostic/product firmware via USB-C.
3. Confirm `/api/v1/info` and sensors.
4. Do **not** enable amplifier until factory acoustic station (§ factory-test.md).
