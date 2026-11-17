"""Hand copper the autorouter cannot close (CAD frame, mm).

ROUTES: (net, layer, width, points)   VIAS: (net, x, y, d, drill)
MOVE:   ref -> ((x, y), rot)           sides come from circuit.py
REMOVE: (kind, net, x, y) -> vias at the point / tracks with an end at the point
"""

# 5V trunk: buck output (B.Cu, east of the VBUS24 strip) -> over the strip on F.Cu between I2C0_SDA and the
# primary keep-out -> strip notch -> B.Cu north to the 5V via next to D2
ROUTES = [
    ("5V", "B.Cu", 0.5, [(280.44, 31.28), (279.82, 30.66), (255.0, 30.66)]),
    ("5V", "F.Cu", 0.5, [(255.0, 30.66), (255.0, 28.6), (253.7, 27.3), (185.6, 27.3)]),
    ("5V", "B.Cu", 0.5, [(185.6, 27.3), (185.6, 51.5), (169.96, 51.5), (169.96, 63.25)]),
    # W5500 EXRES1: pin 10 -> via in the left fan-out -> R40 on B.Cu under the pin row -> GND via of pin 9
    ("W_EXRES", "F.Cu", 0.2, [(179.835, 64.25), (178.5, 64.4)]),
    ("W_EXRES", "B.Cu", 0.2, [(178.5, 64.4), (179.24, 64.42)]),
    ("GND", "B.Cu", 0.25, [(180.26, 64.42), (181.07, 64.75)]),
    # R32 (CC1 pull-down) GND, its old via spot is taken by EXRES
    ("GND", "F.Cu", 0.25, [(178.10, 63.66), (177.3, 64.45)]),
    # ETH_RXN layer change moved 60 um up to clear the EXRES via
    ("ETH_RXN", "F.Cu", 0.25, [(177.85, 65.69), (177.85, 65.45), (178.12, 65.18), (178.40, 65.18)]),
    ("ETH_RXN", "B.Cu", 0.25, [(178.40, 65.18), (179.26, 65.18), (179.97, 65.89)]),
]

VIAS = [
    ("5V", 255.0, 30.66, 0.8, 0.4),
    ("5V", 185.6, 27.3, 0.8, 0.4),
    ("W_EXRES", 178.5, 64.4, 0.5, 0.25),
    ("GND", 177.3, 64.45, 0.5, 0.25),
    ("ETH_RXN", 178.40, 65.18, 0.5, 0.25),
]

MOVE = {
    "TP2": ((230.0, 27.3), 0.0),
    "R40": ((179.75, 64.42), 0.0),
}

REMOVE = [
    ("via", "GND", 178.51, 64.36), ("trk", "GND", 178.51, 64.36),
    ("via", "ETH_RXN", 178.47, 65.12), ("trk", "ETH_RXN", 178.47, 65.12), ("trk", "ETH_RXN", 178.42, 65.12),
    ("trk", "ETH_RXN", 178.91, 64.83),
    ("trk", "GND", 180.76, 72.05), ("via", "GND", 181.53, 72.05), ("trk", "GND", 181.53, 72.05),
]
