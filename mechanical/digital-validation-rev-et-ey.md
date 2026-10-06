# AudioPicture V2.2 — validazione digitale Rev.ET–EY

Data: 1 ottobre 2026. Base `main`: `19a436701211b5135ecb1b672eae44f177894629`.
Questo rapporto estende Rev.EN–ES e distingue i risultati eseguiti dai requisiti
ancora aperti. **Il progetto non è congelato né pronto per la produzione.**
I file CAD sono candidati di studio e coupon. GitHub non viene aggiornato con
un rilascio produttivo mentre persistono questi gate.

## Evidenza e classificazione

Il registro corrente è `mechanical/validation/rev-et-ey/gate-register.json`.
Ogni PASS riguarda solo il controllo indicato; i FAIL di versioni scartate
rimangono nello storico. I nuovi identificatori G01… non rinumerano né
certificano cumulativamente i vecchi gate fino a C1815. Le 999 occorrenze
storiche di stati irrisolti trovate nell'inventario non sono 999 gate indipendenti.

- **Calcolato:** geometria, intersezioni, quote, massa volume×densità e analisi dei dati.
- **Simulato:** output effettivi CalculiX/Elmer, con ipotesi e ambito espliciti.
- **Dato di catalogo:** proprietà/dimensioni attribuite al produttore, non misurate qui.
- **Ipotesi:** materiale normalizzato, contatti e carichi sostitutivi dei modelli.
- **Da misurare:** proprietà stampate, ammissibili, contatti, ritenzione, prestazioni reali.

I file di input, i log, le mesh e gli output grezzi si trovano in `evidence/`.
Gli estratti verificati e i relativi hash sono in `mechanical/validation/`.
Un codice di uscita zero del solver non equivale all'accettazione del progetto.

## Labyrinth, BREP e ingombri

L'export Rev.EM è stato rieseguito: BREP e reimport STEP validi, un solido,
volume 287929,5221706 mm³. La verifica separata della topologia ha confermato
il difetto: solo **4/22 aperture completamente coperte**, copertura areale
53,9616929%, 22/22 raggi assiali aperti. La connettività fluida 22/22 non
dimostrava un trattamento acustico completo. Il collector Rev.EO è stato
scartato per una strozzatura superiore di 5,1 mm² per lato.

Rev.EQ introduce 22 celle parallele a percorso sfalsato. Risultati geometrici:
22/22 aperture coperte e connesse, nessuna richiusura nominale, 0/2574 raggi
campionati aperti e controllo analitico della sezione. Le sezioni minime
aggregate sono 960 mm² inferiori e 900 mm² superiori. Questi numeri non sono
portate, perdite di carico o attenuazione acustica. Le pareti da 1 mm e i
passaggi da 2 mm richiedono coupon di processo. Shell: 302276,3414609 mm³,
un solido valido; export e reimport verificati.

Il fluido Rev.EQ da 3514228,1460351 mm³ è un complemento geometrico con il
telaio semplificato Rev.ES: manca l'ambiente esterno, il wall-gap e l'ostruzione
reale dei componenti/cavi. Non è un dominio CFD completo.

Rev.ES rimuove 1798 mm³ dalla maschera RF conservativa ESP32
X64…119,5 Y318,5…366,5 Z0…40. Nei candidati successivi le intersezioni con i
keep-out elencati sono nulle. Mancano ancora maschere esatte, antenne,
connettori accoppiati e cablaggi; questo controllo non chiude RF o DMU.

L'audit Rev.EX ha inoltre rilevato **36/36 punti campionati sui lati privi
di parete** nel modello shell+frame Rev.EU.4, e il centro dell'apertura service
ancora pieno nella piastra posteriore. Il CAD non descrive quindi un involucro
completo con guarnizione frontale e tutte le aperture funzionali. Il PASS delle
22 aperture di ventilazione non si estende alle aperture mancanti del prodotto.

## Telaio: iterazioni reali e limiti della simulazione

