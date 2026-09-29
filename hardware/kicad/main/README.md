# MAIN PCB — KiCad capture plan Rev.A

Target tool: **KiCad 9.x**.

KiCad native files (.kicad_pro/.kicad_sch/.kicad_pcb) will be committed only when generated/validated by KiCad. This repository does not accept hand-authored pseudo-KiCad files.

## Hierarchy
Root: `audiopicture-main.kicad_sch`

Sub-sheets:
1. `01-ethernet-poe.kicad_sch`
2. `02-power-input-oring.kicad_sch`
3. `03-power-rails-monitor.kicad_sch`
4. `04-esp32-control.kicad_sch`
5. `05-audio-tas5825m.kicad_sch`
6. `06-usb-service.kicad_sch`
7. `07-daughterboards.kicad_sch`
8. `08-test-production.kicad_sch`

## Global power nets
+24V_POE
+24V_EXT
+24V_RAW
+24V_SYS
+5V_SYS
+5V_SERVICE
+3V3_SYS
GND

Functional ground names in documentation do not imply split copper. MAIN L2 is a continuous GND plane unless a verified reference-design isolation boundary requires otherwise.

## Global signal nets
I2C_SDA
I2C_SCL
AUD_BCLK
AUD_LRCLK
AUD_TX
AUD_RX
AMP_PDN
AMP_FAULT
ETH_RST
ETH_INT
POE_PRESENT
EXT_PRESENT
POWER_ALERT
5V_PG
3V3_PG
SPI_SCLK
SPI_MOSI
SPI_MISO
RADAR_CS
RADAR_IRQ
RADAR_RST
RADAR_EN
VOICE_RST
VOICE_IRQ
MIC_HW_EN
STATUS_LED
SERVICE_TOUCH
UART_TX
UART_RX

## Sheet contracts

### 01 Ethernet / PoE
External: RJ45 Ethernet/PoE
Outputs: ETH_MDI pairs -> W5500; +24V_POE; POE_PRESENT
Inputs/control: ETH_RST, SPI bus, ETH_CS
Outputs/control: ETH_INT

### 02 Power input / ORing
External: J2 24 V DC
Inputs: +24V_POE
Outputs: +24V_EXT, +24V_RAW, EXT_PRESENT
Functions: fuse, TVS, reverse protection, dual ideal diode, source priority

### 03 Rails / monitor
Input: +24V_RAW
Outputs: +24V_SYS, +5V_SYS, +3V3_SYS
Control/status: I2C, POWER_ALERT, 5V_PG, 3V3_PG
Functions: Kelvin shunt, INA228, TPSM63603, TPS62823

### 04 ESP32 control
U1 ESP32-S3-WROOM-1-N16R8
Interfaces: SPI Ethernet, radar SPI, I2C, I2S, USB, UART, control/status
Reserved: GPIO26..37
Strapping pins treated explicitly.

### 05 Audio
Input: +24V_SYS, +3V3/control as required, I2S, I2C, AMP_PDN
Output: AMP_FAULT, J3/J4 DML
Functions: TAS5825M, bootstrap, PVDD decoupling, LC filters

### 06 USB service
USB-C service/recovery
Outputs: USB D+/D-, +5V_SERVICE
No amplifier power path.
No uncontrolled backfeed.

### 07 Daughterboards
J101 VOICE 16-pin physical / 14 logical signals
J201 RADAR 12-pin
J301 ENV 8-pin
Expansion header: I2C + UART + 3V3 + 5V + GND + GPIO/INT

### 08 Production test
Pogo pads for rails, UART, boot/reset, I2C, audio clocks and interrupts.

## ERC policy
- no unresolved power-input warnings hidden with blanket PWR_FLAG usage;
- explicit no-connect marks on intentionally unused pins;
- every open-drain line has one deliberate pull-up owner;
- reset/enable lines have boot-safe hardware states;
- no GPIO may be driven when its receiving rail is off unless the interface is power-off protected;
- PoE isolation boundary is explicit;
- USB shield/chassis strategy is explicit;
- no duplicate conflicting global labels.

## PCB net classes (initial)
POWER_24V_HIGH: source/amp high-current paths
POWER_5V: 5 V rail
POWER_3V3: 3.3 V rail
CLASS_D: TAS5825M switching outputs before LC
ETH_MDI: 100BASE-TX differential
USB_FS: USB D+/D-
I2S: BCLK/LRCLK/data
SPI_FAST: W5500/radar host-side SPI
SENSITIVE: INA228 Kelvin and low-level control

Widths/clearances are NOT frozen here; they will be calculated from copper weight, current, temperature rise and manufacturer rules.

## Capture order
1. Power-input/ORing.
2. Rails/INA228.
3. ESP32 minimum system.
4. W5500/Ethernet/PoE.
5. TAS5825M.
6. USB-C.
7. daughterboard connectors.
8. test points.
9. ERC.
10. footprint audit.
11. PCB floorplan.


## Rev.A sheet specification status
- 01 Ethernet/PoE: specified
- 02 Power input/ORing: specified
- 03 Rails/monitor: specified
- 04 ESP32/control: specified
- 05 TAS5825M/audio: specified
- 06 USB service: specified
- 07 Daughterboards: specified
- 08 Factory test: specified

The electrical architecture specification phase for MAIN Rev.A is complete. Next phase: native KiCad schematic capture, symbol/footprint audit, ERC, then PCB floorplanning.


## PCB floorplan constraint — Ethernet/PoE
MAIN Rev.A reserves three physical domains at the cable edge: ETH_CABLE_PRIMARY, CHASSIS and SELV_SYSTEM.

Initial isolation keep-out between PoE primary and system secondary: 6.0 mm nominal no-copper/no-via corridor, subject to final IEC 62368-1/material/pollution-degree verification.

Placement chain:
RJ45 -> T_ETH / PoE extraction -> BR201/BR202 -> Ag53024 -> C_POE_OUT -> PoE LM74700 -> +24V_RAW.

W5500 remains on the SELV/system side of T_ETH and close to the transformer PHY-side pins.

Routing shall not begin until exact RJ45, Ag53024 land pattern and Schottky bridge MPNs are frozen.
