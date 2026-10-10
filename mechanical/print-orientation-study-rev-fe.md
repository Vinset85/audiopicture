# Studio degli assi di stampa — Rev.FE

Stato: implementazione degli assi verificata numericamente; orientamento di
produzione e proprietà stampate **OPEN**. I risultati effettivi del telaio sono
nel registro Rev.FE e nei relativi `execution.json`/`metrics.json`.

I candidati precedenti usavano il piano XY del prodotto come piano degli strati:
la direzione debole locale 3 coincideva con Z. Rev.FE rende esplicite tre basi
ortogonali destrorse, mantenendo i medesimi valori dei nove parametri elastici.

- Debole Z: locale 1 = X, locale 2 = Y, locale 3 = Z; strati nel piano XY.
- Debole X: locale 1 = Y, locale 2 = Z, locale 3 = X; strati nel piano YZ.
- Debole Y: locale 1 = X, locale 2 = −Z, locale 3 = Y; strati nel piano XZ.

L'ultima è una sensibilità aggiuntiva sul bordo corto. Non sostituisce la
verifica del bordo lungo né l'eventuale telaio segmentato previste da Rev.B.
Lo spessore degli strati, la direzione dei percorsi all'interno del piano e
le proprietà a caldo non vengono dedotti dall'orientamento del modello.

Il runner usa `*ORIENTATION` e il riferimento nella `*SOLID SECTION`, secondo
il [manuale CalculiX, orientamento](https://www.feacluster.com/CalculiX/ccx_2.18/doc/ccx/node311.html)
e la [definizione della sezione solida](https://www.feacluster.com/CalculiX/ccx_2.18/doc/ccx/node326.html).
È stato verificato anche il parser nel sorgente locale del solver 2.23.
Il controllo indipendente esegue **18 casi su cubo C3D8**: tre trazioni e tre
tagli per ciascuna delle tre basi. Confronta le deformazioni calcolate dal
solver con la soluzione analitica a tensione uniforme; non impone al cubo
le deformazioni attese. Errore relativo massimo: circa **2,593×10⁻⁷**.

Per ogni confronto LC4 il controllo dei deck elimina soltanto la carta di
orientamento e il suo riferimento: il resto del file deve risultare identico
byte per byte. In questo modo non si introducono nuovi vincoli, carichi,
rigidezze o geometrie durante il confronto.

## Qualificazione fisica necessaria

Prima di scegliere una stampa sul bordo occorre verificare volume utile,
stabilità durante la stampa, supporti, deformazione termica e rimozione dei
supporti su pareti, fori e zone RF. L'orientamento con asse debole Y richiede
un'altezza di costruzione dell'ordine di 400 mm, oltre agli accessori di processo;
questa capacità della stampante non è stata accertata.

P01 deve usare provini coerenti con materiale, essiccazione, stampante,
orientamento e percorsi effettivi del telaio. P02 deve verificare i boss e la
direzione di apertura tra strati. Vanno poi rieseguite tutte le LC1–LC7,
le sensibilità, la convergenza delle tensioni e gli instabili con i dati
qualificati. Un miglioramento numerico di LC4 non è un'approvazione di stampa
o una qualificazione degli altri carichi.
