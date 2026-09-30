# AudioPicture V2.2 — service recess architecture Rev.AL

Status: **SERVICE_REGION_ARCHITECTURE_PASS / PARAMETRIC_OPENING_SEED_ONLY / CONNECTOR_SWEEP_RELEASE_OPEN**

## Repository evidence
A repository search did not identify a frozen RJ45 connector MPN, plug/boot mechanical drawing, latch swept volume, or exact 24 V / USB connector envelope.

Therefore connector-specific opening dimensions are not frozen.

## Frozen service region
Existing architecture:
X100..220 / Y20..48.

The service recess:
- is not credited as thermal inlet;
- must preserve ordinary Ethernet plug/latch access;
- may serve 24 V / USB service paths as applicable;
- must use radiused transitions;
- must not interfere with inlet banks or anti-lift.

## Rev.AK executed architecture seed
Parametric opening seed:
- center X160 / Y34;
- 72 x 16 mm;
- R3 corners;
- bbox X124..196 / Y26..42.

Land remaining inside service region:
- left 24 mm;
- right 24 mm;
- bottom 6 mm;
- top 6 mm.

Executed checks:
- valid one-solid panel kernel;
- 12 inlet intersections = 0 mm3;
- conservative anti-lift envelope intersection = 0 mm3;
- opening entirely inside frozen service region.

## Critical interpretation
72 x 16 mm is **not a production-frozen service opening**.

It is an architecture seed used to prove:
1. a useful central opening can fit inside the service region;
2. reinforcement land remains available;
3. the executed inlet layout is unaffected;
4. the conservative anti-lift region can remain independent.

Before release, replace/validate the seed against:
- exact board RJ45 MPN and position;
- ordinary Cat5e/Cat6 plug body;
- latch access;
- selected boot style or explicit no-boot requirement;
- cable bend/sweep;
- exact 24 V connector;
- exact USB service connector.

## Preferred tunnel concept
Use a passive internal guide/tunnel rather than extending Ethernet electrically.

The tunnel should be a separate parametric feature tied to the final connector sweep. Do not freeze its Z/section from generic RJ45 dimensions.

The existing global service corridor Z22..36 remains the packaging envelope, not a solid tunnel definition.

## Checks
C1061 repository searched for RJ45/connector mechanical definition.
C1062 no frozen RJ45 MPN/drawing found.
C1063 no plug/boot/latch sweep found.
C1064 no exact 24 V/USB envelope found.
C1065 service region X100..220/Y20..48 retained.
C1066 Rev.AK opening seed 72x16 R3 generated.
C1067 opening seed fully inside service region.
C1068 24 mm side reinforcement land retained.
C1069 6 mm upper/lower reinforcement land retained.
C1070 inlet intersections zero.
C1071 conservative anti-lift intersection zero.
C1072 service opening not credited as thermal inlet.
C1073 72x16 explicitly not production frozen.
C1074 passive Ethernet tunnel philosophy retained.
C1075 exact connector/plug/cable sweep required before release.

Status:
**SERVICE_RECESS_REV_AL_ARCHITECTURE_PASS / 72X16_R3_REPLACEABLE_SEED / INLET_CLEAR / ANTILIFT_CLEAR / CONNECTOR_MPN_AND_SWEEP_REQUIRED / C01_TO_C1075**.
