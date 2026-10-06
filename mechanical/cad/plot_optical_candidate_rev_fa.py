"""Static engineering drawing from the executed optical candidate report."""
from pathlib import Path
import json, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Polygon

repo=Path(__file__).resolve().parents[2]
report=json.loads((repo/'evidence/rev-fa/execution.json').read_text())
out=repo/'evidence/rev-fa/optical-layout.png'
fig=plt.figure(figsize=(12,7.7));gs=fig.add_gridspec(1,2,width_ratios=[0.85,1.6],left=.07,right=.98,bottom=.30,top=.80,wspace=.30)
a,b=fig.add_subplot(gs[0]),fig.add_subplot(gs[1])
asa='#aab1b6';green='#237850';pcb='#4d6978';dml='#d9ad65'
a.add_patch(Rectangle((309.2,35),10,24,color=asa,label='Supporto frontale ASA'))
a.add_patch(FancyBboxPatch((310.6,42.8),6.6,8.4,boxstyle='round,pad=0,rounding_size=1.2',facecolor='white',edgecolor='black',lw=1))
a.add_patch(Rectangle((311.3,43),5.2,8,fill=False,ls='--',edgecolor=pcb,lw=1.4,label='Sagoma scheda fissa'))
a.add_patch(Rectangle((312.85,45.95),2.1,2.1,facecolor=green,alpha=.8,label='Ingombro OPT3004'))
a.plot([313.9],[47],'+',color='black');a.annotate('6,6 × 8,4 mm\nR 1,2 mm',(314,43),xytext=(314,38),ha='center',fontsize=10,arrowprops={'arrowstyle':'-','lw':.8})
a.set(xlim=(308.7,319.8),ylim=(34,60),xlabel='X [mm]',ylabel='Y [mm]',title='Vista frontale — dettaglio bordo destro');a.set_aspect('equal');a.legend(loc='upper center',fontsize=8,frameon=False)

b.add_patch(Rectangle((308,0),12,.5,color='#d4d4d4',label='Tessuto; trasmissione da misurare'))
for x,w in [(309.2,1.4),(317.2,2)]:b.add_patch(Rectangle((x,.5),w,1.8,color=asa))
b.add_patch(Rectangle((308,3.3),2,6,color=dml,label='Volume DML congelato'))
b.add_patch(Rectangle((311.3,3.35),5.2,.8,color=pcb,label='Scheda ottica — ingombro'))
b.add_patch(Rectangle((312.85,2.7),2.1,.65,color=green,label='OPT3004 — ingombro massimo'))
b.add_patch(Rectangle((310.4,6),6.4,2.4,color='#6c6f73',alpha=.65,label='Flangia telaio EU.11, sezione locale'))
r=(3.35-.5)*math.tan(math.radians(35))
b.add_patch(Polygon([(312.85,3.35),(312.85-r,.5),(314.95+r,.5),(314.95,3.35)],facecolor=green,alpha=.10,edgecolor=green,lw=1))
for x,sign in [(312.85,-1),(314.95,1)]:b.plot([x,x+sign*r],[3.35,.5],color=green,lw=1.2)
b.annotate('Cono ±35° per tutta\nla proiezione del sensore',(316.5,.9),xytext=(317.1,4.2),fontsize=10,ha='left',arrowprops={'arrowstyle':'-','lw':.8})
b.annotate('Margine sul DML\n1,30 mm (scheda)',(311.3,4.15),xytext=(308.25,5.3),fontsize=9,ha='left',arrowprops={'arrowstyle':'-','lw':.8})
b.set(xlim=(308,320),ylim=(10.3,-.4),xlabel='X [mm]',ylabel='Z [mm] — crescente verso il retro',title='Sezione X–Z a Y = 47 mm');b.set_aspect('equal');b.legend(loc='lower center',fontsize=8,frameon=False)
for ax in [a,b]:ax.spines[['top','right']].set_visible(False);ax.grid(alpha=.14)
fig.suptitle('Sensore di luce: percorso libero sul perimetro',x=.07,y=.965,ha='left',fontsize=18,fontweight='bold')
fig.text(.07,.902,'Rev.FA · candidato CAD verificato · il pannello DML resta integro',fontsize=12)
fig.text(.07,.168,f"Campo nominale libero: ±{report['analytical_all_azimuth_clear_half_angle_deg']:.2f}° sull’intero ingombro del sensore.\nA ±35° rimangono {report['35_deg_remaining_combined_lateral_allowance_mm']:.3f} mm da ripartire tra errori di posizione e profondità.",fontsize=11,color=green)
fig.text(.07,.072,'Fonte: CadQuery/OCC, execution.json Rev.FA; dimensioni massime TI OPT3004DNPR. Nessuna simulazione radiometrica.\nDisegno di studio: fissaggio, collegamento, baffle e tolleranze restano da completare.\nIl coupon verifica forma/allineamento; non dimostra calibrazione lux o resistenza del frontale.',fontsize=10,color='#444444')
fig.savefig(out,dpi=180);plt.close(fig);print(out)
