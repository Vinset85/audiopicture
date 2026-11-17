"""AudioPicture P1 MAIN board: single source of the circuit.

Every part: reference, symbol, value, footprint, MPN, pin->net map, placement group or fixed position.
Pins not listed are no-connect. Positions are global CAD coordinates (mm, X right, Y up, seen from the
front); MAIN outline 292 x 58 at origin (14, 16). KiCad F.Cu faces the room, so the KiCad top view is the
front view: kicad_x = X + 6, kicad_y = 94 - Y (layout.k / layout.g).
"""
from collections import OrderedDict

PARTS = OrderedDict()

R0402 = "Resistor_SMD:R_0402_1005Metric"
R0603 = "Resistor_SMD:R_0603_1608Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"
C0603 = "Capacitor_SMD:C_0603_1608Metric"
C0805 = "Capacitor_SMD:C_0805_2012Metric"
C1206 = "Capacitor_SMD:C_1206_3216Metric"
C1210 = "Capacitor_SMD:C_1210_3225Metric"

# ---------------------------------------------------------------- MPN tables
R_MPN = {"0402": "Yageo RC0402FR-07{v}L", "0603": "Yageo RC0603FR-07{v}L"}
C_MPN = {
    ("100n", "0402"): "Murata GRM155R71C104KA88D",       # 16 V X7R
    ("100n50", "0603"): "Murata GRM188R71H104KA93D",     # 50 V X7R
    ("100n50", "0402"): "Murata GRM155R71H104KE14D",     # 50 V X7R
    ("100n100", "0805"): "Murata GRM21BR72A104KAC4L",    # 100 V X7R
    ("1u", "0603"): "Murata GRM188R71E105KA12D",         # 25 V X7R
    ("1u50", "0805"): "Murata GRM21BR71H105KA12L",       # 50 V X7R
    ("4u7", "0603"): "Murata GRM188R61A475KE15D",        # 10 V X5R
    ("10u", "0805"): "Murata GRM21BR71A106KA73L",        # 10 V X7R
    ("22u", "0805"): "Murata GRM21BR61A226ME44L",        # 10 V X5R
    ("10u50", "1210"): "TDK C3225X7R1H106M250AC",        # 50 V X7R
    ("10u50", "1206"): "TDK C3216X5R1H106K160AB",        # 50 V X5R
    ("22u25", "1210"): "TDK C3225X7R1E226M250AB",        # 25 V X7R
    ("0u68", "0805"): "Murata GRM21BR71H684KA88L",       # 50 V X7R
    ("0u47", "0603"): "Murata GRM188R71E474KA12D",       # 25 V X7R
    ("0u22", "0603"): "Murata GRM188R71E224KA88D",       # 25 V X7R
    ("27p", "0402"): "Murata GRM1555C1H270JA01D",        # C0G
    ("120p", "0402"): "Murata GRM1555C1H121JA01D",       # C0G
    ("1n", "0402"): "Murata GRM155R71H102KA01D",
    ("10n", "0402"): "Murata GRM155R71H103KA88D",
    ("10n100", "0603"): "Murata GRM188R72A103KA01D",     # 100 V X7R
    ("1n2kV", "1808"): "Vishay VJ1808Y102KXGAT",         # 2 kV X7R
}


def part(ref, sym, value, fp, pins, mpn="", grp=None, at=None, side="F", rot=0.0, dnp=False, note="", h=None):
    assert ref not in PARTS, ref
    PARTS[ref] = dict(ref=ref, sym=sym, value=value, fp=fp, pins=dict(pins), mpn=mpn, grp=grp, at=at,
                      side=side, rot=rot, dnp=dnp, note=note, h=h)


def r_code(v):
    """Yageo value code: 49.9 -> 49R9, 6.65k -> 6K65, 10k -> 10K, 1M -> 1M."""
    m = v[-1] if v[-1] in "kM" else "R"
    num = v[:-1] if m != "R" else v
    a, _, b = num.partition(".")
    return a + m.upper() + b


def R(ref, v, a, b, grp, size="0402", **kw):
    mpn = "Yageo RC%sJR-070RL" % size if v == "0" else R_MPN[size].format(v=r_code(v))
    part(ref, "Device:R_Small", v, R0402 if size == "0402" else R0603, {"1": a, "2": b}, mpn, grp, **kw)


def C(ref, v, a, b, grp, key=None, size="0402", **kw):
    fp = {"0402": C0402, "0603": C0603, "0805": C0805, "1206": C1206, "1210": C1210,
          "1808": "Capacitor_SMD:C_1808_4520Metric"}[size]
    key = key or v
    part(ref, "Device:C_Small", v, fp, {"1": a, "2": b}, C_MPN.get((key, size), "VERIFY"), grp, **kw)


