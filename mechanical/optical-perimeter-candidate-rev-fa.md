# Percorso ottico sul perimetro — Rev.FA, 6 ottobre 2026

**Candidato geometrico verificato; integrazione e rilascio produttivo OPEN.**
La posizione ottica ENV precedente resta respinta da G52: il DML occupa tutto
il percorso normale davanti alla regione ENV. Non si presume che il pannello
sia trasparente. Rev.FA propone di separare fisicamente il sensore di luce dal
sensore di temperatura/umidità, mantenendo invariati dispositivi, indirizzi e
quattro reti elettriche. Lo schema ENV Rev.EZ non implementa ancora il nuovo
collegamento fisico tra le due parti.

## Configurazione eseguita

La piccola scheda ottica è riservata sul telaio fisso, dietro il bordo destro
del tessuto. Il frontale ASA rimane removibile. Non sono aggiunte tacche DML
né spostati i magneti; rimane la configurazione a otto stazioni 4 × 2 mm.

- Centro ottico X313,9 / Y47 mm; scheda di studio X311,3..316,5,
  Y43..51, Z3,35..4,15 mm. Spessore 0,8 mm: scelta progettuale da confermare.
- OPT3004DNPR: massimo d'ingombro di catalogo 2,1 × 2,1 × 0,65 mm;
  lato ottico verso il tessuto. Il condensatore C302 è riservato sul retro.
- Apertura nel supporto: X310,6..317,2 / Y42,8..51,2 mm, angoli R1,2;
  attraversa la base ASA Z0,5..2,3. Legamenti laterali nominali 1,4 e 2,0 mm.
- Trasformazione del carrier originale: +0,5 mm in Z, come Rev.F. Gli
  ispessimenti delle stazioni magnetiche raggiungono Z3,7 mm.

I dati dimensionali della nuova scheda e dell'apertura sono **ipotesi di
progetto**, non tolleranze del processo né dimensioni di una scheda ordinata.
Gli STEP degli ingombri elettronici sono parallelepipedi di controllo; non
sono modelli completi di componenti, saldature, connettori o PCB sbrogliati.

## Evidenze reali

Carrier modificato: BREP valido, un solido, volume 25551,913444 mm³; rimozione
di 97,567008 mm³ dal carrier ricostruito. STEP esportato e reimportato: volume
coincidente. Coupon locale: un solido valido, volume 334,432992 mm³, 10 × 24 ×
1,8 mm. Entrambi gli STL sono stati ricaricati: un corpo, chiusi e con
orientamento coerente delle facce. Questi controlli non qualificano la stampa.

Zero sovrapposizioni del nuovo carrier e dei tre ingombri con DML, maschere
ESP32/RADAR, regione ENV precedente, telaio EU.11, shell EQ e otto target
metallici. Scheda–DML **1,30 mm**, scheda–telaio **1,85 mm**; condensatore–telaio
**0,95 mm** nominali. Sono verificate anche sei posizioni di estrazione
rettilinea del frontale verso la stanza, da 0 a 40 mm. L'estrazione inclinata,
i supporti reali e il cavo restano da verificare.

Una parete laterale ipotizzata fino a Z0,5 intersecava il carrier esistente per
1034,699339 mm³. Il risultato respinto è conservato. La riserva della futura
parete destra parte ora da Z4,1, mantenendo 0,4 mm nominali dagli ispessimenti
del carrier. **La parete e la tenuta frontale non sono state realizzate da
questo studio:** l'involucro completo rimane OPEN.

## Campo visivo

La guida [TI OPT3004, SBOS929A, §9.1.2](https://www.ti.com/lit/ds/symlink/opt3004.pdf)
raccomanda almeno ±35°. Il valore tipico di catalogo 57° al 50% della risposta
descrive il sensore; non implica che questa finestra trasmetta tutti quei raggi.

Il controllo usa conservativamente **tutta la proiezione massima del package**,
non un punto centrale ideale, e il piano della scheda Z3,35 come origine più
arretrata possibile. Per ogni punto, la distanza minima dalla parete della
finestra è 2,25 mm. A ±35°, il disco di raggi proiettato sulla faccia Z0,5 ha
raggio 2,85 × tan(35°) = 1,995591 mm. La sua dilatazione dell'intero rettangolo
sorgente è contenuta nell'apertura convessa: questo prova il passaggio per
tutti gli azimut, non soltanto quelli campionati.

Risultati: **1.953/1.953 raggi liberi** a 0°, 15°, 30° e 35°; 153 raggi sono
anche confrontati con intersezioni indipendenti OCC a 0°, 35° e 45°.
Semiangolo nominale garantito sull'intera proiezione: **38,290°**. A 40°,
42/648 raggi campionati sono schermati; a 57°, 410/648. Non viene dichiarata
assenza di schermatura oltre il campo verificato.

Margine residuo a ±35°: **0,254409 mm**. Un bilancio conservativo deve rispettare
`errore_laterale_radiale + tan(35°) × arretramento_positivo ≤ 0,254409 mm`.
Si tratta del margine disponibile da assegnare a stampa, scheda, package,
posizionamento e deformazioni. Non è una tolleranza misurata o già qualificata.

## Prima di congelare

1. Realizzare fissaggio dell'isola, percorso del collegamento e scarico della
   trazione senza interferenze con DML e telaio; verificare il montaggio reale.
2. Aggiornare il circuito nativo per la separazione fisica, progettare le due
   parti PCB/FPC, verificare orientamento, alimentazione, ERC/DRC e bus.
3. Progettare baffle scuro e tenuta rispetto alle sorgenti interne. Nessuna
   proprietà di opacità viene attribuita automaticamente all'ASA.
4. Assegnare il bilancio di tolleranze usando capacità produttive documentate;
   verificare rigidezza dei legamenti e il tessuto installato/deformato.
5. Eseguire il coupon ottico e le prove P15 con tessuto e stampa finali;
   misurare risposta angolare, luce parassita e calibrazione spettrale/lux.

Non sono ancora chiusi la camera passiva SHT45, la termica del prodotto, il
telaio strutturale o il rilascio dell'intero frontale.

Riproduzione: `generate_front_carrier_rev_b_4mm.py` ricostruisce il carrier
originale in una cartella di lavoro; `generate_optical_perimeter_candidate_rev_fa.py`
riceve quel file, il telaio EU.11 e la shell EQ e genera evidenze e candidati.
I file `evidence/rev-fa/execution.json` e `stl-check.json` contengono numeri,
hash, limiti e risultati. L'immagine `optical-layout.png` ne illustra la sezione.
