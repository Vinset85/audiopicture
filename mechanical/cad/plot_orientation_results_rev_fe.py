"""Plot measured solver outputs, not a product-performance illustration."""
from pathlib import Path
import hashlib
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

repo=Path(__file__).resolve().parents[2]
entries=[
 ('EU.20 · debole Z · M0','EU20/M0-LC4-LR-Ez020-G025/LC4'),
 ('EU.21 · debole Z · M0','EU21/M0-LC4-LR-Ez020-G025/LC4'),
 ('EU.22 · debole Z · M0','EU22/M0-LC4-LR-Ez020-G025/LC4'),
 ('EU.22 · debole Z · M1','EU22/M1-LC4-LR-Ez020-G025/LC4'),
 ('EU.20 · debole X · M0','EU20/M0-LC4-LR-Ez020-G025-weakX/LC4'),
 ('EU.20 · debole Y · M0','EU20/M0-LC4-LR-Ez020-G025-weakY/LC4'),
]
paths=[repo/'evidence/rev-fe'/run/'metrics.json' for _,run in entries]
rows=[json.loads(p.read_text()) for p in paths]
assert all(r['solver_execution_pass'] and r['final_step_time']==1 for r in rows)
values=[max(r['corner_max_abs_UZ_mm'].values()) for r in rows]
fig,ax=plt.subplots(figsize=(11.5,6.8));fig.subplots_adjust(left=.29,right=.95,top=.81,bottom=.28)
fig.patch.set_facecolor('#faf9f6');ax.set_facecolor('#faf9f6')
colors=['#b1513d' if v>1 else '#35746c' for v in values]
bars=ax.barh(range(len(values)),values,color=colors,height=.6)
ax.set_yticks(range(len(values)),[x[0] for x in entries]);ax.invert_yaxis()
ax.axvline(1,color='#30343b',ls='--',lw=1.1);ax.set_xlim(0,3.55)
ax.set_xlabel('Massimo |UZ| degli angoli nel caso LC4 destro inferiore [mm]')
ax.spines[['top','right','left']].set_visible(False);ax.grid(axis='x',alpha=.16);ax.set_axisbelow(True)
for bar,value in zip(bars,values):
 ax.text(value+.045,bar.get_y()+bar.get_height()/2,f'{value:.6f}',va='center',fontsize=10)
fig.text(.06,.935,'La massa da sola non chiude la verifica',fontsize=20,weight='bold',color='#202830')
fig.text(.06,.875,'Rev.FE · carico 30 N · stesso seme debole E3/E1 = 0,20 e G13/G12 = G23/G12 = 0,25',fontsize=10.5)
fig.text(.06,.095,'Linea tratteggiata: criterio 1 mm. Il colore indica soltanto questo criterio del modello.\nMateriale ipotizzato e attacchi ideali. Debole Y presenta interferenze DML nei separati LC1 lineari.\nNessuna configurazione è qualificata per produzione; M0/M1 confrontano soltanto lo spostamento.',fontsize=10,color='#424a53')
out=repo/'evidence/rev-fe/orientation-results.png';fig.savefig(out,dpi=160);plt.close(fig)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
report={'classification':'SCIENTIFIC_FIGURE_FROM_EXECUTED_SOLVER_METRICS','source_sha256':{str(p.relative_to(repo)):sha(p) for p in paths+[Path(__file__)]},'artifact_sha256':{str(out.relative_to(repo)):sha(out)},'values_mm':values}
(out.parent/'orientation-figure.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
