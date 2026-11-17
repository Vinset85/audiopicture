"""Write p1-main.kicad_pro: net classes (exact-name patterns from circuit.NETCLASS) and board rules."""
import json
import os

import circuit

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "p1-main.kicad_pro")

# name: (clearance, track, via_d, via_drill)
CLASSES = {
    "Default": (0.15, 0.20, 0.60, 0.30),
    "PRI": (0.30, 0.30, 0.80, 0.40),
    "PWR": (0.15, 0.30, 0.80, 0.40),
    "AMP": (0.15, 0.40, 0.80, 0.40),
    "ETH": (0.15, 0.25, 0.60, 0.30),
    "USB": (0.15, 0.25, 0.60, 0.30),
}


def netclass(name, c):
    cl, tr, vd, vh = c
    return {"name": name, "clearance": cl, "track_width": tr, "via_diameter": vd, "via_drill": vh,
            "microvia_diameter": 0.3, "microvia_drill": 0.1, "diff_pair_width": 0.2, "diff_pair_gap": 0.25,
            "diff_pair_via_gap": 0.25, "wire_width": 6, "bus_width": 12, "line_style": 0, "pcb_color": "rgba(0, 0, 0, 0.000)",
            "schematic_color": "rgba(0, 0, 0, 0.000)", "priority": 0 if name != "Default" else 2147483647}


def write():
    pro = {
        "meta": {"filename": "p1-main.kicad_pro", "version": 3},
        "board": {"design_settings": {
            "defaults": {"board_outline_line_width": 0.1, "copper_line_width": 0.2, "copper_text_size_h": 1.5,
                         "copper_text_size_v": 1.5, "copper_text_thickness": 0.3, "silk_line_width": 0.12,
                         "silk_text_size_h": 0.8, "silk_text_size_v": 0.8, "silk_text_thickness": 0.12},
            "rules": {"min_clearance": 0.15, "min_track_width": 0.15, "min_via_diameter": 0.5, "min_through_hole_diameter": 0.2,
                      "min_hole_to_hole": 0.25, "min_copper_edge_clearance": 0.3, "min_hole_clearance": 0.25,
                      "min_silk_clearance": 0.0, "min_annular_width": 0.1, "min_microvia_diameter": 0.2,
                      "min_microvia_drill": 0.1, "solder_mask_to_copper_clearance": 0.0},
        }},
        "net_settings": {
            "classes": [netclass(k, v) for k, v in CLASSES.items()],
            "meta": {"version": 4},
            "netclass_patterns": [{"netclass": k, "pattern": n} for k, ns in circuit.NETCLASS.items() for n in ns],
        },
        "schematic": {"meta": {"version": 1}},
        "sheets": [],
        "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
    }
    json.dump(pro, open(OUT, "w"), indent=2)
    return OUT


if __name__ == "__main__":
    print(write())