# ======================================================================== POWER ENTRY: DC 24 V
part("J1", "Connector:Barrel_Jack_MountingPin", "24V DC 5.5/2.1", "Connector_BarrelJack:BarrelJack_CUI_PJ-063AH_Horizontal",
     {"1": "DC_RAW", "2": "GND", "MP": "GND"}, "CUI PJ-063BH (VERIFY vs PJ-063AH land)", at=(158.0, 46.0), side="B", rot=0, h=11.0,
     note="mating face toward -Y, plug inserted from the bay floor")
part("F1", "Device:Fuse_Small", "4A", "Fuse:Fuse_Littelfuse-NANO2-451_453", {"1": "DC_RAW", "2": "DC_F"},
     "Littelfuse 0453004.MR", "PIN")
part("D1", "Device:D_Zener_Small", "SMBJ33A", "Diode_SMD:D_SMB", {"1": "DC_F", "2": "GND"}, "Littelfuse SMBJ33A", "PIN",
     note="unidirectional TVS, cathode (pad 1, band) on DC_F")
C("C1", "1u", "DC_F", "GND", "PIN", key="1u50", size="0805")
part("U1", "Power_Management:LM74700", "LM74700QDBVRQ1", "Package_TO_SOT_SMD:SOT-23-6",
     {"1": "VCAP1", "2": "GND", "3": "DC_F", "4": "VBUS_OR", "5": "GATE1", "6": "DC_F"}, "TI LM74700QDBVRQ1", "PIN")
C("C2", "0.22u", "VCAP1", "DC_F", "PIN", key="0u22", size="0603")
part("Q1", "Transistor_FET:BSC028N06LS3", "BSC028N06LS3", "Package_TO_SOT_SMD:TDSON-8-1",
     {"1": "DC_F", "2": "DC_F", "3": "DC_F", "4": "GATE1", "5": "VBUS_OR"}, "Infineon BSC028N06LS3GATMA1", "PIN")

# ======================================================================== POWER ENTRY: PoE (primary side)
part("J2", "Connector:RJ45", "RJ45", "Connector_RJ:RJ45_Amphenol_54602-x08_Horizontal",
     {str(i): f"ETH_L{i}" for i in range(1, 9)}, "Amphenol 54602-908LF (VERIFY)", at=(230.0, 40.0), side="B", rot=0, h=13.5,
     note="unshielded, non-magnetic; magnetics T1")
part("T1", "AudioPicture_P1:PT61020EL", "PT61020EL", "AudioPicture_P1:Bourns_PT61020EL_SMD24",
     {"23": "ETH_L1", "22": "ETH_L2", "24": "POE_CT12",
      "20": "ETH_L3", "19": "ETH_L6", "21": "POE_CT36",
      "17": "ETH_L4", "16": "ETH_L5", "18": "POE_CT45",
      "14": "ETH_L7", "13": "ETH_L8", "15": "POE_CT78",
      "2": "ETH_TXP", "3": "ETH_TXN", "1": "ETH_TCT",
      "5": "ETH_RXP", "6": "ETH_RXN", "4": "ETH_RCT"},
     "Bourns PT61020EL", at=(206.0, 63.0), rot=90.0, h=6.0)
for i, ct in enumerate(("POE_CT12", "POE_CT36", "POE_CT45", "POE_CT78")):
    C(f"C{10 + i}", "10n", ct, f"BS{i + 1}", "PRI", key="10n100", size="0603")
    R(f"R{10 + i}", "75", f"BS{i + 1}", "BS_NODE", "PRI", size="0603")
C("C14", "1n", "BS_NODE", "GND", "PRI", key="1n2kV", size="1808", note="Bob Smith to secondary GND, 2 kV")
for i, (ca, cb) in enumerate((("POE_CT12", "POE_CT36"), ("POE_CT45", "POE_CT78"))):
    for j, ct in enumerate((ca, cb)):
        n = 11 + 4 * i + 2 * j
        part(f"D{n}", "Device:D_Schottky_Small", "STPS2H100A", "Diode_SMD:D_SMA", {"1": "POE_VP", "2": ct},
             "ST STPS2H100A", "PRI")
        part(f"D{n + 1}", "Device:D_Schottky_Small", "STPS2H100A", "Diode_SMD:D_SMA", {"1": ct, "2": "POE_VN"},
             "ST STPS2H100A", "PRI")
