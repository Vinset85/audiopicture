# Esecuzione delle prove fisiche — Rev.EY

Stato: piano pronto per organizzare le prove; nessuna misura acquisita.
L'elenco autorevole P01–P15 e i criteri numerici disponibili sono nel piano Rev.ER.
I STEP/STL dei coupon geometrici sono candidati da qualificare con il processo scelto.

## Prima di stampare

Identificare stampante e volume utile, lotto PC-CF/ASA, essiccazione, ugello,
altezza strato, temperature, orientamento, pareti, riempimento, supporti e
post-trattamento. Salvare il progetto dello slicer e il file realmente stampato.
Non trasferire automaticamente al pezzo le proprietà del filamento o di un
provino con orientamento diverso. Non ridurre il riempimento del telaio usando
poi i risultati del modello omogeneo pieno.

La geometria completa del prodotto non è autorizzata alla produzione: il
labyrinth ha passaggi nominali da 2 mm e pareti da 1 mm da verificare, mentre
i candidati del telaio non chiudono congiuntamente tutti i gate strutturali e
di produzione.

## Sequenza dei coupon e delle misure

1. **P04–P06, processo e quote.** Stampare i coupon ASA vent/labyrinth e la coppia
   di ritenzione ASA/PC-CF. Per P06 usare almeno cinque esemplari pilota per materiale,
   come previsto da Rev.BB. Registrare quote in più sezioni, difetti, incurvamento
   e supporti rimossi. Non accettare passaggi fusi o ostruiti. Conservare le foto
   orientate sui datum e i valori grezzi con l'incertezza dello strumento.
2. **P01, materiale.** Far definire al laboratorio metodo, geometria dei provini e
   numerosità statistica prima della qualificazione. Misurare trazione,
   compressione, taglio e deformazioni laterali nelle direzioni richieste,
   a 23/50/70 °C. Usare provini dello stesso processo previsto per il telaio.
   Le proprietà a caldo non si ricavano scalando arbitrariamente quelle a 23 °C.
3. **P02–P03, fissaggi.** Selezionare l'inserto esatto e la relativa procedura
   d'installazione. Il foro da 6 mm nei candidati FEM è un'ipotesi geometrica,
   non un foro produttivo. Misurare curva forza-spostamento, estrazione,
   coppia e modalità di rottura su boss/gusset rappresentativi. Riprodurre
   sul coupon M1D il vincolo e i carichi del modello per correlare la rigidezza.
4. **P07–P08, magneti.** Eseguire la matrice 4×2 N45 con gap effettivi
   0,2/0,4/0,6/0,8 mm e target da 0,8/1,0/1,2 mm; almeno cinque assiemi per
   condizione. Misurare successivamente il frontale completo a otto stazioni.
   Il criterio complessivo è 20–30 N; le forze isolate non si sommano come
   prova della ritenzione assemblata. Registrare distacco sequenziale,
   scorrimento, riaggancio e prova a caldo con temperatura da qualificare.
5. **P10, ingombri.** Rilevare componenti montati, piani di riferimento, terminali,
   connettori accoppiati, latch, curvature dei cavi e ferramenta. Aggiornare
   il DMU prima di costruire il prodotto completo. Verificare il gap tessuto-DML
   2,8 mm nominale e almeno 2,0 mm nelle condizioni di tolleranza ammesse.

## Prove sull'assieme qualificato

Eseguire P09 solo con telaio e fissaggi rivisti e proprietà calibrate. Usare
una fixture che separi cleat sinistro/destro, appoggi inferiori e anti-lift.
Acquisire carico e spostamento in modo indipendente. Provare entrambi i guasti
con singolo cleat, i carichi LC1–LC6 e le tre ampiezze di misfit LC7.
I limiti noti sono 0,5 mm al nodo superiore LC1 e 1,0 mm all'angolo LC4;
resistenza e margini richiedono gli ammissibili qualificati. La capacità
dell'ancoraggio nella parete è una prova separata, dipendente dal supporto reale.

Per P11 usare assieme chiuso, cablaggi reali, potenza dissipata tracciabile,
gap parete 3/4/5 mm e ambienti 20/30/35 °C secondo la matrice Rev.EK.
Registrare temperature dell'aria e dei componenti con sonde posizionate e
identificate, oltre a bilancio energetico e portata. Il solo SHT45 non misura
la temperatura interna dei semiconduttori. Conservare l'evoluzione temporale
per verificare l'effettivo raggiungimento del regime.

P12 richiede il pannello DML, i quattro eccitatori e il montaggio reali:
impedenza, risposta, distorsione, perdita fronte-retro e confronto con riferimento
sigillato. P13 confronta Wi-Fi/BLE e radar con orientamenti, parete e disturbi
riproducibili. Definire prima le finestre quantitative ancora OPEN.

P14 include avvio PoE, capacità totale visibile al modulo, transitori di carico,
commutazione tra sorgenti, UV/OV, taratura INA228 e attuazione del governor.
Il test software non verifica questi fenomeni elettrici. P15 registra ogni
unità tramite UUID, inclusi privacy microfono a OFF/reset e recupero ROM.

## Registrazione e rilascio

Usare il modello di registro allegato. Un campo non misurato resta `null` e
il test resta `NOT_RUN` oppure `OPEN`. Allegare dati grezzi, configurazione,
strumenti/calibrazione, incertezza, foto, anomalie e criterio applicato.
Un fallimento richiede correzione e ripetizione dei gate dipendenti; non
sostituire il risultato con un dato di catalogo. Il rilascio richiede prima
chiusura dei gate digitali, poi correlazione e riesecuzione dei modelli con i
dati fisici acquisiti.

## P16 — confronto tra sezioni perimetrali

L'addendum Rev.EY aggiunge ai 15 test originali due coupon reali di sezione
perimetrale PC-CF: sezione a C EU.8 e traliccio EU.9. Le dimensioni nominali
sono 8×84×29 mm, con prese terminali da 3,2 mm e luce nominale 77,6 mm.
Usare lo stesso materiale, processo e orientamento per il confronto.
Misurare massa, quote delle aste, difetti, incurvamento, curve forza-spostamento
e coppia-rotazione. Sottrarre la cedevolezza della fixture misurata separatamente.
Il laboratorio deve stabilire prima carichi, numerosità e soglia di correlazione.
I coupon non dimostrano la capacità del telaio completo e non autorizzano
le geometrie di studio alla produzione. Il registro allegato comprende P16.