Rev.EU.1–3 hanno evidenziato percorsi troppo flessibili. Rev.EU.4 aggiunge
ritorni perimetrali profondi e traverse cave, ma fallisce: massa omogenea
calcolata **422,223 g** contro 250 g, distanza dalla shell **0,6 mm** contro
1,0 mm, spostamento normale LC4 **1,8207 mm** contro 1,0 mm.

Rev.EU.5 riduce la massa a 318,498 g ma tocca il labyrinth; è scartata.
Rev.EU.6 recupera 1,0 mm di distanza ma pesa 275,334 g; Rev.EU.7 pesa
254,491 g. Rev.EU.8 restringe la flangia anteriore e arriva a **248,756 g**
con 1,0 mm di distanza. Tutte queste masse sono volume CAD×1,22 g/cm³ di
catalogo, non pesate. EU.8 ha circa 1,24 g di margine: inserti, raccordi e
interfacce mancanti possono annullarlo. Non usare un infill ridotto per
giustificare il peso mantenendo la rigidezza del modello omogeneo pieno.

I quattro fori surrogati hanno raggio 3 mm e profondità utile 7 mm, con centri
X37,5/67,5/252,5/282,5 Y375. Lo spostamento da Y366 evita la maschera RF
conservativa ma richiede cleat accoppiati nuovi. Non è una specifica del foro
di installazione dell'inserto. Mancano i raccordi minimi prescritti, le
interfacce esatte, i giochi e le leggi di contatto qualificate.

### Modello FEM eseguito

CalculiX 2.23 con SPOOLES/ARPACK, tetraedri quadratici C3D10 da Gmsh 4.15.2.
Il cubo analitico di verifica ha errore relativo circa 2×10⁻⁸. Il benchmark
GAPUNI separato risolve sia il ramo chiuso sia quello aperto con le rigidezze
matematiche prescritte; non caratterizza un tampone reale.

E1=E2=1900 MPa e ν12=ν13=ν23=0,35 sono **ipotesi**, non una scheda
PC-CF qualificata e non un limite conservativo garantito. MAT-A/B/C usano
E3/E1=0,20/0,35/0,50; G13/G12 e G23/G12=0,25/0,40/0,60. La matrice di
cedevolezza è controllata positiva definita. Nessun ammissibile di resistenza
viene inventato e nessun margine produttivo viene calcolato.

I fori superiori sono rigidamente vincolati come surrogato di inserti/cleat
perfettamente solidali. Il carico di peso è distribuito sul corpo strutturale
con pesi positivi e baricentro XY imposto: non è la distribuzione reale delle
masse assemblate. La cattura normale dell'anti-lift è un'ipotesi aggiuntiva,
da verificare sulla ferramenta. Gli appoggi inferiori sono unilaterali,
senza attrito e con penalità numerica totale, non rigidezze misurate dei pad.

Le prove Rev.EU.4 coprono LC1, LC2 sinistra/destra, LC3, LC4 all'angolo
inferiore destro, LC5, LC6 e LC7 con misfit 0,25/0,50/1,00 mm a un angolo.
Nel modello sostitutivo LC1/LC2 applicano −70 N in Y al corpo, LC3 −50 N in Z
al corpo, LC4 −30 N in Z ai nodi dell'angolo LR, LC5 −100 N in Y al corpo e
LC6 +50 N in Y alla zona anti-lift. Distribuzione e direzione di LC5 non
dimostrano il contatto reale durante l'installazione. Questi sono casi di
screening identificati con i nomi del contratto, non la qualificazione finale
di tutti i carichi/interfacce richiesti.
Per i casi inizialmente non convergenti si conservano log e fallimenti;
il nuovo tentativo usa penalità totale 10000 N/mm e più iterazioni prima
del cutback, senza allentare le tolleranze dei residui. Il caso LC4 viene
ripetuto con 10000 e 100000 N/mm per controllare la sensibilità numerica.
Le reazioni conteggiano solo i gradi di libertà vincolati; per i momenti si
usano coordinate indeformate nei casi lineari e deformate nei non lineari.

