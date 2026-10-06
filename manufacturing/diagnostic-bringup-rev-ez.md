# Rev.EZ diagnostic bring-up — plan, not executed hardware tests

This supplements P14/P15 in the physical qualification plan. All steps are
**NOT_RUN**. No device has been flashed by the digital build. Use a current-
limited bench supply and qualified native PCB after unpowered inspection.
Exact current limits must come from the approved rail/load budget; this plan
does not invent one. Preserve board revision, UUID, instruments, uncertainties,
firmware hashes, raw traces and observed results for every unit.

1. **Before firmware:** measure reset/boot/fault GPIO levels and controlled
   power-up rails. Amplifier, microphone power, voice processor and radar must
   remain disabled until their dedicated bring-up. PASS requires actual
   hardware bias during reset and boot; application GPIO initialization alone
   is insufficient. GPIO0/CHIP_PU ROM recovery must work with a bad application.
2. **Memory and identity:** verify physical flash size and octal PSRAM;
   read `/api/v1/info`, power-cycle and confirm the same nonempty UUID. An NVS
   fault must produce a traceable fault without silently erasing identity.
3. **Network:** independently bring up W5500 Ethernet and provisioned Wi-Fi
   station; record DHCP, mDNS, disconnect/reconnect and address changes.
   Home Assistant must discover one unit per UUID, reject a mismatched identity,
   recover after address changes, and stop polling after unload. Read-only HTTP
   is intended for a trusted local network; commissioning/security work is open.
4. **Sensors:** verify physical addresses 0x44, 0x45 and 0x40; compare raw SHT45
   temperature/humidity and OPT3004 lux against calibrated references. Sensor
   offset/uncertainty and fabric calibration require the final chamber/tunnel.
   Record raw and corrected values separately. Do not count catalog accuracy as
   measured assembly accuracy, and do not use SHT45 as a junction thermometer.
5. **Communication faults:** disconnect each device, interrupt the I2C bus and
   reset individual devices in a controlled fixture. API values must become
   unavailable/null on failed acquisition or after the 90 s freshness limit;
   no old value may be labelled current. Bound recovery and log driver errors.
   Firmware samples every 30 s; this diagnostic loop is not a fast protection loop.
6. **Status expander:** on the isolated system side only, exercise each reviewed
   conditioned input and compare bits 0..6 to the Rev.EZ pin contract. P7 must
   read low. Configuration=0xFF and polarity=0x00 must read back; register/bus
   failure must invalidate the byte. Do not connect PoE primary classification
   directly to MCU ground. `type2_verified` must remain false in this build,
   including when the raw class-detection input is active.
7. **Power monitor:** measure shunt/lead resistance and offset, then compare
   voltage/current/power against instruments over the approved source/load
   range. Current from the nominal 8 mOhm value is calculated, not calibrated.
   Approve numerical errors and uncertainties before any governor integration.
8. **Protection integration, later image:** measure sampling latency, source
   classification, fault response, amplifier disable time and transient energy.
   The host governor tests do not close this test. The PoE continuous application
   limit is 22.5 W; budget/thermal limits must be calibrated and enforced by an
   integrated image before audio is enabled.

Audio output, DSP/limiting, XVF3800 voice/privacy, radar, OTA/rollback and full
factory sequence remain separate implementation and hardware gates. This
diagnostic image intentionally cannot certify them.
