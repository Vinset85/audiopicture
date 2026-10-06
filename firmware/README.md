# AudioPicture firmware — Rev.EZ diagnostic build

**Compiled for ESP32-S3; not flashed or tested on a physical board.** The
application keeps amplifier, microphones, voice processor and radar disabled.
It is a bring-up diagnostic image, not finished product firmware.

Implemented:

- Preloaded safe GPIO output levels before output-driver enable. External
  reset/boot bias is still mandatory before the application starts.
- Persistent UUID in NVS; NVS errors never automatically erase identity.
- W5500 Ethernet, DHCP and local mDNS discovery. Optional Wi-Fi station reads
  previously provisioned `network/ssid` and `network/password` NVS values.
  No AP, default credentials or provisioning UI is provided.
- Read-only `/api/v1/info` and `/api/v1/status`; unavailable/stale measurements
  are JSON null. No actuator or credential-writing endpoint is exposed.
- SHT45 CRC-checked readings at 0x44; OPT3004 at 0x45; raw INA228 readings at
  0x40 with current/power calculated from the nominal 8 mOhm shunt. SHT45
  thermal and fabric/lux corrections are not fabricated.
- TCA9534 at 0x20: input-only configuration/readback and nullable raw diagnostic
  status byte. `type2_verified` stays false. See the Rev.EZ hardware input map.
- Tested portable power-governor state machine. It is **not connected to live
  amplifier control**, because hardware qualification and calibrated limits
  are missing. Thirty-second sensor polling is not the governor's fast loop.

## Build and host checks

Actual toolchain: **ESP-IDF v5.5.3**, commit
`2c211b236707889e8400c4dc5644dd5c4ee071e0`, official ESP32-S3 toolchain;
managed mDNS dependency 1.8.2 locked by `dependencies.lock`.
After installing that IDF revision with its tools and activating `export.sh`:

```sh
idf.py -B build set-target esp32s3
idf.py -B build build
```

Use a fresh build directory so `sdkconfig.defaults` takes effect: WROOM-1-N16R8,
16 MB flash, octal PSRAM, two 4 MB OTA slots and a separate factory-data NVS
partition. The layout has been compiled; PSRAM/flash behavior is unmeasured.
No OTA upload endpoint is implemented, despite rollback-capable partitions.

Portable C tests, with an AddressSanitizer/UndefinedBehaviorSanitizer-capable
Clang or GCC and CMake:

```sh
cmake -S tests -B build-host -DAP_ENABLE_SANITIZERS=ON
cmake --build build-host
ctest --test-dir build-host --output-on-failure
```

Assertions remain enabled even in Release builds. The three suites exercise
200000 governor events/320 combinations, official sensor vectors/CRC and bus
faults, and input-expander register/pattern/fault handling. Raw logs and hashes
are recorded in `../evidence/rev-ez`. Host transport mocks do not validate PCB
wiring, I2C rise time, SPI timing, network behavior or boot waveforms.

## Work remaining

Native MAIN/VOICE/RADAR schematics and all boards (ENV schematic has scoped ERC/netlist PASS), status-input conditioning,
isolated PoE classification/negotiation, hardware bring-up and measured safe
states; bounded fast power acquisition; TAS5825M initialization/DSP and audio
pipeline; XVF3800/radar integration; commissioning, OTA/security, acoustic
calibration and multiroom timing. Hardware release and complete functional
firmware must not be inferred from this successful diagnostic build.
