# Schema elettrico quadro cucina

Vista del quadro cucina con RCBO + 2× Shelly Pro 4PM.

## File

- [`quadro-elettrico-cucina.png`](quadro-elettrico-cucina.png) — schema tecnico ad alta fedeltà (vettoriale rasterizzato)
- [`quadro-elettrico-cucina.svg`](quadro-elettrico-cucina.svg) — sorgente vettoriale
- [`quadro-elettrico-cucina-foto.jpg`](quadro-elettrico-cucina-foto.jpg) — render fotorealistico dell’armadio
- [`generate_quadro_cucina.py`](generate_quadro_cucina.py) — generatore SVG/PNG

## Architettura

1. Armadio DIN con canaline, piastra forata, barra N e PE
2. RCBO 2P 40A 30mA (ingresso alto, uscita verso BUS)
3. Due Shelly Pro 4PM (O4 O3 L O2 O1 / LAN N S4–S1)
4. MCB 16A di canale verso i carichi 1–8
5. ETH 1 / ETH 2; S1–S4 non usati

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

Rigenerazione schema tecnico:

```bash
python3 docs/electrical/generate_quadro_cucina.py
```
