# AudioPicture — esecuzioni Rev.EZ, 5 ottobre 2026

**Il progetto non è congelato e non è pronto per costruire l'assemblaggio completo.**
Questo aggiornamento chiude controlli circoscritti sullo schema sensori e sul
software diagnostico. Conferma problemi strutturali e individua un'interferenza
nel percorso ottico. Restano attività digitali sostanziali a carico dell'agente,
oltre alle prove fisiche già preparate. Non è un rilascio produttivo.

Base locale e GitHub main verificati: `19a436701211b5135ecb1b672eae44f177894629`.
Il lavoro successivo è locale. Nessun aggiornamento GitHub in questo checkpoint.
Le prove precedenti sono documentate in `digital-validation-rev-et-ey.md`;
non sono ripetute o trasferite automaticamente alle nuove geometrie.

## Circuito sensori effettivamente verificato

Creato lo schema ENV nativo KiCad 9.0.8 con automazione validata, ammessa dal
contratto ENV. ERC eseguito: **0 errori, 0 avvisi, 0 esclusioni**. Verifica
indipendente della netlist KiCad: **10 componenti esclusi i simboli di
alimentazione, 4 reti, 26 pin collegati, 3 NC espliciti**. Verificati alimentazioni,
SDA/SCL, ADDR dell'OPT3004 a VDD per 0x45, pad esposto a massa, condensatore
opzionale DNP e assenza di pull-up I2C locali. Apertura nell'editor grafico
riuscita; eseguito il comando Salva e controllata la rappresentazione.

L'impronta OPT3004 è stata generata e riletta con l'API nativa pcbnew:
pad esposto 0,65 x 1,35 mm, apertura pasta 0,62 x 1,25 mm, copertura 88,319%.
Il confronto riguarda il disegno del produttore; maschera, stencil, vias,
assemblaggio e circuito stampato restano da qualificare. Sono selezionati i
codici esatti dei condensatori ENV. Per fonti e riproduzione vedere
`../hardware/kicad/environment/native-validation-rev-ez.md`.

Corretta la precedente indicazione PTFE: il datasheet Sensirion v7.3 specifica
membrana in poliimmide e riporta esplicitamente la correzione nella cronologia.
Il codice ordinabile del sensore è SHT45-AD1F-R2. BOARD_ID rimane riservato e
scollegato; la vecchia frase che lo descriveva già implementato è stata corretta.

## Percorso ottico: FAIL geometrico confermato

L'intera regione ENV X252..294/Y35..59 è dietro la proiezione DML
X10..310/Y10..390. Il DML occupa Z3,3..9,3, mentre il piano frontale della
scheda ENV parte da Z12. Tutte le **25 linee normali controllate** attraversano
**6 mm** del volume DML; l'intersezione del volume di passaggio è **6048 mm³**.
La relazione tra rettangoli dimostra che il problema vale per tutta la regione,
non solo per i punti campionati. Spostare la scheda da Z12 a Z13 non lo risolve.

Va progettato un percorso ottico reale sul perimetro/frontale oppure spostato
il sensore di luce, rispettando DML, radio e frontale removibile. Non è stata
assegnata una trasmittanza al materiale DML: questo è un controllo geometrico,
non una simulazione ottica né una misura di lux. La posizione PCB resta aperta.

## Telaio EU.11: miglioramento parziale, ancora FAIL

Modificato il traverso inferiore e redistribuiti i rinforzi del perimetro.
Un'interferenza iniziale con due supporti della scocca è stata rilevata e
corretta; i risultati iniziali respinti sono conservati separatamente.

Geometria corrente: un solido BREP valido, STEP reimportato valido;
volume **202410,551 mm³**, massa omogenea **246,941 g** usando il dato di
catalogo 1,22 g/cm³, distanza minima dalla scocca EQ **1,000 mm**;
zero sovrapposizioni con i 12 volumi di esclusione e con la scocca verificata.
La massa non comprende inserti, raccordi e interfacce ancora da completare.
Il margine nominale al tetto di 250 g è soltanto circa 3,06 g.

Mesh effettiva: **151260 nodi, 72609 tetraedri quadratici**, qualità minSICN
positiva 0,004986. Risolti con CalculiX LC1 lineare e LC4 nonlineare con contatti
unilaterali; gli equilibri delle forze superano il controllo previsto.

LC4, 30 N all'angolo inferiore destro: spostamento normale **1,544203 mm**, oltre
il limite **1 mm**. EU.10 era a 2,141594 mm. LC1: spostamento massimo
**7,126802 mm** nella zona interna, peggiore dei 6,702117 mm di EU.10.
L'esecuzione riuscita non è accettazione meccanica.

