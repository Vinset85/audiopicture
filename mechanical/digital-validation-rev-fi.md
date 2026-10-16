# AudioPicture V2.2 — Rev.FI, 16 ottobre 2026

**Una nuova analisi reale, eseguita in sequenza e verificata: il controllo LC4 sull'angolo inferiore destro passa anche sulla mesh più fine. La convergenza strutturale completa resta OPEN.**

Baseline Git: `f45808a49d7e4ceba46a800b765b528b9fde5046`. CAD invariato Rev.FG, stessa geometria STEP, stesso materiale ortotropo normalizzato con asse debole Y, stesso carico 30 N e stesse definizioni geometriche dei vincoli di Rev.FH. Nessuna selezione produttiva del materiale o dell'orientamento di stampa. Il limite di 250 g resta rimosso; massa del telaio invariata, 468,724 g calcolati alla densità di catalogo.

## Risultati eseguiti

- Mesh M1: dimensione massima 3 mm, **353 555 nodi e 196 622 elementi C3D10**, contro 137 215 elementi M0 a 4 mm. Algoritmo e ottimizzatore invariati. Jacobiani quadratici tutti positivi; minimo 0,0000699219 mm³, qualità minima SICN 0,0147248. La qualità positiva non prova la convergenza.
- CalculiX 2.23: completamento senza errori, carico finale 100%, sette incrementi accettati. Tempo dichiarato dal solver **1153,642 s**. Una sola simulazione attiva, dopo completamento della mesh e del suo audit.
- Spostamento normale dell'angolo: **0,875290 mm**, entro **1 mm**. M0: 0,869805 mm. Differenza **0,626581%** rispetto a M1, inferiore al 5% per questa coppia e questa grandezza.
- Separazione conservativa dal DML allo stato finale: almeno **0,173090 mm**, contro 0,177358 mm in M0. Sono controllati i volumi di tutti i 196 622 elementi quadratici; nessun inviluppo sovrapposto o anteriore al DML entro la sua proiezione. Il limite conservativo non è la distanza minima esatta né una tolleranza produttiva.
- Residuo massimo delle forze: **0,000014895 N**, entro la tolleranza prescritta di 0,03 N. Residuo massimo dei momenti diagnostico: 0,002804 N·mm. Penetrazione numerica massima degli appoggi a penalità: 0,002647 mm; non è una deformazione misurata della guarnizione.

Evidenze: [mesh](../evidence/rev-fi/mesh/M1/mesh-report.json), [qualità](../evidence/rev-fi/mesh/M1/quality-audit.json), [esecuzione](../evidence/rev-fi/M1-LC4-LR-weakY/LC4/execution.json), [metriche](../evidence/rev-fi/M1-LC4-LR-weakY/LC4/metrics.json), [audit di separazione](../evidence/rev-fi/M1-LC4-LR-weakY/LC4/quadratic-dml-clearance.json), [confronto M0/M1](validation/rev-fi/mesh-pair.json).

## Cosa dimostra il confronto

I sette punti caricati e le forze applicate coincidono tra M0 e M1 alla precisione numerica documentata. Baricentro del carico: X312,4 / Y12 / Z35 mm, senza spostamento fra i modelli. Gli appoggi inferiori sono discretizzati con 208 nodi in M0 e 332 in M1, mantenendo la penalità totale 100 000 N/mm. I vincoli superiori restano ideali. Il carico nodale è una rappresentazione diagnostica: l'impronta reale dell'azione non è modellata.

Il picco nodale estrapolato di von Mises passa da **5,4661 a 6,1674 MPa**, una differenza di circa **11,37%** rispetto a M1. È un indicatore diagnostico vicino alla cattura inferiore ideale; non è una tensione ammissibile ortotropa o un indice di cedimento. La classificazione del punto critico e la convergenza delle tensioni non singolari restano OPEN. Il superamento del controllo sullo spostamento non chiude queste verifiche.

Il margine nominale dal DML è piccolo e non assorbe automaticamente tolleranze, deformazione del DML, giunti reali o variazioni delle proprietà. Il precedente FAIL con asse debole Z resta valido. Restano aperti LC1–LC7 completi, casi di baricentro e temperatura, contatti reali, buckling e qualificazione dei materiali e del processo. Le altre discipline mantengono lo stato Rev.FH/FG: nessuna CFD completa del prodotto o produzione qualificata.

## Riproduzione e prosecuzione

Usare `mesh_frame_interfaces_rev_fg.py` sulla geometria corrente con `--size 3 --algorithm3d 1`, poi `audit_frame_mesh_rev_fc.py`. Eseguire `run_frame_screen_rev_fe.py` con LC4/LR, `--ez 0.2 --gx 0.25 --gy 0.25 --weak-axis Y --gap --anti-normal --contact-iterations --execute`. Completare in sequenza il riepilogo Rev.FG, l'audit nodale Rev.FE, l'audit quadratico Rev.FD e `consolidate_mesh_pair_rev_fi.py`. I manifest conservano gli hash di input, mesh, sorgenti e solver; nessun risultato deriva dal solo lancio del comando.

Il prossimo approfondimento strutturale deve trattare la cattura inferiore e il punto critico delle tensioni prima di dichiarare una convergenza completa. Un'ulteriore mesh o altri casi di carico andranno eseguiti singolarmente, dopo il salvataggio di questo checkpoint.

Registro storico: **106 PASS / 43 FAIL / 24 OPEN**, con cinque nuovi controlli circoscritti; non è una percentuale di completamento. [Registro](validation/rev-fi/gate-register.json), [riepilogo](validation/rev-fi/summary.json), [provenienza](../evidence/rev-fi/provenance.json). Il supplemento Rev.FI si estrae dopo FA+FB+FC+FD+FE+FG+FH. La pubblicazione non autorizza la produzione.