part("D19", "Device:D_Zener_Small", "SMAJ58A", "Diode_SMD:D_SMA", {"1": "POE_VP", "2": "POE_VN"}, "Littelfuse SMAJ58A", "PRI",
     note="unidirectional TVS, cathode on POE_VP")
C("C15", "100n", "POE_VP", "POE_VN", "PRI", key="100n100", size="0805")
part("U2", "AudioPicture_P1:Ag53024", "Ag53024", "AudioPicture_P1:Silvertel_Ag53000_SIL10",
     {"1": "POE_VP", "2": "POE_VN", "7": "GND", "8": "POE_24V", "9": "POE_ADJ", "10": "GND"},
     "Silvertel Ag53024", at=(203.0, 33.0), rot=180.0, h=18.0,
     note="pin 1 at (203,33); module body toward -Y; primary pins 1-6 right, secondary 7-10 left")
R("R14", "136k", "POE_ADJ", "POE_24V", "PIN", note="lowers VOUT to ~22.8 V so the DC input wins the OR (VERIFY Ag53000 ADJ table)")
part("C16", "Device:C_Polarized_Small", "220u 25V", "Capacitor_SMD:CP_Elec_8x10.5", {"1": "POE_24V", "2": "GND"},
     "Panasonic EEE-FK1E221P", "PIN", h=10.5)
C("C17", "10u", "POE_24V", "GND", "PIN", key="10u50", size="1210")
C("C18", "100n", "POE_24V", "GND", "PIN", key="100n50", size="0603")
part("U3", "Power_Management:LM74700", "LM74700QDBVRQ1", "Package_TO_SOT_SMD:SOT-23-6",
     {"1": "VCAP2", "2": "GND", "3": "POE_24V", "4": "VBUS_OR", "5": "GATE2", "6": "POE_24V"}, "TI LM74700QDBVRQ1", "PIN")
C("C19", "0.22u", "VCAP2", "POE_24V", "PIN", key="0u22", size="0603")
part("Q2", "Transistor_FET:BSC028N06LS3", "BSC028N06LS3", "Package_TO_SOT_SMD:TDSON-8-1",
     {"1": "POE_24V", "2": "POE_24V", "3": "POE_24V", "4": "GATE2", "5": "VBUS_OR"}, "Infineon BSC028N06LS3GATMA1", "PIN")

# ======================================================================== measurement and bus
part("R20", "Device:R_Shunt", "8m", "Resistor_SMD:R_Shunt_Vishay_WSK2512_6332Metric_T1.19mm",
     {"1": "VBUS_OR", "2": "SH_P", "3": "SH_N", "4": "VBUS24"}, "Vishay WSK25128L000FEA", "PIN")
part("U4", "Sensor_Energy:INA228", "INA228AIDGSR", "Package_SO:TSSOP-10_3x3mm_P0.5mm",
     {"1": "GND", "2": "GND", "3": "INA_ALERT", "4": "I2C0_SDA", "5": "I2C0_SCL", "6": "3V3", "7": "GND",
      "8": "SH_N", "9": "SH_N", "10": "SH_P"}, "TI INA228AIDGSR", "PIN", note="I2C 0x40")
C("C20", "100n", "3V3", "GND", "PIN")
R("R21", "10k", "INA_ALERT", "3V3", "PIN")
part("C21", "Device:C_Polarized_Small", "470u 35V", "Capacitor_THT:CP_Radial_D10.0mm_P5.00mm",
     {"1": "VBUS24", "2": "GND"}, "Panasonic EEU-FR1V471B", at=(128.0, 22.0), rot=90.0, h=16.0,
     note="PVDD bulk; 10 x 16 mm (VERIFY height vs 16.5 envelope)")

# ======================================================================== 5 V buck
part("U5", "Converter_DCDC:TPSM53603RDA", "TPSM53603RDAR", "Package_DFN_QFN:Texas_B3QFN-14-1EP_5x5.5mm_P0.65mm_ThermalVia",
     {"1": "VBUS24", "14": "VBUS24", "2": "EN_5V", "3": "GND", "10": "GND", "11": "GND", "15": "GND", "12": "GND",
      "6": "PG_5V", "7": "5V", "8": "5V", "9": "FB_5V"}, "TI TPSM53603RDAR", "BUCK")