Materiale ortotropo e vincoli rimangono ipotesi di screening; il modulo base
1900 MPa non è presentato come proprietà qualificata. I fori superiori sono
vincolati rigidamente e non consentono di validare lo spostamento reale del
fissaggio. Nessun margine di resistenza o convergenza delle tensioni è dichiarato.
La matrice completa LC1–LC7/materiali/mesh di EU.4 non vale per EU.11.

## Software realmente eseguito

Tre suite C su host con AddressSanitizer/UndefinedBehaviorSanitizer: PASS.
Comprendono 200000 eventi e 320 combinazioni del controllo di potenza,
vettori sensori, 48 corruzioni CRC a singolo bit, errori e timeout del bus,
256 configurazioni di ingresso e 510 configurazioni registro invalide del
TCA9534. Il nuovo espansore è configurato solo come ingresso e controllato
tramite rilettura; non comanda l'amplificatore.

Firmware ESP32-S3 compilato con ESP-IDF 5.5.3: immagine **851936 byte**.
Include identità persistente, Ethernet W5500, Wi-Fi station opzionale,
letture sensori, diagnostica di alimentazione e API locali in sola lettura.
Letture assenti/non valide/scadute sono null; `type2_verified` resta false.
Amplificatore, voce, microfoni e radar rimangono disabilitati. Nessun dispositivo
è stato programmato o provato fisicamente; il controllo di potenza non è
ancora collegato alla catena reale di acquisizione e comando.

Home Assistant: **32 test PASS**, **181/181 istruzioni coperte** con fixture
reali e server HTTP locale. È copertura di righe, non di rami o hardware.
Le prove, eseguite il 1 ottobre e non alterate dalle modifiche successive,
coprono scoperta, identità, recupero, cambi indirizzo, unload e risposte errate.
L'integrazione espone sette sensori diagnostici; non è stata installata sul
Home Assistant dell'utente e non implementa riproduzione audio, voce o radar.

## Distinta e prove fisiche

BOM parziale: **76 righe**, delle quali **27 attive non completamente definite
con codici ordinabili**, più **5 opzionali/rimosse**. Il conteggio precedente
usava un intervallo fisso che includeva una riga vuota e saltava l'ultima
resistenza; inoltre RADAR_FILTERS è una rete, non un singolo componente
completamente definito. Il nuovo audit corregge entrambi i casi. Non si tratta
del conteggio completo dei componenti del prodotto, che richiede gli schemi.

Aggiunti U20 TCA9534PWR e il relativo bypass C20; scelti i condensatori ENV e
il codice di confezionamento SHT45. Restano da definire condizionamenti degli
ingressi, isolamento della classificazione PoE e negoziazione effettiva.
La classificazione hardware grezza non autorizza il budget Type 2 nel software.

P01–P16 restano NON ESEGUITI. Aggiunta una procedura operativa di primo avvio
diagnostico in `../manufacturing/diagnostic-bringup-rev-ez.md`, con controlli
positivi e di guasto, registrazione delle evidenze e criteri senza numeri
inventati. I coupon possono essere preparati secondo le istruzioni; non sono
un assemblaggio completo già approvato.

## Lavoro digitale residuo, in ordine di dipendenza

1. Risolvere la rigidezza del telaio e completare raccordi, fissaggi e contatti
   reali. Eseguire sulla geometria risultante l'intera matrice strutturale.
2. Completare scocca laterale, tenuta DML, aperture service/cablaggi e camera
   ENV; risolvere il percorso ottico e integrare componenti/cablaggi verificati.
3. Costruire il dominio termico coniugato con proprietà documentate, radiazione,
   gravità, aperture reali e distanza dal muro 3/4/5 mm. **CFD01–CFD05 del prodotto
   sono ancora NON ESEGUITI**; i benchmark Elmer riusciti non li sostituiscono.
4. Completare schemi MAIN/VOICE/RADAR, tutti i PCB e la distinta derivata;
   verificare alimentazione, isolamento, capacità/inrush, layout ed ERC/DRC.
5. Completare software audio/DSP, voce/privacy, radar, commissioning,
   aggiornamenti e controllo di potenza integrato; verificare modalità acustiche,
   impedenza montata/LC e radio con dati materiali e hardware appropriati.
6. Integrare le misure dei coupon e del prototipo nei modelli, ripetere i gate
   dipendenti e soltanto allora congelare CAD e file di fabbricazione.

Proprietà qualificate dei materiali, magneti/inserti, calibrazioni e correlazioni
non possono essere sostituite con dichiarazioni digitali. La loro assenza non
significa che tutto il lavoro digitale sia già completato.
