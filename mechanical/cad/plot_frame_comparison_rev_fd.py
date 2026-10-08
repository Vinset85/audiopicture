"""Plot actual CAD masses and executed, explicitly scoped M0 displacement screens."""
from pathlib import Path
import hashlib
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

repo=Path(__file__).resolve().parents[2]
specs=[(18,'M0-linear-MAT-B','M0-contactK100k-MAT-B'),
       (19,'M0-linear70-MAT-B','M0-contactK100k-MAT-B-LR'),
       (20,'M0-linear70-MAT-B','M0-contactK100k-MAT-B-LR')]
rows=[];sources=[Path(__file__)]
for n,linear,torsion in specs:
    paths=[repo/f'evidence/rev-eu{n}/execution.json',
           repo/f'evidence/rev-ev{n}/{linear}/LC1/metrics.json',
           repo/f'evidence/rev-ev{n}/{torsion}/LC4/metrics.json']
    cad,lc1,lc4=[json.loads(p.read_text()) for p in paths]
    assert lc1['solver_execution_pass'] and lc4['solver_execution_pass']
    rows.append({'candidate':f'EU.{n}','mass_g':cad['mass_g_at_catalog_density_1p22'],
                 'LC1_70N_max_resultant_mm':lc1['max_displacement_mm'],
                 'LC4_30N_LR_max_corner_UZ_mm':max(lc4['corner_max_abs_UZ_mm'].values())})
    sources+=paths
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(1,3,figsize=(13,5.5))
labels=[r['candidate'] for r in rows];colors=['#a4a9af','#5481a0','#297568']
for ax,key,title in zip(axes,['mass_g','LC1_70N_max_resultant_mm','LC4_30N_LR_max_corner_UZ_mm'],
                       ['Massa CAD a densità di catalogo (g)','Verticale 70 N · massimo risultante (mm)','Torsione 30 N · angolo inferiore destro (mm)']):
    values=[r[key] for r in rows]
    bars=ax.bar(labels,values,color=colors,width=.6)
    ax.set_title(title,fontsize=10,pad=17)
    ax.set_ylim(0,max(values)*1.2)
    for bar,value in zip(bars,values):
        ax.text(bar.get_x()+bar.get_width()/2,value+max(values)*.025,f'{value:.1f}' if key=='mass_g' else f'{value:.3f}',ha='center',fontsize=12)
    ax.yaxis.grid(True,alpha=.18);ax.set_axisbelow(True)
axes[2].axhline(1,color='#a44939',linestyle='--',linewidth=1.3,label='limite 1 mm')
axes[2].legend(loc='upper right',fontsize=9,frameon=False)
fig.suptitle('AudioPicture · confronto dei telai dopo la rimozione del limite di massa',fontsize=16,y=.98)
fig.text(.055,.08,'Risultati effettivi su mesh M0. Materiale ortotropo e fissaggi sono modelli di screening.\n'
         'Geometria e discretizzazione cambiano; nessuna qualifica di resistenza o del prodotto. LC1 usa i soli vincoli superiori.',fontsize=10)
fig.subplots_adjust(left=.055,right=.985,bottom=.25,top=.80,wspace=.30)
out=repo/'evidence/rev-fd'
fig.savefig(out/'frame-comparison.png',dpi=160,facecolor='white')
(out/'frame-comparison.json').write_text(json.dumps({'classification':'PLOT_OF_CALCULATED_MASS_AND_SIMULATED_NORMALIZED_DISPLACEMENTS',
    'rows':rows,'source_sha256':{str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}},indent=2)+'\n')
print(rows)
