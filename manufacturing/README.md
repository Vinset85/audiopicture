# Manufacturing

Factory test/provisioning target:
1. power rails;
2. ESP32 boot and identity;
3. Ethernet;
4. Wi-Fi/BLE;
5. environmental sensors;
6. radar;
7. four microphones;
8. amplifier;
9. DML acoustic sweep;
10. write factory calibration;
11. write/verify UUID and hardware revision;
12. firmware/OTA/recovery verification.

MAIN must expose pogo test points for power, UART, boot/reset, I2C, audio clocks and critical interrupts.