R("R22", "100k", "VBUS24", "EN_5V", "BUCK", note="UVLO 1.23*(1+100/6.65)=19.7 V")
R("R23", "6.65k", "EN_5V", "GND", "BUCK")
R("R24", "10k", "5V", "FB_5V", "BUCK", note="RFBT")
R("R25", "2.49k", "FB_5V", "GND", "BUCK", note="RFBB -> 5.02 V")
R("R26", "10k", "PG_5V", "3V3", "BUCK")
C("C22", "10u", "VBUS24", "GND", "BUCK", key="10u50", size="1206")
C("C23", "10u", "VBUS24", "GND", "BUCK", key="10u50", size="1206")
C("C24", "100n", "VBUS24", "GND", "BUCK", key="100n50", size="0603")
for i in range(3):
    C(f"C{25 + i}", "22u", "5V", "GND", "BUCK", key="22u25", size="1210")
part("D2", "Device:D_Schottky_Small", "MBR130T1G", "Diode_SMD:D_SOD-123", {"1": "5V", "2": "VBUS_USB"},
     "onsemi MBR130T1G", "PIN", note="USB-only service mode")

# ======================================================================== 3V3 buck
part("U6", "Regulator_Switching:TPS62823DLC", "TPS62823DLCR", "Package_SON:Texas_VSON-HR-8_1.5x2mm_P0.5mm",
     {"1": "5V", "2": "FB_3V3", "3": "GND", "5": "GND", "6": "SW_3V3", "7": "5V"}, "TI TPS62823DLCR", "PWR")
part("L1", "Device:L_Small", "470n", "Inductor_SMD:L_Wuerth_PMFI-201610_PMCI-compatible", {"1": "SW_3V3", "2": "3V3"},
     "TDK TFM201610ALM-R47MTAA", "PWR", note="2016 land (VERIFY)")
R("R27", "453k", "3V3", "FB_3V3", "PWR", note="0.6*(1+453/100)=3.32 V")
R("R28", "100k", "FB_3V3", "GND", "PWR")
C("C28", "120p", "3V3", "FB_3V3", "PWR")
C("C29", "10u", "5V", "GND", "PWR", size="0805")
C("C30", "22u", "3V3", "GND", "PWR", size="0805")
C("C31", "22u", "3V3", "GND", "PWR", size="0805")

# ======================================================================== ESP32-S3
part("U8", "RF_Module:ESP32-S3-WROOM-1", "ESP32-S3-WROOM-1-N16R8", "RF_Module:ESP32-S3-WROOM-1",
     {"1": "GND", "40": "GND", "41": "GND", "2": "3V3", "3": "ESP_EN",
      "4": "XVF_BCLK", "5": "XVF_LRCK", "6": "XVF_DATA1", "7": "ESP_XVF_DOUT",
      "8": "ESP_TAS_BCLK", "9": "ESP_TAS_LRCK", "10": "ESP_TAS_SDIN", "11": "TAS_PDN", "12": "TAS_FAULT",
      "13": "USB_DN", "14": "USB_DP", "15": "PG_5V", "17": "RADAR_IO", "18": "ETH_CS", "19": "ETH_MOSI",
      "20": "ETH_SCLK", "21": "ETH_MISO", "22": "ETH_INT", "23": "ETH_RST", "24": "ESP_X1D13", "25": "LED_DATA",
      "27": "ESP_BOOT", "31": "INA_ALERT", "32": "MUTE_STATE", "33": "BTN_ACTION", "34": "ESP_SDA1", "35": "ESP_SCL1",
      "36": "RADAR_TX", "37": "RADAR_RX", "38": "I2C0_SCL", "39": "I2C0_SDA"},
     "Espressif ESP32-S3-WROOM-1-N16R8", at=(86.0, 74.0), rot=0.0, h=3.2,
     note="antenna toward +Y, module end flush with the top edge; all-layer keep-out under the antenna")
R("R30", "10k", "ESP_EN", "3V3", "ESP")
C("C32", "1u", "ESP_EN", "GND", "ESP", size="0603")
R("R31", "10k", "ESP_BOOT", "3V3", "ESP")
part("SW3", "Switch:SW_Push", "BOOT", "Button_Switch_SMD:SW_SPST_PTS810", {"1": "ESP_BOOT", "2": "GND"}, "C&K PTS810SJM250SMTRLFS", "ESP")
part("SW4", "Switch:SW_Push", "RESET", "Button_Switch_SMD:SW_SPST_PTS810", {"1": "ESP_EN", "2": "GND"}, "C&K PTS810SJM250SMTRLFS", "ESP")
C("C33", "22u", "3V3", "GND", "ESP", size="0805")
C("C34", "100n", "3V3", "GND", "ESP")

