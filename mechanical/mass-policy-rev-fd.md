# AudioPicture — modifica autorizzata del budget di massa, Rev.FD

7 ottobre 2026. Decisione dell'utente: «superiamo tranquillamente il limite
del budget di massa».

Il target di **250 g per il telaio PC-CF è superato come criterio di esclusione**.
Non si impone un nuovo tetto numerico arbitrario. La massa resta una quantità
da calcolare, misurare e ottimizzare dopo la verifica di rigidezza e resistenza.
Il precedente obiettivo complessivo di 1,70 kg resta un riferimento storico
di pianificazione: non può obbligare a ripristinare indirettamente il tetto
di 250 g autorizzato al superamento. Il peso finale ammissibile sarà riesaminato
insieme a montaggio, movimentazione e carichi effettivi.

Questa decisione prevale sulle clausole di massa di `rear-structural-frame-rev-b.md`
sezione 24, `rear-frame-parametric-fea-rev-b.md` obiettivo/C92 e sui budget
storici Rev.A/Rev.FC. I vecchi risultati restano archiviati rispetto ai requisiti
allora applicati: un precedente FAIL di massa non diventa una simulazione PASS.
I FAIL di rigidezza, interferenza e gli OPEN di resistenza restano applicabili.

## Priorità correnti

1. Rispettare ingombro 320 × 400 × 40 mm, datumi, materiali, RF hard keep-out,
   DML, componenti, ventilazione e servizio.
2. Ottenere percorsi di carico, fissaggi e rigidezza conformi; mantenere il
   criterio LC4 da 30 N e spostamento normale agli angoli <=1 mm.
3. Verificare LC1–LC7, materiali ortotropi, contatti, instabilità e convergenza
   sulla geometria corrente, con calibrazione fisica prima della qualificazione.
4. Registrare massa del solo telaio, massa completa senza doppio conteggio e
   baricentro; ridurre peso solo quando compatibile con i primi tre punti.

Il carico verticale **70 N resta il minimo di progetto**, non un limite di peso
del prodotto. Con il fattore interno 4g già previsto nel budget storico, il
carico da riesaminare è `max(70 N, 4 × massa_assemblata_kg × 9,80665 m/s²)`.
Questa regola non è una certificazione o una portata della parete. Finché la
massa completa è sconosciuta, le prove a 70 N sono solo riferimenti di confronto;
non si dichiara verificata la loro adeguatezza al prodotto più pesante.
LC3/LC4 e gli altri carichi di installazione mantengono i requisiti specifici.

Nessun cambiamento delle proprietà materiali, degli appoggi o del contributo
strutturale dell'ASA è implicito nell'aumento del budget. Parete, cleat, inserti
e anti-lift devono sostenere il carico risultante con margini verificati.

Manifest corrente: `fea/rear-frame-solver-manifest-rev-fd.json`.
