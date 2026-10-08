"""Render the actual candidate STEP as a scientific CAD inspection figure."""
from pathlib import Path
import hashlib
import json
import cadquery as cq
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

repo = Path(__file__).resolve().parents[2]
step = repo / 'evidence/rev-eu20/AP22_FRAME_CANDIDATE_REV_EU.step'
cad = json.loads((step.parent / 'execution.json').read_text())
assert hashlib.sha256(step.read_bytes()).hexdigest() == cad['sha256']
shape = cq.importers.importStep(str(step)).val()
vertices, triangles = shape.tessellate(.2, .15)
xyz = np.asarray([v.toTuple() for v in vertices])
faces = xyz[np.asarray(triangles)]
fig = plt.figure(figsize=(11, 8))
ax = fig.add_subplot(111, projection='3d')
surface = Poly3DCollection(faces, facecolors='#4384a0', edgecolors='#214658', linewidths=.12)
ax.add_collection3d(surface)
ax.set(xlim=(0,320), ylim=(0,400), zlim=(0,40), xlabel='X (mm)', ylabel='Y (mm)', zlabel='Z (mm)')
ax.set_box_aspect((320,400,100))
ax.set_zticks([0,20,40])
ax.view_init(elev=58, azim=-72)
ax.set_title('AudioPicture · telaio candidato EU.20', loc='left', pad=22, fontsize=17)
fig.text(.08,.045, f'Massa calcolata {cad["mass_g_at_catalog_density_1p22"]:.2f} g · PC-CF a 1,22 g/cm³ di catalogo\n'
         'STEP realmente generato. Asse Z amplificato 2,5× per ispezione; non CAD congelato per produzione.', fontsize=10)
out = repo / 'evidence/rev-fd'; out.mkdir(parents=True, exist_ok=True)
fig.savefig(out / 'frame-candidate.png', dpi=160, facecolor='white', bbox_inches='tight')
(out/'geometry-figure.json').write_text(json.dumps({'classification':'CALCULATED_CAD_INSPECTION_FIGURE_NOT_RELEASE',
    'step_sha256':cad['sha256'], 'triangles':len(triangles), 'Z_visual_scale':2.5,
    'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}, indent=2)+'\n')
print(out / 'frame-candidate.png')