# ======================================================================== USB-C (service / firmware)
part("J3", "Connector:USB_C_Receptacle_USB2.0_16P", "USB-C", "Connector_USB:USB_C_Receptacle_GCT_USB4085",
     {"A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND", "A4": "VBUS_USB", "A9": "VBUS_USB", "B4": "VBUS_USB",
      "B9": "VBUS_USB", "A5": "USB_CC1", "B5": "USB_CC2", "A6": "USB_DP", "B6": "USB_DP", "A7": "USB_DN", "B7": "USB_DN",
      "SH": "GND"}, "GCT USB4085-GF-A", at=(176.0, 52.0), side="B", rot=0, h=3.3)
R("R32", "5.1k", "USB_CC1", "GND", "PIN")
R("R33", "5.1k", "USB_CC2", "GND", "PIN")
part("U9", "Power_Protection:TPD2EUSB30", "TPD2EUSB30", "Package_TO_SOT_SMD:Texas_DRT-3",
     {"1": "USB_DP", "2": "USB_DN", "3": "GND"}, "TI TPD2EUSB30DRTR", "PIN")
C("C35", "1u", "VBUS_USB", "GND", "PIN", size="0603")

# ======================================================================== Ethernet W5500
part("U10", "Interface_Ethernet:W5500", "W5500", "Package_QFP:LQFP-48_7x7mm_P0.5mm",
     {"1": "ETH_TXN", "2": "ETH_TXP", "5": "ETH_RXN", "6": "ETH_RXP",
      **{p: "GND" for p in ("3", "9", "14", "16", "19", "48", "29", "23", "38", "39", "40", "41", "42")},
      **{p: "3V3A" for p in ("4", "8", "11", "15", "17", "21")},
      "10": "W_EXRES", "20": "W_TOCAP", "22": "W_1V2O", "28": "3V3", "30": "W_XI", "31": "W_XO",
      "32": "ETH_CS", "33": "ETH_SCLK", "34": "ETH_MISO", "35": "ETH_MOSI", "36": "ETH_INT", "37": "ETH_RST"},
     "WIZnet W5500", at=(184.0, 66.0), rot=0.0)
R("R40", "12.4k", "W_EXRES", "GND", "ETH", side="B")
C("C40", "4.7u", "W_TOCAP", "GND", "ETH", key="4u7", size="0603")
C("C41", "10n", "W_1V2O", "GND", "ETH")
part("FB1", "Device:FerriteBead_Small", "120R", "Inductor_SMD:L_0603_1608Metric", {"1": "3V3", "2": "3V3A"},
     "Murata BLM18PG121SN1D", "ETH")
C("C42", "10u", "3V3A", "GND", "ETH", size="0805")
for i in range(6):
    C(f"C{43 + i}", "100n", "3V3A", "GND", "ETH")
C("C49", "100n", "3V3", "GND", "ETH")
part("Y1", "Device:Crystal_GND24_Small", "25MHz", "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm",
     {"1": "W_XI", "2": "GND", "3": "W_XO", "4": "GND"}, "Abracon ABM8G-25.000MHZ-18-D2Y-T", "ETH")
C("C50", "27p", "W_XI", "GND", "ETH")
C("C51", "27p", "W_XO", "GND", "ETH")
R("R41", "1M", "W_XI", "W_XO", "ETH")
R("R42", "49.9", "ETH_TXP", "ETH_TCT", "ETH")
R("R43", "49.9", "ETH_TXN", "ETH_TCT", "ETH")
R("R44", "10", "ETH_TCT", "3V3A", "ETH")
C("C52", "100n", "ETH_TCT", "GND", "ETH")
R("R45", "49.9", "ETH_RXP", "ETH_RCT", "ETH")
R("R46", "49.9", "ETH_RXN", "ETH_RCT", "ETH")
C("C53", "100n", "ETH_RCT", "GND", "ETH")
R("R47", "10k", "ETH_INT", "3V3", "ETH")
R("R48", "10k", "ETH_RST", "3V3", "ETH")

# ======================================================================== TAS5825M amplifier
part("U11", "Amplifier_Audio:TAS5825MRHB", "TAS5825MRHBR", "Package_DFN_QFN:Texas_RHB0032E_VQFN-32-1EP_5x5mm_P0.5mm_EP3.45x3.45mm_ThermalVias",
     {"1": "BSTAP", "2": "OUTAP", "3": "VBUS24", "4": "VBUS24", "5": "GND", "6": "3V3", "7": "TAS_VRDIG",
      "8": "TAS_ADR", "11": "TAS_FAULT", "12": "TAS_LRCK", "13": "TAS_BCLK", "14": "TAS_SDIN", "15": "I2C0_SDA",
      "16": "I2C0_SCL", "17": "TAS_PDN", "18": "TAS_GVDD", "19": "TAS_AVDD", "20": "GND", "21": "VBUS24",
      "22": "VBUS24", "23": "OUTBP", "24": "BSTBP", "25": "GND", "26": "GND", "27": "OUTBN", "28": "BSTBN",
      "29": "BSTAN", "30": "OUTAN", "31": "GND", "32": "GND", "33": "GND"},
     "TI TAS5825MRHBR", at=(112.0, 33.0), rot=270.0, note="I2C 0x4C (ADR 0 ohm to GND)")
