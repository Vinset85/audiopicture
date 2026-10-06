# Coupon ottico Rev.FA — supplemento P15

**Stato: preparato, NON ESEGUITO.** Non richiede un assemblaggio AudioPicture
completo. Serve a verificare geometria e risposta del candidato prima del
rilascio della scheda e del frontale. Non misura la resistenza dell'intero ring.

## Materiale da preparare

- Coupon `AP22_OPTICAL_WINDOW_COUPON_REV_FA.step` / `.stl`: 10 × 24 × 1,8 mm,
  apertura 6,6 × 8,4 mm, R1,2. Conservare il riferimento globale del file;
  appoggiarlo sul piano di stampa tramite traslazione, senza modificarne scala
  o forma. Documentare orientamento, lotto ASA, essiccazione e processo.
- Supporto di misura regolabile per il sensore: non ancora un supporto del
  prodotto. Dispositivo OPT3004DNPR con circuito verificato, misurabile anche
  senza tessuto; ingombro e posizione del PCB di studio non sono un PCB pronto.
- Campioni di tessuto e stampa realmente destinati al prodotto, sensore lux
  di riferimento con dati di taratura, sorgente stabile e supporto angolare.
  Registrare identificativi, condizioni ambientali e incertezza strumentale.

## Sequenza e criteri

1. **Controllo dimensionale a freddo.** Misurare finestra, legamenti, spessore,
   deformazione e posizioni. Caricare le dimensioni reali nel modello; verificare
   che non risultino collisioni. Per accettare il passaggio geometrico ±35°,
   la somma degli scostamenti laterali, dell'arretramento moltiplicato per
   tan(35°) e delle rispettive incertezze deve rimanere entro **0,254409 mm**
   rispetto al candidato nominale. Le incertezze non vanno poste uguali a zero.
   Se mancano, risultato OPEN; se il limite è superato, FAIL e ridisegno.
2. **Posizione e smontaggio.** Registrare Z del piano scheda e X/Y del package
   rispetto al coupon. Ripetere la misura dopo i montaggi previsti dal piano
   di prova; registrare ogni montaggio separatamente. Verificare contatti,
   graffi, deformazioni o movimento del sensore. Il coupon non qualifica
   automaticamente lo sgancio inclinato del frontale completo.
3. **Risposta angolare senza tessuto.** Acquisire riferimento e sensore con
   e senza finestra a 0°, ±15°, ±30°, ±35°; esplorare anche ±40°, ±45° e ±57°
   per identificare la schermatura oltre il campo nominale. Ripetere nei due
   piani principali e sulle diagonali, mantenendo costante la posizione del
   centro. Conservare letture grezze, orientamento e stabilità della sorgente.
   La simulazione non predice i lux; nessuna soglia di precisione ottica viene
   inventata per dichiarare PASS prima di definire l'errore richiesto.
4. **Tessuto e stampa.** Ripetere con i campioni finali a più livelli e
   temperature di colore. Separare dati usati per stimare `K_fabric` dai dati
   di verifica. Registrare errore residuo e incertezza; controllare saturazione
   e rumore al buio. La correzione scalare è accettabile solo entro la futura
   specifica quantitativa di accuratezza, ancora OPEN.
5. **Luce interna e baffle.** Con ambiente oscurato, acquisire LED interni
   spenti/accesi e sensore coperto/scoperto. Il baffle e la tenuta reali devono
   essere montati per questa prova. Registrare differenza, rumore, drift e
   incertezza; confrontare con il budget di luce parassita da definire. Non
   attribuire opacità al materiale senza evidenza.
6. **Documentazione.** Salvare immagini del montaggio, dati grezzi, tarature,
   CAD/schema usati e relativi hash. Marcare separatamente PASS/FAIL della
   geometria, stato della calibrazione e stato della ritenzione. P15 resta
   OPEN finché i criteri mancanti e le prove del sensore SHT45 non sono chiusi.

Non stampare l'intero carrier per dedurre da questo solo coupon una qualifica
strutturale, una schermatura della luce interna o la fabbricabilità del prodotto.
