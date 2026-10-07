# AudioPicture — verifiche Rev.FC, 7 ottobre 2026

**Il telaio e il prodotto restano non qualificati per il primo assemblaggio completo.**
Base verificata: `7a61afc609072f81a5ce00683a7f3da2161ec81d`.
Sono stati generati quattro candidati CAD e completate cinque nuove esecuzioni
CalculiX. I fallimenti CAD/mesh/strutturali restano visibili con il loro ambito.

## Risultati effettivi

- **EU.15:** diaframma pieno locale al nodo anti-lift, a partire da EU.14.
  Massa 251,737924 g: FAIL del target 250 g. La prova LC4 da 30 N all'angolo
  inferiore destro dà 1,358603 mm: FAIL del limite 1 mm. Il miglioramento
  rispetto a EU.14 è circa 5,3%; non risolve il problema. LC1/LC3 non eseguiti.
- **EU.16:** nuovi collegamenti profondi tra traverso, appoggi e angoli, attorno
  alla riserva SERVICE; nervature primarie ridotte a 2,4 mm. Massa 251,662101 g.
  CAD eseguito; nessuna mesh o simulazione dichiarata.
- **EU.17:** diagonali del perimetro ridotte da 3,2 a 2,8 mm; massa 248,719422 g.
  Due tentativi di mesh Gmsh, Delaunay e HXT, falliscono. HXT localizza una
  tangenza a (313; 5,6; 22,266) mm. Nessuna FEA su questa geometria.
- **EU.18:** rinforzi diagonali inferiori aumentati fisicamente da 2,8 a 3,2 mm,
  eliminando la tangenza con il traverso. Massa 249,328340 g, margine nominale
  al target 0,672 g per il solo candidato incompleto. La modifica non è un
  offset CAD nascosto e non cambia i vincoli di appoggio.

Tutti e quattro sono un singolo BREP valido con STEP reimportato valido e
22 controlli di sovrapposizione nominale a zero; distanza shell 1,0 mm e carrier
frontale 0,5 mm. Questi ingombri semplificati non qualificano tolleranze e assemblaggio.

Per EU.18 sono realmente completati:

- LC1 lineare, 70 N verticali: spostamento massimo risultante **7,179289 mm**;
  peggiora rispetto a EU.14. È un confronto normalizzato, non la verifica
  dello spostamento degli attacchi, i cui fori sono prescritti fissi.
- LC3 nonlineare, 50 N verso l'esterno: massimo **8,952446 mm**; nessun nodo
  campionato entra nel volume DML. Non è una verifica degli elementi deformati
  continui e il modello non include il contatto con il DML.
- LC4 nonlineare, 30 N all'angolo inferiore destro: **1,389561 mm** con M0 e
  **1,392602 mm** con M1. Entrambe le prove falliscono il criterio da 1 mm.
  La differenza relativa a M1 è **0,218368%**: questa coppia conferma il
  fallimento del criterio di spostamento, senza chiudere la convergenza completa.

Tutte le cinque esecuzioni raggiungono il carico finale e superano il controllo
di equilibrio entro 0,1% del carico o 0,001 N. I risultati di resistenza restano
non qualificati; non sono disponibili limiti ammissibili ortotropi misurati.

## Mesh e condizioni del confronto

M0 EU.18: 164193 nodi e 80066 C3D10; dimensione globale massima 4 mm.
M1: 275055 nodi e 145806 C3D10; dimensione massima 3 mm e ottimizzazione Netgen
prima dell'elevazione quadratica. Entrambe hanno zero Jacobiani non positivi
nel controllo adattivo Gmsh. Restano 101 e 80 elementi con minSICN sotto 0,01;
i minimi sono rispettivamente 0,000454 e 0,001584. Servono raccordi e controllo
dei punti critici prima di una verifica di tensione convergente.

La densità della mesh e l'ottimizzatore cambiano insieme. Cambiano anche i nodi
che campionano carichi e contatti. Sono mantenute le regole geometriche delle
zone di applicazione e la forza totale, non identiche coordinate nodali.
I confronti EU.14/EU.15 e EU.14/EU.18 sono salvati in `evidence/rev-fc/`.
Il postprocessore del traverso stima una traslazione/rotazione di sezione mediante
minimi quadrati: è diagnostica, non una decomposizione dell'energia o una misura fisica.

Materiale di screening: E1=E2=1900 MPa, E3/E1=0,35, G13/G12=G23/G12=0,40,
nu=0,35. Sono ipotesi normalizzate non qualificate. LC3/LC4 hanno geometria
nonlineare, contatti inferiori unilaterali senza attrito con penalità totale
100000 N/mm e vincolo normale ideale dell'anti-lift. EU.18 ha 238 nodi di contatto
in M0 e 320 in M1. Il carico distribuito deriva dal volume del telaio con CG
XY 160/200 mm, non dalle masse reali dell'assemblaggio. LC1 lineare non include
gli appoggi inferiori/anti-lift e non costituisce il modello assemblato finale.

## Massa: il target va valutato insieme alla rigidezza

La revisione [`system-mass-review-rev-fc.md`](system-mass-review-rev-fc.md)
spiega l'origine dei 250 g e l'obsolescenza del budget complessivo da 1,55 kg.
Il target del telaio è un'allocazione progettuale, modificabile dopo revisione
motivata; non un limite del materiale. Non viene aumentato per trasformare
automaticamente un FAIL in PASS. Le future alternative possono essere più
pesanti, purché ne siano documentati benefici strutturali e peso complessivo.

## Gate e lavoro residuo

Registro: **47 PASS / 23 FAIL / 17 OPEN**, comprendente risultati storici e
controlli circoscritti; non è una percentuale di completamento. Nessun candidato
di questa iterazione è accettato per assemblaggio.

Restano lavoro digitale: percorso strutturale e interfacce reali del telaio,
raccordi, distinta di massa e baricentro, matrice LC1–LC7/materiali/CG/contatti/
buckling sulla geometria corrente, pareti/tenute/service/cablaggi, integrazione
ottica e camera SHT45, CFD01–CFD05 del prodotto, schemi MAIN/VOICE/RADAR, tutti
i PCB, BOM e firmware funzionale completo. Le vecchie matrici EU.4 non si
trasferiscono ai nuovi telai. Nessuna nuova CFD o prova fisica è dichiarata.
I coupon e P01–P16 restano preparati, non eseguiti.

CAD, mesh, deck e campi completi sono negli archivi del checkpoint; metriche,
log, sorgenti e hash nel repository. La pubblicazione e la sua verifica sono
registrate separatamente in `docs/validation-checkpoints.md`.