R("R50", "0", "TAS_ADR", "GND", "AMP")
C("C54", "4.7u", "3V3", "GND", "AMP", key="4u7", size="0603")
C("C55", "100n", "3V3", "GND", "AMP")
C("C56", "1u", "TAS_VRDIG", "GND", "AMP", size="0603")
C("C57", "1u", "TAS_GVDD", "GND", "AMP", size="0603")
C("C58", "1u", "TAS_AVDD", "GND", "AMP", size="0603")
for i in range(2):
    C(f"C{59 + i}", "10u", "VBUS24", "GND", "AMP", key="10u50", size="1210")
    C(f"C{61 + i}", "100n", "VBUS24", "GND", "AMP", key="100n50", size="0402")
for n, (b, o) in enumerate((("BSTAP", "OUTAP"), ("BSTAN", "OUTAN"), ("BSTBP", "OUTBP"), ("BSTBN", "OUTBN"))):
    C(f"C{63 + n}", "0.47u", b, o, "AMP", key="0u47", size="0603")
R("R51", "100k", "TAS_PDN", "GND", "AMP")
R("R52", "10k", "TAS_FAULT", "3V3", "AMP")
R("R53", "33", "ESP_TAS_BCLK", "TAS_BCLK", "AMP")
R("R54", "33", "ESP_TAS_LRCK", "TAS_LRCK", "AMP")
R("R55", "33", "ESP_TAS_SDIN", "TAS_SDIN", "AMP")
for n, (o, s) in enumerate((("OUTAP", "SPK_WFP"), ("OUTAN", "SPK_WFN"), ("OUTBP", "SPK_TWA"), ("OUTBN", "SPK_TWN"))):
    part(f"L{2 + n}", "Device:L_Small", "10u", "Inductor_SMD:L_Coilcraft_XAL7050-XXX", {"1": o, "2": s},
         "Coilcraft XAL7050-103MEC", "AMP", h=5.1)
    C(f"C{67 + n}", "0.68u", s, "GND", "AMP", key="0u68", size="0805")
part("C71", "Device:C_Small", "47u NP", "Capacitor_THT:C_Radial_D10.0mm_H12.5mm_P5.00mm", {"1": "SPK_TWA", "2": "SPK_TWP"},
     "Nichicon UES1H470MPM", "AMP", h=12.5, note="tweeter DC/LF protection, fc ~847 Hz with 4 ohm")
part("J4", "Connector_Generic:Conn_01x04", "SPK", "Connector_JST:JST_VH_B4P-VH_1x04_P3.96mm_Vertical",
     {"1": "SPK_WFP", "2": "SPK_WFN", "3": "SPK_TWP", "4": "SPK_TWN"}, "JST B4P-VH(LF)(SN)", at=(121.0, 67.0), rot=0.0, h=9.6)

# ======================================================================== privacy mute and UI
part("SW1", "Switch:SW_Push", "MUTE", "Button_Switch_SMD:SW_SPST_EVQP7A", {"1": "GND", "2": "BTN_MUTE_RAW"},
     "Panasonic EVQ-P7A01P", at=(60.0, 18.2), rot=0.0, note="side actuated, plunger through the bottom wall")
R("R60", "100k", "BTN_MUTE_RAW", "3V3", "UI")
C("C72", "100n", "BTN_MUTE_RAW", "GND", "UI")
part("U12", "74xGxx:74LVC1G17", "74LVC1G17", "Package_TO_SOT_SMD:SOT-353_SC-70-5",
     {"2": "BTN_MUTE_RAW", "3": "GND", "4": "MUTE_CLK", "5": "3V3"}, "TI SN74LVC1G17DCKR", "UI")
part("U13", "74xGxx:74AUP1G74", "74AUP1G74", "Package_SO:VSSOP-8_2.3x2mm_P0.5mm",
     {"1": "MUTE_CLK", "2": "MIC_ON", "3": "MIC_ON", "4": "GND", "5": "MUTED", "6": "MUTE_POR", "7": "3V3", "8": "3V3"},
     "TI SN74AUP1G74DCUR", "UI", note="toggle: D = /Q")