La matrice completa LC1 ha **27 combinazioni ortotrope e 4 baricentri aggiuntivi**
eseguiti. La convergenza lineare dello spostamento LC1 su EU.4 usa 82369,
126787 e 194571 elementi: Umax=3,49060 / 3,50764 / 3,51566 mm;
variazione finale 0,22813%. Il picco nodale equivalente grezzo cambia da
4,55048 a 3,20837 a 3,23086 MPa, ma cambia anche posizione. Tetraedri
localmente distorti, spigoli non raccordati e vincoli rigidi impediscono di
chiudere il gate di tensione non singolare. Von Mises non è usato come
criterio di rottura del PC-CF ortotropo.

Il buckling lineare su EU.4/M1 restituisce fattori 46,29288 / 165,4514 /
597,1354 per il carico seme 70 N e i vincoli dichiarati. Non verifica
imperfezioni, instabilità non lineare, scorrimento, estrazione o danno materiale.
Gli spostamenti sui fori vincolati sono zero per costruzione: non dimostrano
il criterio di movimento reale del nodo superiore ≤0,5 mm.

I risultati numerici aggiuntivi e l'esito dell'ultimo candidato sono riportati
nell'appendice generata dagli output effettivi in fondo a questo documento.

## Termica e solver CFD

Elmer è installato e funzionante come alternativa numerica. Il riferimento
ufficiale di radiazione ha errore circa 4,44×10⁻¹⁰. Il caso ufficiale
NaturalConvection converge senza avvisi accoppiati con tre fattori di
rilassamento 0,10/0,20/0,35. È un riferimento con acqua, non AudioPicture.

