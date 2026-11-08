# Schema elettrico quadro cucina

Schema di cablaggio corretto del quadro cucina basato sul bozzetto a mano e sullo schema ufficiale Shelly Pro 4PM.

## File

- [`quadro-elettrico-cucina.png`](quadro-elettrico-cucina.png) — schema pronto da stampare
- [`quadro-elettrico-cucina.svg`](quadro-elettrico-cucina.svg) — vettoriale modificabile
- [`generate_quadro_cucina.py`](generate_quadro_cucina.py) — generatore SVG/PNG

## Architettura

1. **Magnetotermico differenziale (RCBO)** protegge L + N in ingresso.
2. **BUS L** e **BUS N** alimentano due **Shelly Pro 4PM**.
3. Ogni uscita `Ox` fornisce la fase commutata al carico; il neutro torna al BUS N.
4. **ETH 1 / ETH 2** collegano le porte LAN dei due moduli.
5. Ingressi interruttore **S1–S4** non usati in questo quadro.

## Mappa carichi

| Circuito | Carico | Modulo | Terminale |
|---:|---|---|---|
| 1 | Lavastoviglie | Shelly #1 | O1 |
| 2 | Microonde | Shelly #1 | O2 |
| 3 | Forno | Shelly #1 | O3 |
| 4 | Frigorifero | Shelly #1 | O4 |
| 5 | Piano cottura | Shelly #2 | O1 |
| 6 | Prese piano cottura | Shelly #2 | O2 |
| 7 | Prese piano lavoro | Shelly #2 | O3 |
| 8 | Prese interno mobile | Shelly #2 | O4 |

## Limiti Shelly Pro 4PM

Verificare in opera correnti e sezioni: tipicamente max **16 A per canale** e **40 A totali** per modulo. Forno e piano cottura possono richiedere protezione dedicata o moduli diversi se superano questi limiti.

Rigenerazione:

```bash
python3 docs/electrical/generate_quadro_cucina.py
```
