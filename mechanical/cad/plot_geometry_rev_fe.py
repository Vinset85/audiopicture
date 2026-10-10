"""Scientific inspection figures from the executed STEP artifacts."""
import hashlib
import json
from pathlib import Path
import cadquery as cq
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
repo=Path(__file__).resolve().parents[2]; out=repo/'evidence/rev-fe'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
parts=[('Telaio EU.22','evidence/rev-eu22/AP22_FRAME_CANDIDATE_REV_EU.step','#357f9c'),
       ('Scocca con pareti laterali','evidence/rev-fe/sidewalls-eu22/AP22_SHELL_SIDEWALL_CANDIDATE_REV_FE.step','#b48148')]
fig=plt.figure(figsize=(14,7)); sources={}; counts={}
for i,(title,path,color) in enumerate(parts):
    p=repo/path; shape=cq.importers.importStep(str(p)).val(); assert shape.isValid()
    vertices,tri=shape.tessellate(.15,.18); xyz=np.array([v.toTuple() for v in vertices])
    ax=fig.add_subplot(1,2,i+1,projection='3d')
    facets=xyz[np.array(tri)]
    normals=np.cross(facets[:,1]-facets[:,0],facets[:,2]-facets[:,0])
    lengths=np.linalg.norm(normals,axis=1)
    normals/=np.maximum(lengths[:,None],1e-30)
    light=np.array([-.4,-.4,-.82]);light/=np.linalg.norm(light)
    # Two-sided inspection lighting: coplanar OCC facets get identical shade
    # even when their underlying face orientation differs.
    intensity=.4+.6*np.abs(normals@light)
    colors=np.tile(to_rgba(color),(len(facets),1)); colors[:,:3]*=intensity[:,None]
    ax.add_collection3d(Poly3DCollection(facets,facecolors=colors,edgecolors='none'))
    ax.set(xlim=(0,320),ylim=(0,400),zlim=(0,40),xlabel='X (mm)',ylabel='Y (mm)',zlabel='Z (mm)')
    ax.set_box_aspect((320,400,100)); ax.view_init(elev=-63,azim=-68)
    ax.set_zticks([0,20,40]); ax.set_title(title,fontsize=15,pad=18)
    sources[path]=sha(p);counts[path]=len(tri)
fig.suptitle('AudioPicture · candidati CAD Rev.FE, vista interna',fontsize=18,y=.98)
fig.text(.06,.04,'Geometrie STEP effettive. Asse Z amplificato 2,5×. Giunti, tenute e passaggi di servizio ancora da completare.\n'
         'Telaio con fori FEM provvisori; nessun congelamento produttivo o risultato CFD implicito.',fontsize=10)
fig.subplots_adjust(bottom=.15,top=.87,left=.02,right=.98,wspace=.1)
fig.savefig(out/'geometry-candidates.png',dpi=150,facecolor='white'); plt.close(fig)
sources[str(Path(__file__).relative_to(repo))]=sha(Path(__file__))
(out/'geometry-figure.json').write_text(json.dumps({'classification':'CALCULATED_CAD_INSPECTION_NOT_RELEASE',
    'source_sha256':sources,'triangles':counts,'Z_visual_scale':2.5},indent=2)+'\n')
print(out/'geometry-candidates.png')
