"""True-scale scientific sections of the reimported mounting assembly."""
import hashlib,json
from pathlib import Path
import cadquery as cq
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Patch

ROOT=Path(__file__).resolve().parents[2];out=ROOT/'evidence/rev-fg'
manifest=out/'upper-mounts-chamfer/execution.json';r=json.loads(manifest.read_text())
colors={'frame':('#668fa5','Telaio PC-CF'),'shell':('#d5ab70','Scocca ASA'),
        'PRODUCT_CLEAT_L':('#53764d','Cleat prodotto'),'WALL_CLEAT_L':('#343e48','Cleat parete'),
        'BOSS_SEAL_L1_COMPRESSED':('#bc6ea5','Guarnizione, forma compressa'),
        'BOSS_SEAL_L2_COMPRESSED':('#bc6ea5',None),
        'SCREW_L1_BOUNDING':('#77c7cd','Inviluppo vite svasata'),
        'SCREW_L2_BOUNDING':('#77c7cd',None),
        'WALL_HEAD_L_37.5_SPACE_ENVELOPE':('#9aaab7','Spazio testa fissaggio parete'),
        'WALL_HEAD_L_67.5_SPACE_ENVELOPE':('#9aaab7',None)}
parts={};sources={}
for n in colors:
    p=ROOT/r['artifacts'][n]['file'];sources[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    assert sources[str(p.relative_to(ROOT))]==r['artifacts'][n]['sha256']
    parts[n]=cq.importers.importStep(str(p)).val()
fig,axes=plt.subplots(1,2,figsize=(13,7.2))
for ax,x,title in zip(axes,[37.5,52.5],['Sezione sul fissaggio · X = 37,5 mm','Sezione del gancio · X = 52,5 mm']):
    plane=cq.Face.makePlane(basePnt=cq.Vector(x,0,0),dir=cq.Vector(1,0,0))
    for n,shape in parts.items():
        section=shape.intersect(plane)
        triangles=[]
        for face in section.Faces():
            vertices,faces=face.tessellate(.01,.05)
            xyz=np.array([v.toTuple() for v in vertices])
            if len(faces):triangles.extend(xyz[np.array(faces)][:,:,[1,2]])
        if triangles:ax.add_collection(PolyCollection(triangles,facecolors=colors[n][0],edgecolors='none'))
    ax.axhline(40,color='#b55243',ls='--',lw=1)
    ax.axhline(43,color='#343e48',lw=1)
    ax.fill_between([360,400],43,45,color='#eee9e0',hatch='///',edgecolor='#d6cfc5',linewidth=.3)
    ax.set(xlim=(362,400),ylim=(18,45),xlabel='Y (mm)',ylabel='Z (mm)',title=title)
    ax.set_aspect('equal');ax.grid(alpha=.15)
axes[1].text(362.5,40.2,'Z40 · limite corpo',color='#b55243',fontsize=8)
axes[1].text(362.5,43.35,'Parete · gap 3 mm',fontsize=8)
axes[1].annotate('Sollevare 7 mm\npoi estrarre verso il fronte',xy=(391,38),xytext=(377,21),
                  arrowprops=dict(arrowstyle='->',color='#343e48'),fontsize=9)
fig.suptitle('AudioPicture · fissaggi superiori Rev.FG',fontsize=19,y=.97)
handles=[Patch(facecolor=c,label=t) for c,t in colors.values() if t]
fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.09),ncol=3,frameon=False,fontsize=9)
fig.text(.055,.035,'Sezioni dei file STEP effettivi, scala uguale nei due assi. Geometria nominale candidata.\n'
         'Viti rappresentate da inviluppi; tenute, tolleranze, contatti deformabili e resistenza non qualificati.',fontsize=10)
fig.subplots_adjust(top=.87,bottom=.25,wspace=.2,left=.06,right=.98)
png=out/'mount-sections.png';fig.savefig(png,dpi=180,facecolor='white');plt.close(fig)
for p in [manifest,Path(__file__)]:sources[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
(out/'mount-sections-figure.json').write_text(json.dumps({'classification':'CALCULATED_STEP_CROSS_SECTIONS_NOT_PRODUCTION_RELEASE',
    'source_sha256':sources,'artifact_sha256':{str(png.relative_to(ROOT)):hashlib.sha256(png.read_bytes()).hexdigest()}},indent=2)+'\n')
print(png)
