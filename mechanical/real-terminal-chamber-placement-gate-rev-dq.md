# AudioPicture V2.2 — real four-bank terminal chamber placement gate Rev.DQ

Status: **AUTHORITATIVE_BK_AND_FRAME_C_RECOVERED / Z_CONFLICT_IDENTIFIED / REAL_PLACEMENT_AUDIT_DEFINED**

The current authoritative CAD sources were recovered from the repository:
- rear shell: generate_rear_shell_frame_aware_master_rev_bk.py;
- coarse PC-CF frame kernel: generate_rear_frame_g2_rev_c.py.

A direct copy of normalized Rev.DO is not mechanically legal by default.

Reason:
- normalized terminal chamber lower Z = 34.0 mm;
- coarse PC-CF frame occupies Z = 27..35 mm where its XY material exists.

Therefore any chamber volume in a frame-occupied XY region between Z34 and Z35 would create a hard collision/bridge.

Rev.DP screens the four actual vent-bank envelopes against the real Rev.C frame kernel while sweeping chamber lower Z upward.

Candidate lower Z values:
34.0, 35.1, 35.3, 35.5, 35.8, 36.0 mm.

For each bank the audit reports:
- conservative occupied-envelope/frame intersection volume;
- remaining local throat proxy using the Rev.DO 16 mm exit / 1 mm wall assumption;
- whether the placement is collision-free with nonzero throat.

This is deliberately conservative. Envelope failure may still allow a sculpted local topology, but envelope pass is sufficient to proceed to detailed solid construction.

Checks:
C1691 authoritative Rev.BK shell generator recovered.
C1692 authoritative Rev.C frame generator recovered.
C1693 normalized Z34 chamber conflicts with frame Z27..35 wherever XY overlaps.
C1694 blind direct mapping rejected.
C1695 four-bank conservative placement audit Rev.DP defined.
C1696 lower-Z sweep 34.0..36.0 defined.
C1697 nonzero throat and zero frame overlap required.
C1698 detailed real solid gated by placement audit.

Status: **MECHANICAL_REV_DQ / REAL_TERMINAL_CHAMBER_PLACEMENT_AUDIT_NEXT / C01_TO_C1698**.
