# Dati reali necessari per arrivare alla produzione — Rev.FE, 9 ottobre 2026

**Il progetto non è ancora pronto per produzione.** Servono sia attività
digitali ancora da completare, sia dati fisici che non si possono ricavare
dal CAD. Non occorre costruire subito l'intero prodotto: i primi dati arrivano
da provini stampati, componenti acquistati e piccoli montaggi di prova.

Questo elenco deriva dai contratti del repository. Le soglie già definite
sono riportate; quelle ancora aperte non sono sostituite con valori inventati.
Una simulazione, un valore di catalogo e una misura hanno evidenze distinte.

## 1. Da ottenere prima di congelare telaio e fissaggi

### Processo di stampa realmente utilizzabile

Occorrono produttore e codice esatto di PC-CF e ASA, lotto, essiccazione,
stampante e volume utile, ugello, altezza strato, temperature, velocità,
orientamento, percorsi, numero di pareti, riempimento e post-trattamenti.
Conservare il profilo dello slicer e il file di produzione usato per i provini.
Il telaio con direzione debole Y richiede circa 400 mm di altezza di stampa,
oltre agli accessori; la disponibilità di quel processo è ancora da verificare.

**Serve per:** rendere ripetibili proprietà, deformazioni e tolleranze.
Un provino con un processo diverso dal pezzo non qualifica il pezzo. I modelli
attuali omogenei non dimostrano le prestazioni di un riempimento alleggerito.

### Proprietà del PC-CF stampato — P01

Un laboratorio deve fornire, a **23, 50 e 70 °C** e negli assi della stampa:

- tre moduli elastici E1/E2/E3 e tre moduli di taglio G12/G13/G23, in MPa;
- tre coefficienti di Poisson indipendenti, con reciprocità e matrice elastica
  fisicamente ammissibile;
- curve tensione/deformazione e resistenze direzionali a trazione,
  compressione e taglio, con modo di rottura e deformazione a rottura;
- massa/dimensioni dei provini, densità effettiva, dispersione e incertezza.

Per il carico permanente a parete occorre inoltre definire la durata di vita
richiesta e verificare deformazione nel tempo alle temperature d'impiego.
Il protocollo e il limite di deformazione permanente restano da chiudere.
Le numerosità e gli ammissibili statistici vanno stabiliti con il laboratorio
prima della qualificazione: una singola prova non basta.

**Serve per:** resistenza, rigidezza, instabilità e prestazioni a caldo.
Il valore 1900 MPa oggi nei modelli è un'ipotesi di confronto; i 18 test numerici
degli assi non lo trasformano in un dato misurato. Neppure un modulo di catalogo
costituisce una scheda ortotropa completa del processo scelto.

### Inserti, viti, cleat e parete — P02/P09/P10

Occorrono codici e disegni esatti di inserti, viti, rondelle e dei due cleat;
dimensioni reali del pacco montato, profondità di avvitamento, giochi e
materiali. Se il produttore fornisce disegni/STEP completi, non serve ridisegnarli
da fotografie. La geometria finale dei cleat resta attività di progetto.

Sul nodo stampato rappresentativo misurare:

- diametro/ovalità/profondità del foro, spessore del fondo, boss e raccordi;
- procedura d'installazione dell'inserto: temperatura, tempo, forza se
  misurabile, profondità finale, inclinazione, cricche e deformazioni;
- coppia di serraggio e di cedimento, estrazione/taglio, curve forza-spostamento,
  rigidezza del giunto, modo di rottura e comportamento a caldo;
- cedevolezza del cleat e degli appoggi/anti-sollevamento realmente montati,
  separando quella della fixture di prova.

Il [provino M4 Rev.FE](../mechanical/test/insert-installation-pilot-rev-fe.md)
è pronto come file per una prova d'installazione del candidato ruthex RX-M4x8.1:
foro nominale Ø5,6 × 9,1 mm. Non è ancora un nodo strutturale qualificato.
I fori provvisori Ø6 × 7 mm del telaio non sono compatibili con questa specifica.

**Criteri già fissati:** spostamento attacchi LC1 ≤0,5 mm; deformazione normale
angolo LC4 ≤1 mm; margine 2,0 in LC1 e 1,5 in LC2/LC3/LC4/LC6. Le capacità
assolute di estrazione e la coppia ammessa dipendono dal giunto e dai carichi
effettivi: sono ancora aperte. Servono anche tipo di parete e tasselli scelti;
la portata del telaio non certifica qualsiasi muro.

## 2. Da ottenere prima di congelare frontale e scocca

