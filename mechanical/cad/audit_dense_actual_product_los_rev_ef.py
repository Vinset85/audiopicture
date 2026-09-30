# AudioPicture V2.2 dense actual-product acoustic LOS audit Rev.EF
# Geometric screening only; NOT an acoustic attenuation simulation.
import cadquery as cq,json,math
X=320.;Y=400.;R=1.5;EPS=0.02
def box(x0,x1,y0,y1,z0,z1):return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
lowerL=[("V",17,20,14,54),("V",24,27,14,54),("V",17,20,62,102),("V",24,27,62,102),("V",17,20,110,150),("V",24,27,110,150)]
upperL=[("H",17,62,315,318),("H",17,62,322,325),("H",17,62,329,332),("H",17,62,336,339),("H",17,62,343,346)]
def mirror(c):o,x0,x1,y0,y1=c;return(o,X-x1,X-x0,y0,y1)
vents=[("IL"+str(i+1),)+c for i,c in enumerate(lowerL)]+[("IR"+str(i+1),)+mirror(c) for i,c in enumerate(lowerL)]+[("UL"+str(i+1),)+c for i,c in enumerate(upperL)]+[("UR"+str(i+1),)+mirror(c) for i,c in enumerate(upperL)]
def cap(row,zlo,zhi,eps=0.):
 n,o,x0,x1,y0,y1=row;x0-=eps;x1+=eps;y0-=eps;y1+=eps
 if o=="H":
  cy=(y0+y1)/2;rr=(y1-y0)/2;xa=x0+rr;xb=x1-rr
  return cq.Workplane("XY",origin=(0,0,zlo)).moveTo(xa,cy-rr).lineTo(xb,cy-rr).threePointArc((x1,cy),(xb,cy+rr)).lineTo(xa,cy+rr).threePointArc((x0,cy),(xa,cy-rr)).close().extrude(zhi-zlo)
 cx=(x0+x1)/2;rr=(x1-x0)/2;ya=y0+rr;yb=y1-rr
 return cq.Workplane("XY",origin=(0,0,zlo)).moveTo(cx-rr,ya).lineTo(cx-rr,yb).threePointArc((cx,y1),(cx+rr,yb)).lineTo(cx+rr,ya).threePointArc((cx,y0),(cx-rr,ya)).close().extrude(zhi-zlo)
# Rev.DX/EC obstacle solid
solid=box(0,320,0,400,37.8,40)
for a,b,c,d in [(0,2.2,148,337),(317.8,320,148,337),(18,302,0,2.2),(18,302,397.8,400)]:solid=solid.union(box(a,b,c,d,35.6,37.8))
for row in vents:solid=solid.cut(cap(row,37.58,40.22,EPS))
for x,y in [(145,383),(175,383),(12,200),(308,200),(80,17),(240,17)]:solid=solid.union(cq.Workplane("XY",origin=(x,y,36)).circle(5).extrude(1.8))
L=36.;CHL=24.;CHW=36.;EXIT=16.;OV=12.;ROOF=36.8;T=1.;ZT=37.85
def left(y0,zl):
 x0=15.;x1=51.;y1=y0+48
 ss=[box(x0,x1,y0,y1,ROOF,ZT),box(x0,x0+T,y0,y1,zl,ROOF),box(x0,x1,y0,y0+T,zl,ROOF)]
 cx0=x1-CHL;cx1=x1;cy0=y1-CHW;cy1=y1
 ss += [box(cx1-T,cx1,cy0,cy1,zl,ROOF),box(cx0,cx1,cy0,cy0+T,zl,ROOF)]
 ex0=cx0+T;ex1=min(cx1-T,ex0+EXIT)
 ss += [box(cx0,ex0,cy1-T,cy1,zl,ROOF),box(ex1,cx1,cy1-T,cy1,zl,ROOF)]
 bx=min(cx1-T,cx0+T+EXIT+OV);ss.append(box(bx-T,bx,cy0+T,cy1-T,zl,ROOF))
 s=ss[0]
 for q in ss[1:]:s=s.union(q)
 for row in vents:s=s.cut(cap(row,36.58,38.02,EPS))
 return s.clean()
def mx(s):return s.mirror("YZ",basePointVector=(160,0,0))
for p in [left(14,34),mx(left(14,34)),left(315,35.1),mx(left(315,35.1))]:solid=solid.union(p)
solid=solid.clean()
# 9 source samples per aperture, inset from capsule boundary.
def samples(row):
 n,o,x0,x1,y0,y1=row
 pts=[]
 if o=="V":
  cx=(x0+x1)/2
  for dx in (-0.7,0,0.7):
   for fy in (.12,.50,.88):pts.append((cx+dx,y0+(y1-y0)*fy,40.18))
 else:
  cy=(y0+y1)/2
  for fx in (.12,.50,.88):
   for dy in (-0.7,0,0.7):pts.append((x0+(x1-x0)*fx,cy+dy,40.18))
 return pts
# Multiple destinations distributed in free internal cavity below labyrinth.
dest=[(160,200,33.5),(80,200,33.5),(240,200,33.5),(160,80,33.5),(160,300,33.5),
      (60,180,34.0),(260,180,34.0),(100,260,34.0),(220,260,34.0)]
# Ray represented as a thin cylinder; any obstacle intersection blocks LOS.
def ray(a,b,r=.04):
 ax,ay,az=a;bx,by,bz=b;vx=bx-ax;vy=by-ay;vz=bz-az;L=math.sqrt(vx*vx+vy*vy+vz*vz)
 if L==0:return None
 return cq.Workplane("XY",origin=a).transformed(rotate=(0,math.degrees(math.atan2(math.sqrt(vx*vx+vy*vy),vz)),math.degrees(math.atan2(vy,vx)))).circle(r).extrude(L)
# More robust: use OCC edge distance to obstacle rather than relying on cylinder orientation.
def open_ray(a,b):
 e=cq.Edge.makeLine(cq.Vector(*a),cq.Vector(*b))
 # Ignore tiny contact near source by starting 0.20 mm below outer point.
 v=cq.Vector(b[0]-a[0],b[1]-a[1],b[2]-a[2]);ln=v.Length;u=v.multiply(1.0/ln)
 aa=cq.Vector(a[0]+u.x*.20,a[1]+u.y*.20,a[2]+u.z*.20)
 ee=cq.Edge.makeLine(aa,cq.Vector(*b))
 d=solid.val().distance(ee)
 return d>1e-5,d
per={};total=0;opened=0;mind=1e9
examples=[]
for row in vents:
 oc=0;md=1e9
 for a in samples(row):
  for b in dest:
   op,d=open_ray(a,b);total+=1;md=min(md,d);mind=min(mind,d)
   if op:
    oc+=1;opened+=1
    if len(examples)<20:examples.append({"vent":row[0],"source":a,"dest":b,"clearance_mm":d})
 per[row[0]]={"rays":len(samples(row))*len(dest),"open":oc,"min_obstacle_distance_mm":md}
print(json.dumps({"source_samples_per_vent":9,"destinations":len(dest),"total_rays":total,
"open_rays":opened,"blocked_rays":total-opened,"per_vent":per,"open_examples":examples,
"decision":"PASS" if opened==0 else "FAIL",
"interpretation":"Zero open rays is geometric LOS screening only; it is not acoustic attenuation proof."},indent=2))
