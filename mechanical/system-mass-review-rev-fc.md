# AudioPicture — revisione del budget di massa, Rev.FC

7 ottobre 2026. **Nessuna massa assemblata o nuovo limite produttivo è rilasciato.**

## Perché 250 g

Il limite riguarda il solo telaio PC-CF, prima di inserti e cleat metallici.
Il budget iniziale `system-mass-cg-budget-rev-a.md` assegnava 220 g nominali,
con intervallo di lavoro 170–280 g, a un prodotto stimato in 1548 g e con
obiettivo complessivo 1700 g. La Rev.B del telaio, sezione 24, ha portato
l'obiettivo strutturale a 250 g. Il contratto FEA lo riprende come criterio
di ottimizzazione. Non è una soglia fisica del PC-CF, del DML o dell'amplificatore.

La stessa Rev.B richiede di riesaminare la topologia prima di accettare un
aumento. Il budget originale dice anche di ottimizzare la massa **dopo** la
FEA anisotropa. Pertanto il target non giustifica un telaio insufficientemente
rigido e non impedisce di simulare candidati più pesanti per confrontarli.
Un candidato sopra 250 g mantiene il FAIL del target corrente finché il
bilancio complessivo e la revisione del requisito non ne giustificano il cambio.

## Il vecchio margine non è quello attuale

Il budget da 1548 g precede i CAD correnti e contiene valori da aggiornare:

- Scocca: vecchia allocazione 150 g. Il solido shell/labyrinth EQ realmente
  generato ha volume 302276,341 mm³. Applicando **soltanto la sensitività ASA
  già usata nel repository**, 1,05–1,10 g/cm³, si ottengono 317,390–332,504 g.
  Non sono pesate né densità qualificate; mancano ancora pareti e dettagli
  dell'involucro. Questo confronto rende obsoleta la vecchia allocazione.
- Eccitatori: il vecchio budget cita EX25FHE2-4, mentre la selezione congelata
  è DAEX25FHE-4. La [scheda Dayton Audio, revisione stampata 2/5/2014](https://www.audiophonics.fr/images2/8713/295-224-dayton-audio-daex25fhe-4-spec-sheet.pdf)
  riporta 110,9 g netti ciascuno, cioè 443,6 g per quattro. È dato di catalogo,
  non massa mobile, peso di spedizione o misura dei componenti acquistati.
- Il carrier frontale FA è molto più leggero della vecchia riserva di sistema,
  ma il solo polimero non può sostituire una voce che include magneti, adesivi
  e accessori. Elettronica, cavi, fissaggi e densità stampate restano incompleti.

Il calcolo ripetibile `cad/review_mass_budget_rev_fc.py` sostituisce **solo**
telaio, scocca ed eccitatori e lascia esplicitamente inalterate tutte le altre
vecchie riserve. Con EU.18 da 249,328 g restituisce 1736,318–1751,432 g.
Questo è uno scenario di riconciliazione, **non una previsione di peso finale**:
alcune riserve possono diminuire, mentre i componenti mancanti aggiungeranno massa.
Non viene quindi dichiarato né un prodotto già fuori peso né un margine libero.

Gli scenari ipotetici di telaio da 275 e 300 g mostrano solo l'effetto aritmetico
sullo stesso budget; non rappresentano geometrie simulate o approvate.
Rispetto a EU.18 aggiungerebbero rispettivamente 25,672 e 50,672 g.

## Decisione di lavoro

Conservare 250 g come riferimento tracciato; dare priorità a percorso dei carichi,
interfacce e rigidezza. Non ridurre nervature solo per ottenere PASS di massa.
Confrontare anche soluzioni oltre target quando hanno una motivazione strutturale,
senza attribuire loro accettazione preventiva. EU.13 da 268,514 g fallisce comunque
la torsione: aggiungere massa senza migliorare il percorso del carico non basta.

Prima di accettare un nuovo target servono una distinta di massa corrente senza
doppi conteggi, CAD dell'involucro completo, densità/processo qualificati, massa e
baricentro dell'assemblaggio e nuove verifiche strutturali. I 70 N restano il carico
verticale minimo di progetto del modello; non sono la portata certificata della parete.

Evidenza numerica e classificazioni: `../evidence/rev-fc/mass-budget-review.json`.
