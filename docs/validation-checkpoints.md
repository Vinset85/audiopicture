# Checkpoint digitali e sincronizzazione GitHub

Richiesta dell'utente, 6 ottobre 2026: mantenere il repository aggiornato con
il lavoro e i risultati verificati, senza attendere che il prodotto sia pronto.

Ogni checkpoint consolidato pubblica sorgenti, documentazione, registro
PASS/FAIL/OPEN, metriche, log dei solver e provenienza. I risultati falliti
restano disponibili con il loro ambito; non vengono riscritti come PASS.
Le modifiche che invalidano i risultati precedenti richiedono nuove esecuzioni.
Non si presenta la riuscita del solver come accettazione del progetto.

Gli output generati più voluminosi (mesh, campi FEM/CFD, deck completi e CAD)
sono conservati negli allegati della release del checkpoint. Il repository
mantiene `evidence/raw-artifact-index.json` con percorsi, dimensioni e SHA-256.
La copia locale completa conserva anche i file esclusi dalla normale storia
Git; non vengono cancellati durante la pubblicazione.

Checkpoint corrente: **Rev.FA, 2026-10-06**, tag previsto
`checkpoint-rev-fa-2026-10-06`. È una prerelease di validazione digitale,
non un rilascio per produzione. Una pubblicazione è completata soltanto dopo
aver verificato il commit remoto e la presenza/integrità dei relativi allegati.

Per leggere lo stato:

- `mechanical/digital-validation-rev-fa.md`: risultati e lavoro residuo;
- `mechanical/validation/rev-fa/gate-register.json`: gate con ambito/evidenze;
- `evidence/`: misure numeriche e log effettivi, senza qualifiche implicite;
- `manufacturing/optical-coupon-rev-fa.md`: nuova prova preparata, NON ESEGUITA.

Le grandi evidenze vengono suddivise in archivi ZIP indipendenti, ciascuno
con percorsi relativi alla stessa radice `audiopicture/`. Estrarre tutte le
parti nella stessa cartella per ricostruire il checkpoint completo. Verificare
gli hash degli archivi e dei file prima di ricalcolare o utilizzare i risultati.
Le parti hanno un limite conservativo di dimensione inferiore ai 2 GiB
ammessi per ogni [allegato di release GitHub](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).

Sono sempre distinte le categorie calcolato, simulato, dato di catalogo,
ipotesi e da misurare. Le prove fisiche mancanti non vengono dichiarate concluse,
e la loro assenza non implica che tutto il lavoro digitale sia terminato.