C("C73", "100n", "3V3", "GND", "UI")
C("C74", "100n", "3V3", "GND", "UI")
R("R61", "100k", "3V3", "MUTE_POR", "UI")
C("C75", "1u", "MUTE_POR", "GND", "UI", size="0603")
R("R62", "1k", "MUTED", "MUTE_STATE", "UI")
part("Q3", "Transistor_FET:2N7002", "2N7002", "Package_TO_SOT_SMD:SOT-23", {"1": "MUTED", "2": "GND", "3": "LED_MUTE_K"},
     "onsemi 2N7002LT1G", "UI")
part("D3", "Device:LED_Small", "RED", "LED_SMD:LED_0603_1608Metric", {"1": "LED_MUTE_K", "2": "LED_MUTE_A"},
     "Kingbright APT1608EC", at=(80.0, 24.0), rot=0.0, note="under the mute light pipe")
R("R63", "470", "3V3", "LED_MUTE_A", "UI")
part("SW2", "Switch:SW_Push", "ACTION", "Button_Switch_SMD:SW_SPST_EVQP7A", {"1": "GND", "2": "BTN_ACTION"},
     "Panasonic EVQ-P7A01P", at=(100.0, 18.2), rot=0.0)
R("R64", "10k", "BTN_ACTION", "3V3", "UI")
C("C76", "100n", "BTN_ACTION", "GND", "UI")
part("D4", "LED:WS2812B-2020", "WS2812B-2020", "LED_SMD:LED_WS2812B-2020_PLCC4_2.0x2.0mm",
     {"2": "GND", "3": "LED_DIN", "4": "LED_5V"}, "Worldsemi WS2812B-2020", at=(90.0, 24.0), rot=0.0,
     note="under the status light pipe")
part("D5", "Device:D_Schottky_Small", "MBR130T1G", "Diode_SMD:D_SOD-123", {"1": "LED_5V", "2": "5V"},
     "onsemi MBR130T1G", "UI", note="drops VDD to ~4.6 V so 3.3 V DIN meets VIH")
C("C77", "100n", "LED_5V", "GND", "UI")
R("R65", "33", "LED_DATA", "LED_DIN", "UI")

# ======================================================================== Flex (XVF3800) header and mic power switch
part("U7", "Power_Management:TPS22917DBV", "TPS22917DBVR", "Package_TO_SOT_SMD:SOT-23-6",
     {"1": "5V", "2": "GND", "3": "MIC_ON", "4": "FLEX_CT", "5": "FLEX_QOD", "6": "FLEX_5V"}, "TI TPS22917DBVR", "UI",
     note="hardware privacy: MUTED removes power from the XVF3800 and microphones")
C("C78", "1u", "5V", "GND", "UI", size="0603")
R("R74", "100", "FLEX_QOD", "FLEX_5V", "UI", size="0603", note="quick output discharge")
C("C79", "1n", "FLEX_CT", "GND", "UI")
C("C80", "10u", "FLEX_5V", "GND", "UI", size="0805")
C("C81", "100n", "FLEX_5V", "GND", "UI")
part("J5", "Connector_Generic:Conn_02x10_Odd_Even", "FLEX", "Connector_IDC:IDC-Header_2x10_P2.54mm_Vertical",
     {"2": "XVF_LRCK", "3": "XVF_DATA0", "4": "GND", "5": "XVF_SDA", "6": "XVF_SCL", "7": "XVF_X1D13", "8": "GND",
      "9": "FLEX_5V", "10": "FLEX_5V", "11": "FLEX_VDDIO", "12": "GND", "17": "GND", "19": "XVF_DATA1", "20": "XVF_BCLK"},
     "Amphenol T821120A1S100CEU", at=(44.5, 68.5), side="B", rot=90.0, h=9.1,
     note="IDC ribbon 80 mm to the reSpeaker Flex header; pin map docs/p1/flex-header.md")
R("R66", "1k", "ESP_XVF_DOUT", "XVF_DATA0", "UI")
R("R67", "1k", "ESP_X1D13", "XVF_X1D13", "UI")
R("R68", "100", "ESP_SDA1", "XVF_SDA", "UI")
R("R69", "100", "ESP_SCL1", "XVF_SCL", "UI")
R("R70", "4.7k", "XVF_SDA", "FLEX_VDDIO", "UI", note="pull-ups to the Flex VDDIO: no back-powering when muted")
R("R71", "4.7k", "XVF_SCL", "FLEX_VDDIO", "UI")

