# AudioPicture V2.2 — Rev.FH, 15 ottobre 2026

**Tre esecuzioni reali completate e verificate sul telaio corrente Rev.FG. Nessun rilascio per produzione.** L'orientamento alternativo con asse debole Y supera i due controlli d'angolo inferiori e la separazione finale dal DML nei tre casi analizzati. Il FAIL con asse debole Z rimane valido; non viene riscritto come PASS.

Baseline Git: `069621b970e5b8b130c754e29dd4dac697ac8674`. La geometria corrente, le sedi inserti, i ganci e la mesh sono invariati rispetto a [Rev.FG](digital-validation-rev-fg.md). Il telaio pesa **468,724 g calcolati** alla densità di catalogo 1,22 g/cm³; il limite di 250 g resta rimosso.

## Esiti eseguiti

- **LC4, angolo inferiore destro, 30 N:** spostamento normale **0,869805 mm**, entro il limite 1 mm. Separazione conservativa dell'intero elemento quadratico dal DML almeno **0,177358 mm** allo stato finale. Residuo massimo delle forze 0,00000955 N.
- **LC4, angolo inferiore sinistro, 30 N:** spostamento normale **0,870653 mm**, entro 1 mm. Separazione conservativa almeno **0,176540 mm**. Residuo massimo delle forze 0,000000863 N.
- **LC3, trazione frontale distribuita 50 N:** spostamento massimo **3,279141 mm**, massimo normale 3,274502 mm. Separazione conservativa dal DML almeno **0,404518 mm**. Residuo massimo delle forze **0,022199 N**, pari allo 0,0444% del carico e inferiore alla tolleranza numerica preesistente dello 0,1% (0,05 N in questo caso). Nessun criterio di resistenza viene dedotto dalla sola separazione.

Tutti e tre i solver terminano senza errori e raggiungono il carico completo. L'audit considera il volume di tutti i **137 215 elementi C3D10**, non soltanto i nodi. Non risultano inviluppi degli elementi sovrapposti al DML o davanti ad esso entro la sua proiezione. La verifica riguarda lo stato finale; non certifica tutti gli stati intermedi o una geometria reale deformata con tolleranze.

Evidenze: [angolo destro](../evidence/rev-fh/M0-LC4-LR-weakY/LC4/metrics.json), [angolo sinistro](../evidence/rev-fh/M0-LC4-LL-weakY/LC4/metrics.json), [trazione](../evidence/rev-fh/M0-LC3-weakY/LC3/metrics.json). Nelle stesse cartelle si trovano log, manifest e audit `quadratic-dml-clearance.json`.

## Significato e limiti

È una sensibilità numerica ortotropa con E1 = E2 = 1900 MPa, E3 = 380 MPa, rapporti di taglio debole 0,25 e asse debole globale Y. Le proprietà rimangono **ipotesi normalizzate**, non misure o resistenze ammissibili del PC-CF stampato. L'orientamento di stampa non è selezionato per produzione; occorre verificarne fattibilità, stabilità e proprietà sul processo effettivo.

Le analisi includono non linearità geometrica, appoggi inferiori unilaterali senza attrito e cattura normale ideale. Le superfici dei fori superiori sono vincolate idealmente: non sono risolti inserti installati, precarico viti, ganci deformabili e contatti reali. Il DML è un ingombro fisso per il controllo geometrico, non un corpo con contatto accoppiato. Il carico distribuito è quello del modello diagnostico, non la distinta completa di masse dell'assemblaggio.

Il controllo verticale Rev.FG a 100 N con lo stesso orientamento conservava almeno 0,823384 mm di separazione dal DML. Con questi nuovi casi si riduce una parte dell'incertezza sul candidato; restano **OPEN** convergenza della geometria corrente, LC1–LC7 completi, tutti gli angoli e baricentri previsti, contatto e giunti reali, buckling, materiali e temperature. I margini di 0,177 mm sono numerici: non assorbono automaticamente le tolleranze di produzione.

La prova Rev.FG LC4 con asse debole Z mantiene il risultato **FAIL: 1,141787 mm e interferenza predetta**. Non si afferma che il telaio passi per qualsiasi orientamento del materiale.

## Continuità delle esecuzioni e ordine successivo

Due tentativi iniziali si sono interrotti al 20% del carico quando la sessione è scomparsa, senza rapporto di completamento. Sono registrati come interrotti, non PASS né fallimenti di convergenza dimostrati. I risultati sopra derivano da nuove esecuzioni complete. Gli output parziali sono conservati separatamente per tracciabilità.

Su richiesta dell'utente del 15 ottobre, **le prossime verifiche si eseguono una alla volta**, completando audit e salvataggio prima di avviare la successiva. Le tre analisi qui registrate erano già terminate quando è stata recepita tale richiesta; i relativi audit sono stati eseguiti in sequenza.

La prossima verifica numerica utile è il confronto LC4 sull'angolo inferiore con una mesh più fine del medesimo telaio e orientamento, senza cambiare contemporaneamente altri parametri. Restano inoltre da progettare fermo DML indipendente, battute regolabili e cattura inferiore reale, prima di qualificare l'assemblaggio. CFD del prodotto, elettronica/PCB, firmware completo e prove fisiche mantengono lo stato dichiarato nel rapporto Rev.FG.

Registro con storia: **101 PASS / 43 FAIL / 24 OPEN**, con ambiti espliciti; non è una percentuale di completamento. [Registro](validation/rev-fh/gate-register.json), [riepilogo](validation/rev-fh/summary.json), [provenienza](../evidence/rev-fh/provenance.json). Il supplemento Rev.FH si estrae dopo FA+FB+FC+FD+FE+FG e conserva input e output grezzi. La pubblicazione non è un'approvazione produttiva.