### Magneti e bersagli metallici — P07/P08

Usare il magnete effettivamente previsto, **Ø4 × 2 mm N45**, con codice,
rivestimento, direzione di magnetizzazione e bersaglio reali. Misurare forza
di distacco normale e scorrimento con gap effettivi **0,2/0,4/0,6/0,8 mm** e
bersagli di spessore **0,8/1,0/1,2 mm**. Il piano esistente prevede almeno
cinque montaggi per condizione; registrare tutti i valori, non solo la media.

**Criteri già fissati:** media nominale 2,8–3,5 N per stazione, nessuna
stazione nominale a temperatura ambiente sotto 2,5 N, e misura indipendente
di **20–30 N sull'intero frontale a otto stazioni**. Verificare sgancio
progressivo, riassemblaggio e comportamento a caldo con tessuto, adesivi e
guarnizioni reali. La variante a dieci stazioni richiede una nuova prova
dell'insieme; non basta sommare i valori di catalogo.

### Geometria stampata e componenti montati — P04/P05/P06/P10

Misurare ritiro, planarità e deformazione di ASA e PC-CF, posizioni dei datum,
fori, sedi magnetiche, spessori e canali del labyrinth. Verificare passaggi
aperti, cedimento dei ponti di stampa, residui e rimovibilità dei supporti.

Servono ingombri montati dei quattro DAEX25FHE-4, morsetti e adesivi; schede,
moduli, connettori con spine inserite, linguette e curve dei cavi; posizione
effettiva del DML e del tessuto. Rilevare anche spessori del DML, massa e
comportamento del suo fissaggio. Gli ingombri semplificati non bastano per
produrre pezzi che si assemblano senza interferenze.

**Criteri già fissati:** ingombro 320 × 400 × 40 mm, nessun intaglio DML per
alloggiare magneti, gap tessuto-DML nominale 2,8 mm e minimo 2,0 mm, rispetto
dei keep-out RF. Le tolleranze produttive devono risultare dalle misure del
processo e dalla catena di tolleranze, non dal numero di decimali del CAD.

### Tenute e percorsi d'aria — nuovo P17

Il candidato attuale lascia percorsi non trattati al giunto frontale anche
se le 22 aperture posteriori hanno il loro labyrinth. Prima va completata
la geometria delle tenute. Poi servono spessore e curva forza-compressione
del materiale scelto, forza di chiusura, stabilità dopo riassemblaggio/cicli
termici, curva pressione-portata delle perdite e posizione delle fughe.

**Serve per:** mantenere la ritenzione 20–30 N, il distacco manuale e il gap
minimo, evitare passaggi involontari e rendere credibili CFD e acustica.
Le soglie di perdita, compressione e durata vanno definite sul progetto finale;
non esiste ancora una guarnizione qualificata. I vent previsti devono restare aperti.

## 3. Dati da schede e piccoli banchi di prova

### Potenza dissipata e proprietà termiche — P11/P14

Misurare potenza assorbita e resa nei diversi stati di funzionamento: riposo,
audio, rete/PoE, voce, radar, sensori e combinazioni peggiori. Separare le
perdite di alimentatore PoE, convertitori, amplificatore e induttori. Conservare
andamenti temporali, tensioni, correnti e condizioni del carico audio reale.

Per i materiali impiegati servono densità, conduzione termica direzionale
quando rilevante, emissività delle superfici effettive e resistenze di contatto
dei percorsi di calore; il calore specifico serve alle analisi transitorie.
Accetto dati di fornitore pertinenti al materiale/processo o misure tracciabili;
parametri incerti restano ipotesi con intervalli, senza un PASS termico definitivo.

**Serve per:** distribuire correttamente i 3/5/8/10 W della matrice termica.
La potenza elettrica in ingresso non coincide tutta con calore locale, né la
potenza audio nominale con la perdita dell'amplificatore. Il limite continuo
applicativo PoE già fissato è **22,5 W**; transitori e protezioni vanno misurati.

### SHT45, luce e tessuto — P15 e supplemento ottico Rev.FA

Occorrono campioni reali di tessuto/stampa, trasmissione e risposta angolare
con OPT3004, letture di riferimento tarate, rumore al buio e luce parassita
dei LED interni. Per SHT45 misurare scostamento e tempo di risposta con la
camera reale, a prodotto freddo e caldo. Queste misure chiudono calibrazione
e isolamento dall'aria interna riscaldata.

