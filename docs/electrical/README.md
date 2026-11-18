# Schema elettrico quadro cucina

## File

- [`quadro-elettrico-cucina-foto.jpg`](quadro-elettrico-cucina-foto.jpg) — **render** con foto componenti reali
- [`quadro-elettrico-cucina.png`](quadro-elettrico-cucina.png) / [`.svg`](quadro-elettrico-cucina.svg) — schema tecnico
- [`components/`](components/) — cutout Shelly ufficiale + RCBO
- [`generate_quadro_cucina.py`](generate_quadro_cucina.py) / [`generate_quadro_cucina_render.py`](generate_quadro_cucina_render.py)

### Foto componenti
- **Shelly Pro 4PM**: immagine ufficiale [shelly.com](https://www.shelly.com/cdn/shop/files/Shelly-Pro-4PM-main-image.png?v=1749538954)
- **RCBO**: cutout prodotto 2P 40A 30mA Tipo A

Il cablaggio sopra le foto è disegnato dal codice (topologia corretta), non inventato dall’AI.

## Cablaggio corretto

1. **L/N rete** → morsetti **alti** del RCBO  
2. Uscite RCBO → **BUS L** / **BUS N**  
3. Shelly: **L** alto centrale, **N** basso  
4. **Ox** → MCB 16A → carico; neutro → **MORSETTIERA N**  
5. **ETH1/ETH2** solo porte **LAN**  
6. **S1–S4** non usati; **PE** separata  

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
python3 docs/electrical/generate_quadro_cucina_render.py
```
