# AudioPicture V2.2 six-point shell retention topology Rev.AN
# Packaging node centers only; fastener MPN and final boss geometry remain open.
import json, math
R=5.0
nodes=[("TOP_L",145.,383.),("TOP_R",175.,383.),("SIDE_L",12.,200.),("SIDE_R",308.,200.),("BOT_L",80.,17.),("BOT_R",240.,17.)]
ex=[
("CLEAT_L",(25.5,79.5,352,390)),("CLEAT_R",(240.5,294.5,352,390)),
("UPPER_VENT_L",(0,129,339,400)),("UPPER_VENT_R",(191,320,339,400)),
("LOWER_VENT_L",(0,16,2,146)),("LOWER_VENT_R",(304,320,2,146)),
("SERVICE",(100,220,20,48)),("ANTILIFT",(145,175,12,24)),
("ESP32_RF_COARSE",(64,119.5,318.5,366.5)),("MAIN_C",(85,235,315,370))]
def hit(x,y,rct):
 a,b,c,d=rct;return a-R<=x<=b+R and c-R<=y<=d+R
hits={n:[e for e,r in ex if hit(x,y,r)] for n,x,y in nodes}
# top nodes require dedicated PC-CF tabs from top ring inner edge y388 toward y383.
# Seed tab: 12x12 projected square around node, fused to top ring y388..398.
tabs=[("TAB_TOP_L",(139.,151.,378.,390.)),("TAB_TOP_R",(169.,181.,378.,390.))]
# verify top tab boxes themselves avoid upper vent bounding envelopes and MAIN-C/cleats/RF.
tab_ex=[e for e in ex if e[0] not in ("SERVICE","ANTILIFT","LOWER_VENT_L","LOWER_VENT_R")]
tab_hits={}
for tn,(a,b,c,d) in tabs:
 hh=[]
 for en,(x0,x1,y0,y1) in tab_ex:
  if min(b,x1)>max(a,x0) and min(d,y1)>max(c,y0):hh.append(en)
 tab_hits[tn]=hh
mind=min(math.hypot(a[1]-b[1],a[2]-b[2]) for i,a in enumerate(nodes) for b in nodes[i+1:])
assert all(not v for v in hits.values())
assert all(not v for v in tab_hits.values())
print(json.dumps({"node_radius_screen_mm":R,"nodes":nodes,"node_exclusion_hits":hits,
"top_tab_seed_boxes":tabs,"top_tab_exclusion_hits":tab_hits,"minimum_node_spacing_mm":mind,
"architecture":"6 point: 2 top dedicated PC-CF tabs + 2 side ring + 2 bottom ring",
"limitations":["fastener MPN/hole diameter/insert open","top tab section and FEA open","exact frame B-rep fusion required","exact radar RF mask open","5mm radius is packaging screen only"]},indent=2))
