"""Summarise a kicad-cli DRC JSON report."""
import collections
import json
import sys

d = json.load(open(sys.argv[1]))
filt = sys.argv[2] if len(sys.argv) > 2 else None
for key in ("violations", "unconnected_items", "schematic_parity"):
    items = d.get(key, [])
    c = collections.Counter((v["type"], v["severity"]) for v in items)
    print(key, len(items), dict(c))
    shown = collections.Counter()
    for v in items:
        desc = " | ".join(i["description"] for i in v.get("items", []))
        if filt and filt not in desc:
            continue
        if shown[v["type"]] < int(sys.argv[3] if len(sys.argv) > 3 else 6):
            shown[v["type"]] += 1
            pos = v["items"][0]["pos"] if v.get("items") else {}
            print("   %-24s %s  @(%.1f,%.1f)" % (v["type"], desc[:170], pos.get("x", 0) - 6, 94 - pos.get("y", 0)))
