"""Compare the kicad-cli netlist export with circuit.nets() (pin-exact)."""
import sys
import kilib
import circuit


def main(path):
    t = kilib.parse(open(path).read())
    nets = {}
    for n in kilib.find(kilib.first(t, "nets"), "net"):
        name = kilib.sval(kilib.first(n, "name")[1])
        nets[name] = sorted((kilib.sval(kilib.first(nd, "ref")[1]), kilib.sval(kilib.first(nd, "pin")[1]))
                            for nd in kilib.find(n, "node"))
        cls = kilib.first(n, "class")
    ref = circuit.nets()
    bad = [n for n in ref if sorted(ref[n]) != nets.get(n)]
    extra = [n for n in nets if n not in ref and not n.startswith("unconnected-")]
    print(f"netlist nets {len(nets)}  circuit nets {len(ref)}  mismatched {len(bad)}  extra {len(extra)}")
    for n in bad[:10]:
        print("  ", n, ref[n], nets.get(n))
    return not bad and not extra


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1]) else 1)