# ======================================================================== radar
part("J6", "Connector_Generic_MountingPin:Conn_01x06_MountingPin", "RADAR", "Connector_JST:JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical",
     {"1": "3V3", "2": "GND", "3": "RADAR_RX", "4": "RADAR_TX", "5": "RADAR_IO", "6": "GND", "MP": "GND"},
     "JST BM06B-GHS-TBT", at=(44.0, 57.0), rot=0.0, h=4.3, note="HLK-LD6004 harness (VERIFY pinout)")
C("C82", "22u", "3V3", "GND", "UI", size="0805")
C("C83", "100n", "3V3", "GND", "UI")

# ======================================================================== environment island (thermally isolated)
part("U14", "Sensor_Humidity:SHT4x", "SHT45", "Sensor_Humidity:Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad",
     {"1": "I2C0_SDA", "2": "I2C0_SCL", "3": "3V3", "4": "GND"}, "Sensirion SHT45-AD1B-R2", at=(294.0, 24.0), rot=0.0,
     note="I2C 0x44, next to the bottom inlet vents")
C("C84", "100n", "3V3", "GND", "ENV")
part("U15", "AudioPicture_ENV:OPT3004DNPR", "OPT3004", "AudioPicture_ENV:TI_DNP0006A_OPT3004",
     {"1": "3V3", "2": "3V3", "3": "GND", "4": "I2C0_SCL", "6": "I2C0_SDA", "7": "GND"}, "TI OPT3004DNPR", at=(294.0, 46.0),
     rot=0.0, note="I2C 0x45 (ADDR=VDD), under the ambient light pipe")
C("C85", "100n", "3V3", "GND", "ENV")
R("R72", "2.2k", "I2C0_SDA", "3V3", "ENV")
R("R73", "2.2k", "I2C0_SCL", "3V3", "ENV")

# ======================================================================== test points, holes, fiducials
for n, net in enumerate(("VBUS24", "5V", "3V3", "GND", "GND", "FLEX_5V", "POE_24V", "DC_F", "I2C0_SDA", "I2C0_SCL",
                         "TAS_FAULT", "ESP_EN")):
    part(f"TP{n + 1}", "Connector:TestPoint", net, "TestPoint:TestPoint_Pad_D1.0mm", {"1": net}, "", "TP")
for n, (x, y) in enumerate(((18, 20), (302, 20), (18, 70), (302, 70), (142, 20), (142, 70))):
    part(f"H{n + 1}", "Mechanical:MountingHole", "M3", "MountingHole:MountingHole_3.2mm_M3", {}, "", at=(float(x), float(y)))
for n, (x, y) in enumerate(((16.5, 30.0), (303.5, 31.0), (150.0, 72.0))):
    part(f"FID{n + 1}", "Mechanical:Fiducial", "FID", "Fiducial:Fiducial_1mm_Mask2mm", {}, "", at=(x, y))

# ======================================================================== net classes
NETCLASS = {
    "PRI": ["ETH_L%d" % i for i in range(1, 9)] + ["POE_CT12", "POE_CT36", "POE_CT45", "POE_CT78", "POE_VP", "POE_VN",
                                                   "BS1", "BS2", "BS3", "BS4", "BS_NODE"],
    "PWR": ["DC_RAW", "DC_F", "POE_24V", "VBUS_OR", "5V", "FLEX_5V", "LED_5V", "VBUS_USB", "SW_3V3",
            "SH_P", "SH_N"],
    "AMP": ["OUTAP", "OUTAN", "OUTBP", "OUTBN", "SPK_WFP", "SPK_WFN", "SPK_TWA", "SPK_TWP", "SPK_TWN",
            "BSTAP", "BSTAN", "BSTBP", "BSTBN"],
    "ETH": ["ETH_TXP", "ETH_TXN", "ETH_RXP", "ETH_RXN", "ETH_TCT", "ETH_RCT"],
    "USB": ["USB_DP", "USB_DN"],
}
PLANES = {"GND": "In1.Cu", "3V3": "In2.Cu"}
STRIP_NET = "VBUS24"   # B.Cu pour strip along the lower corridor


def nets():
    out = {}
    for p in PARTS.values():
        for pin, n in p["pins"].items():
            out.setdefault(n, []).append((p["ref"], pin))
    return out


if __name__ == "__main__":
    ns = nets()
    print(len(PARTS), "parts,", len(ns), "nets")
    for n, c in sorted(ns.items()):
        if len(c) < 2:
            print("  single-pin net:", n, c)
