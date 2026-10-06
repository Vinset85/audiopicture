"""Plot measured solver outputs with explicit screening scope, no inferred margins."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

repo = Path(__file__).resolve().parents[2]
new = json.loads((repo / 'mechanical/validation/rev-fb/summary.json').read_text())['frames_rev_fb']
old = json.loads((repo / 'mechanical/validation/rev-fa/summary.json').read_text())['frame_EU12']
labels = ['EU.12', 'EU.13', 'EU.14']
colors = ['#ae4850', '#c38622', '#236d94']
mass = [old['CAD']['volume_mm3']*.00122] + [new[n]['CAD']['mass_g_at_catalog_density_1p22'] for n in ['EU13','EU14']]
values = {}
for case in ['LC1', 'LC3', 'LC4']:
    entries = [old[case]] + [new[n]['cases'][case] for n in ['EU13','EU14']]
    values[case] = [max(e['corner_max_abs_UZ_mm'].values()) if case == 'LC4' else e['max_displacement_mm'] for e in entries]
fig, axes = plt.subplots(2, 2, figsize=(11, 7.5))
for ax, series, title, unit, limit in [
    (axes[0,0], mass, 'Massa del solo candidato', 'g', 250),
    (axes[0,1], values['LC1'], 'LC1 · 70 N verticali: spostamento massimo', 'mm', None),
    (axes[1,0], values['LC3'], 'LC3 · 50 N verso l’esterno: spostamento massimo', 'mm', None),
    (axes[1,1], values['LC4'], 'LC4 · 30 N: spostamento normale agli angoli', 'mm', 1)]:
    bars = ax.bar(labels, series, color=colors, width=.56)
    ax.bar_label(bars, labels=[f'{v:.3f}' for v in series], padding=4)
    ax.set_title(title, loc='left', fontsize=10, pad=12)
    ax.set_ylabel(unit)
    ax.set_ylim(0, max(series)*1.23)
    ax.spines[['top','right']].set_visible(False)
    ax.set_axisbelow(True); ax.grid(axis='y', alpha=.18)
    if limit is not None:
        ax.axhline(limit, color='#a82020', ls='--', lw=1)
        ax.text(.98, .94, f'Limite {limit:g} {unit}', transform=ax.transAxes, va='top', ha='right', color='#a82020', fontsize=9)
fig.suptitle('AudioPicture · confronto diagnostico dei telai', fontsize=17, x=.065, ha='left', y=.98)
fig.text(.065,.016, 'MAT-B non qualificato, attacchi ideali, una mesh per candidato. LC1 non verifica la cedevolezza degli attacchi.\nLC3 senza contatto DML: 2.669 nodi interferenti in EU.12; nessuno nei campioni EU.13/EU.14. Non è una verifica completa di clearance.', fontsize=9, color='#41464d')
fig.tight_layout(rect=[.035,.075,.98,.95], h_pad=2.6, w_pad=3)
out=repo/'evidence/rev-fb/frame-comparison.png'
fig.savefig(out, dpi=170, facecolor='white')
print(out)