Il [piano ottico](optical-coupon-rev-fa.md) contiene sequenza e limite
geometrico del candidato; accuratezza lux e budget di luce parassita richiedono
ancora una specifica quantitativa. Il prototipo del sensore può precedere
il frontale completo.

## 4. Sul primo assemblaggio di verifica, prima della produzione

- **Massa e baricentro completi:** pesare componenti e assieme, misurare il
  baricentro nei tre assi e aggiornare i carichi. Nessun limite di 250 g.
  La regola provvisoria è max(70 N, 4 × massa in kg × 9,80665); non sostituisce
  la verifica finale di fissaggi, distribuzione dei carichi e parete.
- **Meccanica:** prove LC1–LC7 con fissaggi reali, deformazioni, eventuale
  assestamento permanente, sgancio, contatti e ripetibilità. Il materiale e
  il nodo devono essere qualificati prima di interpretare i margini.
- **Termica/aria:** temperature e potenze con 3/5/8/10 W, ambienti
  20/30/35 °C e distanza dalla parete 3/4/5 mm; temperatura dei componenti,
  aria, parete, portata/perdite e zone stagnanti. Confrontare con CFD01–CFD05,
  bilancio energetico e limiti dei componenti esatti. SHT45 non misura le
  temperature di giunzione dell'elettronica.
- **Acustica:** impedenza dei due exciter in serie per canale montati sul DML,
  risposta in frequenza, distorsione, escursione, vibrazioni/rumori, fuga
  posteriore, microfoni e cancellazione dell'eco. La LOS chiusa non prova
  attenuazione. Banda, livello audio e soglie di distorsione/fuga richiesti
  devono essere fissati prima dell'accettazione.
- **Radio/radar:** portata e throughput Wi-Fi/BLE, orientamento/distanza
  dalla parete, presenza/range/zone cieche e falsi allarmi del radar, effetto
  di PC-CF e metalli distribuiti. I limiti funzionali e il riferimento di
  confronto vanno definiti; il solo rispetto geometrico dei keep-out non
  dimostra le prestazioni radio.
- **Elettronica e firmware:** avvio, cambi di alimentazione, stabilità
  Ag53024 con capacità reali, transitori delle rail, calibrazione corrente,
  derating, audio/voce/radar, privacy hardware, aggiornamento e recupero ROM,
  integrazione Home Assistant. Registrare esito per ogni unità, versione e UUID.

Prima di una serie servono anche ripetibilità tra esemplari, resa del processo,
controlli di fabbrica e verifica dei requisiti applicabili al prodotto e al
mercato di destinazione. Non viene dichiarata una certificazione da questi test.

## Come consegnare le misure

Per ogni prova: identificativo provino/unità, codice e lotto dei componenti,
CAD/versione firmware, processo/orientamento, temperatura/umidità, strumento
e taratura, incertezza, valori grezzi con unità, fotografie del montaggio e
modo di rottura quando applicabile. Conservare curve complete e singole
ripetizioni; fotografie o soli valori medi non sostituiscono i dati.

Un produttore di stampa può raccogliere processo e metrologia; un laboratorio
meccanico materiale e giunti; un banco elettronico/acustico le misure funzionali.
Non occorre che l'utente esegua personalmente tutte queste prove.

È disponibile un [registro vuoto per P01–P17](../mechanical/test/measurement-record-template-rev-fe.json),
da copiare per provino o unità. Nessuna misura o accettazione è precompilata;
il confronto P16 su vecchie sezioni resta applicabile solo se rappresentativo
della geometria finale. Il supplemento ottico mantiene il collegamento a P15.

## Lavoro digitale ancora a mio carico

Integrare boss/inserti/cleat e tenute reali, completare CAD/assemblaggio e
catene di tolleranze, rieseguire la matrice FEM sulla geometria definitiva con
materiali misurati, completare CFD del prodotto, schemi/PCB/BOM e firmware
funzionale, preparare file produttivi e collaudo tracciabile. Posso proseguire
le parti non dipendenti dalle misure; non posso dichiarare validate proprietà
fisiche mancanti o sostituire i test dell'assemblaggio con i modelli.

Riferimenti: [piano fisico P01–P15](../mechanical/test/physical-qualification-rev-er.json),
[P16](../mechanical/test/physical-qualification-addendum-rev-ey.json),
[aggiornamenti Rev.FE e P17](../mechanical/test/physical-qualification-addendum-rev-fe.json),
[contratto strutturale](../mechanical/rear-frame-parametric-fea-rev-b.md),
[contratto CFD](../mechanical/cfd/passive-convection-solver-manifest-rev-ek.json).
