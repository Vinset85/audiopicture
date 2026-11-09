# Schema elettrico quadro cucina

**Fonte di verità:** solo lo schema tecnico vettoriale. I render fotorealistici generati da AI inventano collegamenti errati (es. ETH sulla barra PE, L/N scambiati, uscite sui morsetti sbagliati) e non vanno usati per l’impianto.

## File

- [`quadro-elettrico-cucina.png`](quadro-elettrico-cucina.png) — schema corretto
- [`quadro-elettrico-cucina.svg`](quadro-elettrico-cucina.svg) — sorgente vettoriale
- [`generate_quadro_cucina.py`](generate_quadro_cucina.py) — generatore

## Cablaggio corretto

1. **L rete / N rete** entrano dall’**alto** del RCBO.
2. Uscite RCBO → **BUS L** (marrone) e **BUS N** (blu).
3. Ogni Shelly Pro 4PM: **L** sul morsetto alto centrale; **N** sul morsetto basso; terminali alti `O4 O3 L O2 O1`.
4. Ogni **Ox** → MCB 16A → carico; il neutro del carico torna alla **morsettiera N**.
5. **ETH 1 / ETH 2** solo sulle porte **LAN** (mai su PE / S / L / N).
6. **S1–S4** non collegati in questo quadro.
7. **Barra PE** separata (giallo/verde).

## Mappa carichi

| # | Carico | Modulo | Terminale |
|--:|---|---|---|
| 1 | Lavastoviglie | Shelly #1 | O1 |
| 2 | Microonde | Shelly #1 | O2 |
| 3 | Forno | Shelly #1 | O3 |
| 4 | Frigorifero | Shelly #1 | O4 |
| 5 | Piano cottura | Shelly #2 | O1 |
| 6 | Prese piano cottura | Shelly #2 | O2 |
| 7 | Prese piano lavoro | Shelly #2 | O3 |
| 8 | Prese interno mobile | Shelly #2 | O4 |

```bash
python3 docs/electrical/generate_quadro_cucina.py
```
