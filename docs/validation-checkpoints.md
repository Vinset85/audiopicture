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


## Supplemento Rev.FE — 9 ottobre 2026

Il [report Rev.FE](../mechanical/digital-validation-rev-fe.md) e il
[registro](../mechanical/validation/rev-fe/gate-register.json) conservano
sensibilità deboli/orientate, nuove pareti ASA, audit del giunto frontale,
inserto originale e provino d'installazione. Il [piano delle misure reali](../manufacturing/real-data-required-rev-fe.md)
separa attività su provini, componenti e primo assemblaggio. Nessun rilascio produttivo.

Estrarre `audiopicture-rev-fe-supplement.zip` dopo FA+FB+FC+FD, nella stessa
cartella. `evidence/rev-fe/raw-artifact-index.json` indica file grezzi, byte
e SHA-256. Rev.FE è [pubblicata](https://github.com/Vinset85/audiopicture/releases/tag/checkpoint-rev-fe-2026-10-09)
il giorno 11 ottobre sul commit `3996b697d6673c8ac19a297206d947c2e36917c9`.
La ricevuta `evidence/rev-fe/github-publication.json` verifica il commit del
tag e tutti e tre gli allegati per nomi, dimensioni e SHA-256 contro i digest
GitHub. L'archivio contiene 396 file: 218 file versionati confrontati con i
blob del commit e 178 artefatti grezzi verificati individualmente. Il confronto
è registrato in `evidence/rev-fe/archive-tree-verification.json`.
Gli indici pre-upload nello ZIP restano immutabili; per lo stato corrente
fa fede la ricevuta in `main`. È una verifica di pubblicazione, non un rilascio
per produzione.


## Supplemento Rev.FG — 14 ottobre 2026

Il [report Rev.FG](../mechanical/digital-validation-rev-fg.md) consolida quattro
esecuzioni strutturali, sedi inserti aggiornate, ganci incassati, guarnizioni
assiali e audit indipendente dello sgancio continuo e dei domini d'aria.
Il telaio corrente fallisce ancora LC4 e non è rilasciato per produzione.
La correzione documentale Rev.FE registra i 57 nodi realmente interferenti
nel caso EU20 LC1 100 N debole Y; gli output storici non cambiano.

Estrarre `audiopicture-rev-fg-supplement.zip` dopo FA+FB+FC+FD+FE.
L'indice `evidence/rev-fg/raw-artifact-index.json` descrive gli artefatti grezzi.
La pubblicazione degli allegati è verificata separatamente dalla validazione
digitale; non si considera completata prima della ricevuta in `main`.

Rev.FG è [pubblicata](https://github.com/Vinset85/audiopicture/releases/tag/checkpoint-rev-fg-2026-10-14)
il 15 ottobre sul commit `d2dbe81e34abad0a0a7c749e5e940226d7e55684`.
Tutti e tre gli allegati sono verificati per nomi, dimensioni e SHA-256 contro
i digest GitHub; il commit del tag coincide. L'archivio contiene 201 file:
115 file corrispondenti ai blob Git e 86 artefatti grezzi verificati uno per uno.
Le ricevute sono `evidence/rev-fg/github-publication.json` e
`evidence/rev-fg/archive-tree-verification.json`. Il confronto si ripete con
`tools/verify_checkpoint_archive.py`, specificando archivio, commit e indice grezzo.

È verificata anche la rettifica della descrizione pubblica Rev.FE: i tre
allegati originari conservano dimensioni e SHA-256 identici. Vedere
`evidence/rev-fg/prior-release-erratum-verification.json`.


## Supplemento Rev.FH — 15 ottobre 2026

Il [report Rev.FH](../mechanical/digital-validation-rev-fh.md) aggiunge tre
esecuzioni complete sul telaio Rev.FG con asse materiale debole Y: i due
angoli inferiori LC4 e la trazione LC3. I controlli geometrici finali passano
negli ambiti esplicitati; non è qualificato l'assemblaggio. Il FAIL debole Z
resta registrato. Due tentativi precedenti interrotti sono separati dai risultati.

Estrarre `audiopicture-rev-fh-supplement.zip` dopo FA+FB+FC+FD+FE+FG.
La pubblicazione è completa solo dopo verifica degli allegati e relativa
ricevuta in `main`. Le successive verifiche saranno eseguite una alla volta
come richiesto dall'utente il 15 ottobre.

Rev.FH è [pubblicata](https://github.com/Vinset85/audiopicture/releases/tag/checkpoint-rev-fh-2026-10-15)
sul commit `0fa19a389e9840527128557908a5cd4ebaa5dc12`. Tutti e tre gli
allegati e il commit del tag sono verificati. Lo ZIP contiene 58 file:
43 corrispondenti ai blob Git e 15 output grezzi verificati individualmente.
Ricevute: `evidence/rev-fh/github-publication.json` e
`evidence/rev-fh/archive-tree-verification.json`. La verifica di integrità
della pubblicazione non costituisce qualificazione del progetto.

## Supplemento Rev.FI — 16 ottobre 2026

Il [report Rev.FI](../mechanical/digital-validation-rev-fi.md) registra una sola
nuova simulazione LC4/LR debole Y sulla mesh più fine del telaio invariato.
Spostamento 0,875290 mm, differenza M0/M1 0,626581%, separazione conservativa
dal DML almeno 0,173090 mm. La convergenza delle tensioni rimane OPEN.
Mesh, audit di qualità, solve e audit degli output sono eseguiti in sequenza.

Estrarre `audiopicture-rev-fi-supplement.zip` dopo FA+FB+FC+FD+FE+FG+FH.
La pubblicazione è completa solo dopo verifica degli allegati e relativa
ricevuta in `main`. Non è un rilascio per produzione.