Il benchmark di cavità differenzialmente riscaldata de Vahl Davis,
Ra=1000 e Pr=0,71, è stato eseguito su griglie 20/40/80. I coefficienti sono
costruiti per rappresentare il problema matematico; **non sono proprietà
dell'aria del prodotto**. Include gravità, velocità/pressione, energia e
Boussinesq con βΔT=0,01. Sulla mesh più fine Nu caldo=1,1176654214 contro
1,118 di riferimento: errore 0,02993%; variazione ultima mesh circa 0,01994%;
sbilancio caldo/freddo circa 0,00000132%. Nessun NaN o avviso di mancata
convergenza accoppiata. Fonte primaria: [de Vahl Davis, 1983](https://doi.org/10.1002/fld.1650030305).

**CFD01–CFD05 del prodotto non sono eseguiti.** Per farlo occorrono prima
chiusura dell'involucro, geometria/ostruzioni globali, distribuzione delle
sorgenti senza doppio conteggio, conduzioni solide e contatti termici,
emissività/radiazione e proprietà documentate. I benchmark separati non
provano la soluzione coniugata completa. Restano wall-gap 3/4/5 mm, sweep
3/5/8/10 W, ambienti 20/30/35 °C, convergenza mesh <5%, bilancio energetico
e volumi stagnanti secondo Rev.EK. Nessun proxy 75/80% è imposto come
condizione al contorno CFD. Non è dichiarata una potenza passiva dissipabile.

## Esito delle ulteriori iterazioni strutturali

EU.9 sostituisce la parete perimetrale con due facce triangolate: massa
230,121 g, ma LC4 resta a 2,888121 mm. EU.10 rinforza la sola traversa
inferiore centrale e ripristina nervature da 2,8 mm: massa 246,511 g,
clearance 1 mm, ma il limite LC4 resta fallito, come quantificato in appendice.
Il risparmio di massa non dimostra fattibilità strutturale.

Una prosecuzione del dimensionamento deve partire da proprietà stampate e
interfacce di fissaggio caratterizzate: cambiare ancora la struttura per
inseguire numeri ottenuti con E=1900 MPa e cleat idealizzati non può produrre
un rilascio verificato. Rimangono anche lavoro CAD e progettazione digitale,
non solo test fisici. I coupon P01/P02/P16 rendono acquisibili gli ingressi
necessari a una scelta strutturale motivata.

## Elettronica, BOM e firmware

Il controllo della distinta conserva 74 righe, di cui 5 opzionali/rimosse.
Due scelte già presenti nei documenti sono ora riportate nel CSV:
Panasonic EEU-FR1V471B per C901 e Coilcraft XAL7050-103MEC per L901–L904.
La corrente di saturazione tipica del Coilcraft è corretta da 12,1 a **7,1 A**;
12,1 è la frequenza di autorisonanza in MHz. Rimangono **26 righe attive senza
MPN ordinabile esatto** e 35 marcatori di verifica, inclusi DNP. Non esiste
una distinta rilasciata agli acquisti. Fonte e condizioni sono nel rapporto
`component-source-verification-rev-ex.md` e nei documenti audio.

Per Ag53024 il datasheet di variante indica Cout minimo/tipico/massimo
180/220/330 µF. La capacità audio da 470 µF richiede verifica della capacità
effettivamente vista dal modulo attraverso la commutazione di alimentazione,
oltre al condensatore locale proposto da 220 µF. È un gate di avvio/stabilità,
non un'instabilità misurata. Il tentativo di scaricare lo STEP TE esatto ha
ricevuto HTTP 403; nessun import di quel file è dichiarato.

Il nucleo portabile del power governor è implementato e testato sul computer:
200000 eventi deterministici, 320 combinazioni di ingressi, guasti e dati
obsoleti/non validi, transizioni, timer wrap, stallo dello scheduler,
configurazioni non valide e fallback limitato. AddressSanitizer,
UndefinedBehaviorSanitizer e il test CMake/CTest passano. Il limite software
PoE è ricondotto a 22,5 W. Le calibrazioni dei test sono fixture, non valori
produttivi; l'implementazione parte con amplificatore disabilitato.

Restano driver e integrazione ESP-IDF/TAS5825M/INA228, DSP e tarature,
privacy hardware, rete/Home Assistant, provisioning/OTA e test sul dispositivo.
Mancano schemi e PCB KiCad nativi con ERC/DRC e geometria assemblata completa.
Il test host non dimostra il limite istantaneo di potenza sull'hardware.

## Ordine obbligato prima della costruzione

1. Chiudere il disegno strutturale e l'involucro, raccordi, interfacce,
   cleat/inserti e cablaggi. Verificare tolleranze, montabilità, RF esatto e
   passaggio di ogni apertura. Non promuovere i STEP di studio a produzione.
2. Eseguire i coupon e acquisire proprietà materiali/contatti; rerun FEM con
   tutti i casi, orientamenti e temperature, mesh locale adeguata, angolo
   peggiore, imperfezioni e ammissibili qualificati.
3. Completare il modello termico coniugato e l'intera matrice Rev.EK. Misurare
   poi la correlazione sul prototipo chiuso.
4. Completare circuito e PCB nativi, distinta ordinabile, power sequencing,
   software di dispositivo e verifiche elettriche/RF/acustiche.
5. Applicare P01–P15 e il confronto perimetrale aggiuntivo P16, registrando risultati grezzi e incertezza. Il piano,
   le istruzioni pratiche Rev.EY e il registro vuoto sono allegati.

Il target di ritenzione assemblata rimane 20–30 N, con 8 stazioni 4×2 N45
baseline e 10 fallback; le forze isolate non lo dimostrano. Il gap tessuto-DML
rimane 2,8 mm nominale e almeno 2,0 mm. Non sono introdotti anelli continui
in acciaio, intagli DML, ventole o una riduzione dell'envelope 320×400×40.

<!-- EXECUTED_RESULTS_APPENDIX -->

## Appendice: risultati eseguiti e verificati

- EU.4 LC1, penalità 100000 N/mm: Umax 3.437285 mm; bilancio forze PASS.
- EU.4 LC3, penalità 100000 N/mm: Umax 5.260544 mm; bilancio forze PASS.
- EU.4 LC4, penalità 100000 N/mm: Umax 1.826235 mm; bilancio forze PASS.
- EU.4 LC5, penalità 100000 N/mm: Umax 4.893749 mm; bilancio forze PASS.
- EU.4 LC7, penalità 100000 N/mm: Umax 0.533928 mm; bilancio forze PASS.
- EU.4 LC2L, nuovo tentativo con penalità 10000 N/mm: Umax 6.414779 mm; bilancio forze PASS.
- EU.4 LC2R, nuovo tentativo con penalità 10000 N/mm: Umax 6.416488 mm; bilancio forze PASS.
- EU.4 LC4, nuovo tentativo con penalità 10000 N/mm: Umax 1.841838 mm; bilancio forze PASS.
- EU.4 LC6, nuovo tentativo con penalità 10000 N/mm: Umax 3.669168 mm; bilancio forze PASS.

LC4 EU.4: cambiando la penalità di dieci volte, lo spostamento all'angolo cambia del 0.8534%. La penetrazione numerica massima passa da 0.004468 a 0.022357 mm. Entrambi i risultati falliscono il limite di 1 mm. La penalità non identifica un pad fisico. Il floor del nuovo tentativo è 10⁻⁷ N per nodo, su 202 nodi.

- LC7 EU.4, misfit 0.25 mm: Umax 0.267017 mm, reazione normale alla deformazione imposta -6.217420 N. Un solo angolo; le altre posizioni restano OPEN.
- LC7 EU.4, misfit 0.50 mm: Umax 0.533928 mm, reazione normale alla deformazione imposta -12.430031 N. Un solo angolo; le altre posizioni restano OPEN.
- LC7 EU.4, misfit 1.00 mm: Umax 1.067434 mm, reazione normale alla deformazione imposta -24.840947 N. Un solo angolo; le altre posizioni restano OPEN.

### Candidato EU.8

Volume 203898.163407 mm³; massa omogenea calcolata 248.755759 g; distanza dalla shell 1.000000 mm; solidi 1; BREP valido True.

- LC1 (lineare): Umax 8.000665 mm; bilancio forze PASS.
- LC4 (non lineare con contatto): Umax 2.825162 mm; bilancio forze PASS. Angolo LR |UZ|=2.808054 mm, criterio ≤1 mm: FAIL.

Materiali e ferramenta rimangono ipotesi; questi risultati non ereditano la matrice completa e la convergenza mesh della diversa geometria EU.4. I raccordi e il CAD esatto sono ancora da integrare.

### Candidato EU.9

Volume 188623.414972 mm³; massa omogenea calcolata 230.120566 g; distanza dalla shell 1.000000 mm; solidi 1; BREP valido True.

- LC1 (lineare): Umax 8.821495 mm; bilancio forze PASS.
- LC4 (non lineare con contatto): Umax 2.914744 mm; bilancio forze PASS. Angolo LR |UZ|=2.888121 mm, criterio ≤1 mm: FAIL.

Materiali e ferramenta rimangono ipotesi; questi risultati non ereditano la matrice completa e la convergenza mesh della diversa geometria EU.4. I raccordi e il CAD esatto sono ancora da integrare.

### Candidato EU.10

Volume 202058.498378 mm³; massa omogenea calcolata 246.511368 g; distanza dalla shell 1.000000 mm; solidi 1; BREP valido True.

- LC1 (lineare): Umax 6.702117 mm; bilancio forze PASS.
- LC4 (non lineare con contatto): Umax 2.159790 mm; bilancio forze PASS. Angolo LR |UZ|=2.141594 mm, criterio ≤1 mm: FAIL.

Materiali e ferramenta rimangono ipotesi; questi risultati non ereditano la matrice completa e la convergenza mesh della diversa geometria EU.4. I raccordi e il CAD esatto sono ancora da integrare.
