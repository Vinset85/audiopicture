"""Board-level layout data shared by the placer (venv Python) and the board builder (KiCad Python).

All coordinates are global CAD mm (X right, Y up, seen from the front = KiCad top view).
"""
import amp_hand
import hand_routes

X0, Y0, X1, Y1 = 14.0, 16.0, 306.0, 74.0


def k(x, y):
    """Global CAD -> KiCad page coordinates (mm)."""
    return x + 6.0, 94.0 - y


def g(kx, ky):
    return kx - 6.0, 94.0 - ky


# Edge.Cuts internal slots (thermal isolation of the ENV island), bridge Y 40..50 keeps the I2C/3V3/GND path
SLOTS = [(283.5, 18.0, 284.5, 40.0), (283.5, 50.0, 284.5, 72.0)]

# placement groups -> allowed rectangles
REGIONS = {
    "ENV": [(285.6, 17.0, 305.0, 73.0)],
    "UI": [(15.0, 17.0, 99.5, 73.0)],
    "AMP": [(100.0, 17.0, 150.0, 73.0)],
    "PIN": [(150.0, 37.5, 197.0, 57.5), (150.0, 57.5, 179.0, 73.0)],
    "ETH": [(179.0, 56.0, 199.0, 73.0)],
    "PRI": [(212.0, 37.5, 250.0, 73.0)],
    "BUCK": [(251.0, 17.0, 282.4, 73.0)],
    "PWR": [(251.0, 17.0, 282.4, 73.0)],
    "ESP": [(60.0, 17.0, 99.5, 73.0)],
}
REGIONS["TP"] = [r for gname in ("UI", "AMP", "PIN", "PWR") for r in REGIONS[gname]]

# primary (PoE line side) copper region; secondary copper must keep ISO mm away
PRIMARY = [(211.0, 30.0, 251.0, 74.0), (188.5, 30.0, 211.0, 37.0)]
ISO = 2.0

# extra keep-outs for parts (both sides): isolation barrier of the Ag53024 (from its footprint) is added by the builder
KEEPOUT_TOP = [
    (150.6, 22.6, 208.4, 36.1),   # Ag53024 module body (component side toward -Y)
]
ANTENNA = (75.0, 67.5, 97.0, 74.0)   # ESP32-S3-WROOM-1 antenna at the top edge, all layers

# fixed positions not given in circuit.py
FIXED_EXTRA = {
    "R20": ((145.0, 27.5), 0.0),
    "U4": ((146.0, 32.6), 0.0),
    "U5": ((262.0, 23.0), 0.0),
    "TP1": ((149.0, 19.0), 0.0),
    "C14": ((211.0, 41.0), 180.0),
}
FIXED_EXTRA.update({r: ((x, y), rot) for r, (x, y, rot) in amp_hand.PLACE.items()})
FIXED_EXTRA.update(hand_routes.MOVE)

# B.Cu VBUS24 strip (polygon, global)
# (finger up to Y 42.2 reaches the TAS5825M PVDD pins 3/4 on its upper side and their decoupling)
STRIP = [(100.0, 16.6), (279.0, 16.6), (279.0, 29.5), (189.6, 29.5), (189.6, 24.0), (168.1, 24.0), (168.1, 29.5),
         (118.4, 29.5), (118.4, 42.2), (105.6, 42.2), (105.6, 35.9), (115.4, 35.9), (115.4, 29.5), (100.0, 29.5)]

# nets that are not autorouted: they reach planes/strip through fan-out vias
PLANE_NETS = {"GND": "In1.Cu", "3V3": "In2.Cu", "VBUS24": "B.Cu"}

# anchor a part near a specific pin (decoupling and plane-net parts)
NEAR = {
    "C20": ("U4", "6"), "C33": ("U8", "2"), "C34": ("U8", "2"), "C32": ("U8", "3"), "R30": ("U8", "3"),
    "R31": ("U8", "27"), "SW3": ("U8", "27"), "SW4": ("U8", "3"),
    "C43": ("U10", "4"), "C44": ("U10", "8"), "C45": ("U10", "11"), "C46": ("U10", "15"), "C47": ("U10", "17"),
    "C48": ("U10", "21"), "C49": ("U10", "28"), "C40": ("U10", "20"), "C41": ("U10", "22"), "R40": ("U10", "10"),
    "C54": ("U11", "6"), "C55": ("U11", "6"), "C56": ("U11", "7"), "C57": ("U11", "18"), "C58": ("U11", "19"),
    "C59": ("U11", "3"), "C61": ("U11", "3"), "C60": ("U11", "22"), "C62": ("U11", "22"), "R50": ("U11", "8"),
    "C73": ("U12", "5"), "C74": ("U13", "8"), "C82": ("J6", "1"), "C83": ("J6", "1"),
    "C84": ("U14", "3"), "C85": ("U15", "1"), "R72": ("U15", "6"), "R73": ("U15", "4"),
    "C29": ("U6", "7"), "C30": ("L1", "2"), "C31": ("L1", "2"), "R27": ("U6", "2"), "R28": ("U6", "2"), "C28": ("U6", "2"),
    "C22": ("U5", "1"), "C23": ("U5", "14"), "C24": ("U5", "1"), "C25": ("U5", "7"), "C26": ("U5", "8"), "C27": ("U5", "7"),
    "R22": ("U5", "2"), "R26": ("U5", "6"),
    "C35": ("J3", "A4"), "C42": ("FB1", "2"), "C77": ("D4", "4"), "C78": ("U7", "1"), "C80": ("U7", "6"),
    "C81": ("U7", "6"), "R21": ("U4", "3"), "R60": ("SW1", "2"), "C72": ("SW1", "2"), "R64": ("SW2", "2"),
    "C76": ("SW2", "2"), "R61": ("U13", "6"), "C75": ("U13", "6"), "R63": ("D3", "2"), "Q3": ("D3", "1"),
    "D5": ("D4", "4"), "R65": ("D4", "3"), "C1": ("U1", "6"), "C17": ("U2", "8"), "C18": ("U2", "8"), "C16": ("U2", "8"),
    "R14": ("U2", "9"), "C15": ("U2", "1"), "D19": ("U2", "1"), "R47": ("U10", "36"), "R48": ("U10", "37"),
    "R32": ("J3", "A5"), "R33": ("J3", "B5"), "U9": ("J3", "A6"), "R51": ("U11", "17"), "R52": ("U11", "11"),
}
CENTROID_SKIP = {"GND", "3V3", "VBUS24", "5V"}
