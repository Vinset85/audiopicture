# AudioPicture — esecuzioni Rev.FA, 6 ottobre 2026

**Il progetto resta in sviluppo. Non è un rilascio per il primo assemblaggio
completo.** Questa iterazione verifica un percorso ottico alternativo, prepara
il relativo coupon e migliora il telaio. Restano lavoro digitale dell'agente
e prove fisiche; non sono categorie intercambiabili.

Base repository: `19a436701211b5135ecb1b672eae44f177894629`.
I risultati effettivi sono archiviati. Questo checkpoint è preparato per la
pubblicazione su GitHub su richiesta esplicita dell'utente; l'esito del
trasferimento è registrato separatamente, senza anticiparlo qui.

## Sensore di luce sul bordo

Il nuovo candidato riserva una piccola isola ottica fissa fuori dalla
proiezione DML, dietro un'apertura nel supporto frontale removibile. Il DML
rimane integro. Non viene trasferito sul frontale mobile il cablaggio ENV.

CAD eseguito: carrier e coupon ciascuno validi e costituiti da un solido;
STEP reimportati con volume coincidente, STL chiusi e con facce orientate
coerentemente. Verificate le interferenze con telaio EU.11, shell EQ, DML,
maschere radio, target magnetici e riserva della futura parete destra.
EU.12 è controllato separatamente contro il carrier modificato.

L'apertura **6,6 × 8,4 mm** lascia libero un cono di almeno **±35°** da ogni
punto della proiezione massima del sensore. Prova geometrica continua e
**1.953 raggi campionati liberi**, con ulteriori intersezioni OCC di controllo.
Il margine residuo è **0,254409 mm**; va ripartito tra errori reali di posizione
e profondità. Non è una tolleranza produttiva già misurata.

Sono preparati STEP/STL del coupon e istruzioni di misura. Fissaggio, collegamento
fisico, separazione dei PCB, baffle, calibrazione attraverso il tessuto e camera
SHT45 restano OPEN. Nessuna radiometria o misura di lux viene dichiarata.
Dettagli in `optical-perimeter-candidate-rev-fa.md`; prova fisica in
`../manufacturing/optical-coupon-rev-fa.md`.

## Telaio EU.12

Le nervature interne diventano più larghe e meno profonde, mantenendo la stessa
area nominale di sezione: 6,4 × 2,8 mm al posto di 2,8 × 6,4. Il materiale del
traverso inferiore è spostato verso le flange; un labbro anteriore rimane
fuori dal DML, con scarichi alle stazioni magnetiche. Nessuna proprietà
materiale o condizione di vincolo viene migliorata artificialmente.

Geometria effettiva: **201709,547146 mm³**, un solido valido, STEP reimportato
valido. Massa omogenea **246,085648 g**, calcolata con densità di catalogo
1,22 g/cm³. Zero sovrapposizioni nei **22 controlli**; distanza minima shell
**1,0 mm**, carrier frontale **0,5 mm**. Il margine a 250 g non comprende
inserti, raccordi, portacomponenti e interfacce ancora da completare.

Nuova mesh Gmsh: **154289 nodi, 74440 tetraedri quadratici**, minSICN positiva
0,008010. Il suo hash di geometria coincide con lo STEP corrente.

- **LC1:** 70 N verticali, spostamento massimo **1,337438 mm**, rispetto a
  7,126802 mm di EU.11. Le nervature più larghe migliorano la flessione nel
  piano. È esecuzione/diagnostica: il vincolo rigido dei fori non permette di
  certificare lo spostamento reale degli attacchi, né un margine di resistenza.
- **LC4:** 30 N all'angolo inferiore destro, geometria nonlineare e 202 contatti
  unilaterali. Spostamento normale **1,455950 mm**, rispetto a 1,544203 mm di
  EU.11: **FAIL** del limite 1 mm. La prova non identifica ancora l'angolo
  peggiore tra tutti quelli del prodotto.
- **LC3:** 50 N verso l'esterno, nonlineare con contatti. Il modello predice
  **20,933640 mm** massimi: il controllo delle coordinate deformate trova
  **2669 nodi nel volume DML**, prima tutti esterni, e 3770 ulteriori nodi
  avanzati oltre il suo piano anteriore. **FAIL di compatibilità deformata.**
  Il DML non è incluso come contatto in questa FEA: la risposta successiva
  all'urto non è fisicamente simulata. Il risultato identifica perdita di
  rigidezza fuori piano e rende EU.12 inadatto all'assemblaggio; il miglioramento
  in LC1 non lo compensa. Non si deducono danno reale o carico d'inizio contatto.

Tutte e tre le esecuzioni terminano e superano il controllo di equilibrio. La legge
ortotropa normalizzata, le interfacce e la penalità di contatto sono ipotesi
di screening. Il bilancio forze LC4 ha residuo massimo circa 0,0000015 N.
Non sono eseguiti sulla revisione EU.12 l'intera matrice LC1–LC7, le tre mesh,
le sensitività complete o il buckling; quelli di EU.4 non vengono trasferiti.
Non è qualificato il campo di tensione presso raccordi e contatti incompleti.

## Stato delle altre verifiche

Le evidenze Rev.EZ restano valide nel loro ambito: schema ENV con ERC e
netlist verificati, firmware diagnostico ESP32-S3 compilato, tre suite C e
32 test Home Assistant. Nessun codice firmware o Home Assistant è cambiato
in questa iterazione meccanica; non si dichiara una nuova esecuzione dei test.

Il labyrinth EQ tratta geometricamente 22/22 aperture e blocca i raggi del
controllo documentato. Questo non certifica portata, attenuazione o tutte le
aperture di un involucro ancora incompleto. **Le CFD01–CFD05 del prodotto
completo restano NON ESEGUITE.** La parete laterale completa e la tenuta del
frontale non sono state create dal semplice ingombro di parete usato per
controllare il sensore ottico.

La distinta rimane parziale: 76 righe, 27 attive non completamente ordinabili
e 5 opzionali/rimosse. Il nuovo collegamento ottico dovrà essere aggiunto
quando progettato; non si inventano connettore, FPC, costo o quantità finali.
P01–P16 e il nuovo supplemento ottico sono preparati ma **non eseguiti**.

## Lavoro ancora a carico dell'agente

1. Risolvere rigidezza e interfacce reali del telaio; completare raccordi,
   portacomponenti e fissaggi, poi ripetere la matrice strutturale corrente.
2. Integrare ritenzione ottica, collegamento, baffle e camera SHT45; completare
   pareti, tenute, aperture di servizio e cablaggi dell'involucro.
3. Eseguire le CFD coniugate del prodotto con gravità, proprietà documentate,
   radiazione, aperture reali, distanze dal muro e controlli di convergenza.
4. Completare schemi MAIN/VOICE/RADAR, tutti i PCB e relativa verifica
   elettrica/meccanica; derivare una BOM interamente ordinabile dagli schemi.
5. Completare funzioni audio, voce/privacy, radar, commissioning, aggiornamenti
   e controllo di potenza integrato; verificare acustica e radio nei loro ambiti.
6. Integrare i dati fisici dei coupon, ripetere i gate dipendenti e congelare
   il pacchetto di produzione soltanto dopo risultati conformi.

Le proprietà qualificate, la ritenzione magnetica, gli inserti e le calibrazioni
richiedono misure. La loro assenza non implica che il lavoro digitale sia finito.
Il registro contiene **31 PASS, 14 FAIL e 15 OPEN** con ambito esplicito, inclusi
risultati storici; il conteggio non rappresenta una percentuale di completamento.
