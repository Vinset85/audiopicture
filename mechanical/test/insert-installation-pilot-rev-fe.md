# Provino d'installazione M4 — Rev.FE

Stato: CAD generato e verificato; stampa e misure **NOT_RUN**. Integra P02,
senza sostituire la prova strutturale sul nodo completo.

Il candidato è **ruthex RX-M4x8.1**, confezione GE-M4x81-001. La
[pagina del produttore](https://www.ruthex.de/products/ruthex-gewindeeinsatz-m4-50-stuck-rx-m4x8-1-messing-gewindebuchsen)
fornisce il CAD originale. Il [disegno ruthex del 15/08/2022](https://www.igo3d.com/mediafiles/Sonstiges/Ruthex/ruthex_Datenblatt_RX-Serie.pdf),
pagina 1, indica lunghezza 8,1 mm, diametro esterno 6,3 mm, invito 5,5 mm,
foro nominale 5,6 mm e profondità minima L+1 mm. Questi sono dati di catalogo,
non tolleranze del pezzo stampato né una qualificazione dell'inserto nel PC-CF.

Il provino ha base 30×30 mm, fondo 2,5 mm, boss Ø12 mm, foro Ø5,6 profondo
9,1 mm, altezza totale 11,6 mm e raccordo alla base R2 mm. Base, boss e fondo
sono scelte progettuali. La parete radiale nominale di 3,2 mm supera il minimo
di progetto di 2,5 mm. STEP e STL sono in `evidence/rev-fe/insert-coupon/`.
Non applicare una compensazione di stampa non misurata al file nominale.

Prima della prova registrare lotto e identificazione dell'inserto, materiale,
essiccazione, macchina, orientamento, percorso di stampa, pareti/riempimento,
temperature e post-trattamento. Il laboratorio definisce numerosità e strumenti
con incertezza appropriata; una singola installazione non qualifica il processo.

1. Misurare foro in più sezioni, profondità, fondo, diametro del boss e planarità.
   Conservare valori grezzi e fotografia orientata; annotare ovalità e difetti.
2. Installare seguendo la procedura applicabile del produttore e registrare
   utensile, temperatura, tempo, forza se misurata, sostegno e raffreddamento.
   La temperatura di installazione nel PC-CF non è dedotta dalla simulazione.
3. Rilevare profondità finale, inclinazione, materiale risalito nel filetto,
   crepe, deformazioni, libertà d'avvitamento e spessore del fondo residuo.
   Nessuna cricca, fondo perforato o filetto ostruito è accettabile.
4. Registrare l'eventuale rotazione durante l'avvitamento con coppia misurata.
   Non ricavare la coppia di serraggio dalle tabelle per filetti in acciaio.
5. Confrontare foro reale, installazione e sezione del provino. Solo i dati
   acquisiti possono giustificare compensazioni del foro o modifiche di processo.

I limiti numerici per inclinazione, quota di seduta, coppia e capacità richiedono
il giunto completo, il carico e il processo qualificato: restano **OPEN**. Non
attribuire a questo provino il carico ammissibile del telaio. Le prove P02 di
estrazione/taglio/coppia e a 23/50/70 °C richiedono un boss/gusset rappresentativo
e una fixture definita dal laboratorio, con cedevolezza misurata separatamente.

I fori Ø6×7 mm dei telai EU.20/EU.21/EU.22 restano surrogati FEM. Per questo
inserto sono 2,1 mm meno profondi del minimo di catalogo e 0,4 mm più larghi del
foro nominale. Occorre integrare un boss adeguato, verificare l'intero stack di
vite/cleat/inserto, rimodellare l'interfaccia installata e ripetere i gate FEM.
Non trasferire automaticamente al nuovo giunto i risultati dei fori provvisori.
