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

Baseline pubblicata: **Rev.FA, esecuzioni al 2026-10-06**, tag
[`checkpoint-rev-fa-2026-10-06`](https://github.com/Vinset85/audiopicture/releases/tag/checkpoint-rev-fa-2026-10-06).
Pubblicata il 7 ottobre: dieci allegati verificati per dimensioni e SHA-256
rispetto ai digest GitHub; ricevuta `evidence/rev-fa/github-publication.json`.
È una prerelease di validazione digitale,
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

## Supplemento Rev.FB — 7 ottobre 2026

Il report `mechanical/digital-validation-rev-fb.md` e il registro
`mechanical/validation/rev-fb/gate-register.json` aggiungono le sei prove
LC1/LC3/LC4 di EU.13/EU.14. Nessuna approvazione produttiva è dichiarata.
Il supplemento comprende tutti i nuovi CAD, mesh, deck, campi e log, senza
duplicare la baseline completa. Per ricostruire lo stato estrarre prima le
quattro parti Rev.FA e poi il supplemento Rev.FB nella stessa cartella.

Rev.FB è [pubblicata](https://github.com/Vinset85/audiopicture/releases/tag/checkpoint-rev-fb-2026-10-07)
sul commit `0c082813d117a03b26b0148d60d653d066d61172`: tre allegati con
nomi, dimensioni e SHA-256 verificati. Ricevuta: `evidence/rev-fb/github-publication.json`. `tools/verify_release_assets.py` ripete la verifica con la copia
locale degli allegati e il commit esatto atteso; termina con errore per tag,
nomi, dimensioni, digest mancanti o non coincidenti.

Gli indici dentro gli ZIP fotografano lo stato precedente al caricamento.
Per lo stato corrente della pubblicazione fanno fede le ricevute in `main`;
gli archivi verificati rimangono immutati.

## Supplemento Rev.FC — 7 ottobre 2026

Il report `mechanical/digital-validation-rev-fc.md` consolida i candidati
EU.15–EU.18, cinque nuove esecuzioni e il confronto LC4 su due mesh EU.18.
Il telaio resta non accettato. `mechanical/system-mass-review-rev-fc.md`
spiega l'origine del target 250 g e corregge l'uso del vecchio budget 1,55 kg.
Registro corrente: 47 PASS / 23 FAIL / 17 OPEN, con ambiti espliciti.

Per ricostruire tutti i dati estrarre le quattro parti Rev.FA, il supplemento
Rev.FB e infine `audiopicture-rev-fc-supplement.zip` nella stessa cartella.
L'indice `evidence/rev-fc/raw-artifact-index.json` contiene i nuovi file grezzi.
Rev.FC è [pubblicata](https://github.com/Vinset85/audiopicture/releases/tag/checkpoint-rev-fc-2026-10-07)
sul commit `90b2e86bde759e80ada60c053e32287648f6bb53`. I tre allegati sono
verificati per insieme esatto dei nomi, dimensioni e SHA-256 rispetto ai digest
GitHub. Ricevuta: `evidence/rev-fc/github-publication.json`. Il supplemento
contiene 116 file, inclusi 38 artefatti grezzi verificati individualmente.


## Supplemento Rev.FD — 8 ottobre 2026

Il nuovo [report](../mechanical/digital-validation-rev-fd.md) documenta la
rimozione autorizzata del tetto di massa, due candidati CAD, quattro mesh,
13 esecuzioni e il controllo conservativo dei volumi degli elementi FEM deformati.
EU.20 passa il criterio normalizzato LC4 sui quattro angoli e sulla seconda
mesh LR; non è una qualificazione produttiva. Restano lavoro digitale e prove fisiche.

Estrarre `audiopicture-rev-fd-supplement.zip` dopo FA, FB e FC. L'indice
`evidence/rev-fd/raw-artifact-index.json` elenca i nuovi artefatti grezzi.
Rev.FD è [pubblicata](https://github.com/Vinset85/audiopicture/releases/tag/checkpoint-rev-fd-2026-10-08)
sul commit `26b60bea5645258ce13141e7a85896333513810b`. Tre allegati con
insieme esatto dei nomi, dimensioni e SHA-256 verificati contro i digest GitHub;
anche il commit del tag è verificato. Ricevuta: `evidence/rev-fd/github-publication.json`.
Il supplemento contiene 216 file, inclusi 79 artefatti grezzi verificati individualmente.
Gli indici nell'archivio restano lo snapshot immutabile precedente al caricamento;
per lo stato di pubblicazione fa fede la ricevuta corrente in `main`.
