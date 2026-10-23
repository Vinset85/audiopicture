# P1 — MAIN J5 to reSpeaker Flex (XVF3800) header

J5 is a 2×10, 2.54 mm IDC header on the MAIN bottom side (`Amphenol T821120A1S100CEU`, at X 44.5, Y 68.5, outside the ESP32 antenna keep-out). An 80 mm IDC ribbon (BOM item W1) runs to the Flex core, which sits behind the MAIN on its own standoffs (origin X 30, Y 14, z 12).

Status: **VERIFY against the Seeed Flex XVF3800 header drawing before ordering W1.** The pin numbers on the Flex side follow the Seeed XIAO-replacement header as read for Rev.D; the pitch of the Flex header decides the IDC socket.

| J5 pin | Net | Direction (from MAIN) | Notes |
| ---: | --- | --- | --- |
| 2 | `XVF_LRCK` | in | I2S word clock from the XVF3800 (XVF is I2S master), ESP32 GPIO5 |
| 3 | `XVF_DATA0` | out | ESP32 → XVF reference/playback data, GPIO7 through R66 1 kΩ |
| 4, 8, 12, 17 | `GND` | — | |
| 5 | `XVF_SDA` | bidir | I2C1 control, GPIO41 through R68 100 Ω, pull-up R70 4.7 kΩ to `FLEX_VDDIO` |
| 6 | `XVF_SCL` | out | I2C1 clock, GPIO42 through R69 100 Ω, pull-up R71 4.7 kΩ to `FLEX_VDDIO` |
| 7 | `XVF_X1D13` | out | XVF GPIO (boot/attention), GPIO47 through R67 1 kΩ |
| 9, 10 | `FLEX_5V` | power out | 5 V switched by U7 TPS22917; off while muted |
| 11 | `FLEX_VDDIO` | power in | Flex 3.3 V I/O rail, used only as the I2C pull-up reference |
| 19 | `XVF_DATA1` | in | XVF → ESP32 processed microphone stream, GPIO6 |
| 20 | `XVF_BCLK` | in | I2S bit clock from the XVF3800, GPIO4 |
| 1, 13–16, 18 | — | — | not connected on the MAIN |

Privacy mute is hardware: SW1 toggles U13 (74AUP1G74); `MUTED` turns off U7, so the XVF3800 and the microphones lose power, and lights D3. Because the I2C pull-ups go to `FLEX_VDDIO`, the MAIN never back-powers the Flex. Firmware must also set GPIO4–7, 41, 42 and 47 to high impedance while `MUTE_STATE` (GPIO39) is high; the series resistors limit the current if it does not.
