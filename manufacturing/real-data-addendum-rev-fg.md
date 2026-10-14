# Addendum dati reali e prove — Rev.FG, 14 ottobre 2026

Integra [il piano Rev.FE](real-data-required-rev-fe.md) per il candidato con sedi superiori incassate, viti svasate e guarnizioni assiali. **Nessuna prova fisica è stata eseguita.** I dati richiesti risultano non disponibili; le attività sotto sono predisposte per l'esecuzione successiva. Il telaio corrente fallisce ancora LC4, quindi non costituisce un rilascio produttivo.

## P02 — Inserti e stampa PC-CF

Il candidato corrente usa quattro fori nominali Ø5,6 × 9,1 mm per RX-M4x8.1, boss Ø12 mm e fondo 2,5 mm. La vecchia sede numerica Ø6 × 7 mm non è una specifica d'installazione compatibile.

Registrare lotto e condizionamento del filamento, macchina, ugello, orientamento, strati, perimetri, riempimento, temperature e processo di installazione. Misurare fori prima/dopo installazione, posizione dell'asse, profondità, ovalizzazione, fondo e deformazione locale. Rilevare curve forza-spostamento, estrazione, coppia e rilassamento a temperatura; sottrarre o dichiarare la cedevolezza della macchina/attrezzatura. Non assegnare una coppia ammessa o una resistenza del giunto dalla sola geometria di catalogo.

## P09 — Ganci, teste svasate e ancoraggi

Acquisire materiale e certificato dei ganci, quote dei profili, raccordo/smusso, planarità e qualità superficiale. Verificare le sedi svasate e le teste effettive PTS A79910410 M4×10 ISO 10642 A2. La lunghezza di 10 mm include la testa. Confermare ingaggio e assenza di fondo-corsa dell'inserto, poi misurare precarico, pressione di contatto e cedimento delle sedi.

Con testa massima Ø8,96 mm e foro passante Ø4,5 mm, una piastra da 2,5 mm lascia nominalmente circa **0,27 mm** di tratto cilindrico sotto una svasatura a 90°. Questo dato geometrico non qualifica portanza, fatica o serraggio: la sede sottile richiede verifica strutturale dedicata.

Le teste degli ancoraggi a parete devono restare nell'inviluppo svasato modellato, con lato anteriore Z = 40,5 mm. Definire supporto murario, codice tassello/vite, diametro e lunghezza effettivi; verificare estrazione e taglio secondo i carichi di progetto. Qualsiasi testa sporgente diversa richiede ripetere il percorso di sgancio e l'audit delle interferenze. I distanziali alternativi da 0/1/2 mm determinano rispettivamente il distacco 3/4/5 mm e fanno parte dello stack da misurare.

## P10 — Montaggio, cattura e sgancio

Verificare sull'assemblaggio completo l'installazione e il sollevamento di 7 mm prima dell'estrazione frontale, includendo fissaggi inferiori, cablaggi, tolleranze e accessibilità. Registrare gioco, blocco anti-sollevamento, rumori, ripetibilità di montaggio e danni dopo i cicli previsti dal piano. Il PASS del percorso CAD superiore rigido non chiude questa prova.

## P17 — Tenuta, compressione e fermo DML

Identificare esattamente schiuma, densità, codice acquistabile, lotto e adesivo. Rilevare spessore locale, curve di compressione/scarico alle temperature operative, rilassamento e deformazione permanente. Misurare planarità e gap montato lungo l'intero perimetro e presso ogni guarnizione; includere deformazione della shell e spessore adesivo. Eseguire la prova pressione-portata e il controllo di perdita dopo montaggio, temperatura e cicli.

Rondelle assiali superiori: Ø12,4/16,2 mm, spessore nominale libero 1,57 mm e installato 1,256 mm. Non sono O-ring. Per la compressione 10–30%, gli intervalli condizionali di gap sono 1,54…1,62 mm sul DML e 1,2089…1,2717 mm sulle guarnizioni da 1,57 mm. Sono requisiti da garantire mediante stack misurato e regolazione; non tolleranze FDM già ottenute.

La progettazione del fermo DML indipendente, della cattura contro sovracorsa, delle battute regolabili e del metodo di selezione spessori è **lavoro digitale ancora da completare**. Non viene attribuita all'utente e non è sostituita dalle misure. Il frontale magnetico mantiene il proprio obiettivo di ritenzione 20–30 N; non precarica implicitamente tutta la guarnizione DML.

## Criteri e stato

Restano applicabili i criteri originali del contratto strutturale, fra cui spostamento locale LC1 ≤0,5 mm e margine 2, LC4 ≤1 mm e margine 1,5, margine 1,5 per LC2/LC3/LC6, con interpretazione e punti di misura definiti dal contratto. La ritenzione frontale è 20–30 N e il gap tessuto-DML minimo 2 mm. La compressione delle guarnizioni resta 10–30%. Nessun limite di perdita, coppia o proprietà materiale viene inventato in assenza di una specifica qualificata.

Il telaio corrente raggiunge **1,141787 mm** nella sensibilità normalizzata LC4 debole Z: **FAIL**, con interferenza deformata predetta. Una prova fisica non deve essere usata per ignorare questo difetto digitale. Tutte le prove di questo addendum hanno stato **NOT_RUN**; nessun materiale, giunto o prodotto risulta qualificato.
