# Il Veggente dà i numeri – procedura settimanale

Carosello di FantaVeggente pubblicato su Instagram (@fantaveggente) e sulla Pagina Facebook FantaVeggente
**il giorno dopo la fine di ogni giornata di Serie A**. Prima di pubblicare serve sempre l'ok del titolare.

## 1. Controllo del mattino (ogni giorno)

1. Trova l'ultima giornata di Serie A iniziata (fonti: tuttocampo.it, fantacalcio-online.com, legaseriea.it).
2. La giornata è "finita ieri" se l'ultima partita giocata nelle date previste del turno si è giocata **ieri** (ora italiana).
   - Partita rinviata di settimane: non aspettarla, la giornata finisce con l'ultima partita giocata nelle date previste.
   - Nessuna partita ieri, giornata ancora in corso, pausa nazionali: **non fare niente** e chiudi la sessione senza messaggi.
3. Se nel repository esiste già la cartella `gN/` di quella giornata, non fare niente (già fatto).

## 2. Raccolta dei dati

- Voti **Fantacalcio.it**: pagine `fantacalcio-online.com/it/serie-a/2026-2027/voti/N-giornata/<casa>-<trasferta>` (colonna FC) e pagelle di fantacalcio.it.
- Eventi: marcatori, assist, autogol (controlla le decisioni ufficiali della Lega sui gol contesi), rigori sbagliati/parati, espulsioni.
- Fantavoto con bonus e malus classici: +3 gol, +1 assist, +3 rigore parato, −3 rigore sbagliato, −2 autogol, −1 gol subito (portiere), −0,5 ammonizione, −1 espulsione.

## 3. Scelta degli eventi (5–8)

- Solo eventi che toccano il fantacalcio di molti: difese e portieri delle grandi, attaccanti titolari, giocatori presenti in tante rose.
- Cose improbabili: goleade subite, triplette inattese, autogol, rigori parati, squadre che vincono senza dare bonus, gol decisivi dalla panchina.
- Niente cognomi che scatenano polemiche politiche. Niente foto né loghi di club.
- Ordina dalla meno alla più improbabile.

## 4. Probabilità ("quante possibilità c'erano")

Stime fatte con i dati di prima della partita, arrotondate:
- gol di squadra: modello di Poisson con i gol attesi dalla forza in attacco e in difesa delle due squadre;
- gol di un giocatore: media gol ogni 90 minuti (stagione scorsa e questa) e minuti attesi;
- autogol, rigori, rigori parati: frequenze storiche della Serie A (un rigorista ne sbaglia circa 1 su 5).
Scrivi la percentuale con la virgola italiana ("0,23%") e "1 su N" con il punto delle migliaia ("1 su 2.500").

## 5. Testi

- `cosa`: una riga come un titolo ("Para due rigori. Ne prende sei.").
- `card` (riquadro "Al fantacalcio"): **una riga sola** su Instagram. `**x**` = numero in oro, `!!x!!` = malus in rosso.
- `frase`: ironica, da taggare o commentare, **una riga sola**. Spirito "e ti pareva, proprio contro di me". Evita "sfortunato".
- Copertina: titolo "N cose improbabili dell'ultima giornata.", frase "Lo X% di possibilità contro di te. E ti pareva." con X = l'evento più "doloroso" e riconoscibile, e "Se te n'è capitata più di una, ti siamo vicini."

## 6. Generazione

```
cd generatore && npm i && python3 genera.py ../giornate/gN.json && python3 esporta.py N
```
- Copia `generatore/esempi/g9.json` in `giornate/gN.json` e cambia giornata, copertina ed eventi.
- Lo script avvisa con "ATTENZIONE" se un testo è troppo lungo: accorcialo finché non ci sono avvisi.
- Guarda tutte le slide (Instagram e TikTok) prima di andare avanti.
- `esporta.py` crea `gN/01.jpg …` e `gN/tiktok.zip`. Fai commit e push su `main`.
- Lo **stile grafico è approvato e non va cambiato** (font, colori, impaginazione, neon, logo).

## 7. Approvazione

Manda al titolare, con SendUserMessage e i file delle slide (SendUserFile, status "proactive"):
- le slide, il testo del post, una riga sulle stime più approssimative;
- la domanda: "Rispondi **ok** e lo pubblico, oppure dimmi cosa cambiare."

**Non pubblicare senza un "ok" esplicito.** Il titolare di solito risponde verso le 13, in pausa pranzo.

## 8. Pubblicazione (dopo l'ok)

Immagini: `https://raw.githubusercontent.com/FantaOracolo/fantaveggente-social/main/gN/01.jpg` … (controlla che rispondano `image/jpeg`).

- **Instagram** – Zapier `InstagramBusinessCLIAPI`, azione `publish_media_v2`, `instagramPageId` = `17841415718855829` (FantaVeggente 🔮). `media` = lista degli URL in ordine, `caption` = testo.
- **Facebook** – Zapier `FacebookV2CLIAPI`, azione `page_photo`, `page` = `1329722330235050` (Pagina FantaVeggente). `source` = stessa lista, `message` = testo.
- Usa solo questi ID: l'account Facebook amministra anche altre pagine che non vanno toccate.
- Dopo la pubblicazione verifica il post Instagram (azione `new_media`) e manda al titolare il link.

## Testo del post (modello)

```
Il Veggente dà i numeri. 🔮

N cose improbabili dell'ultima giornata, con quante possibilità c'erano.
<2-3 frasi sugli eventi più assurdi, con le percentuali>

E ti pareva: proprio contro di te.

Quale ti è successa? Scrivi il numero nei commenti 👇
Più di una? Scrivile tutte. Ti siamo vicini.

#fantacalcio #serieA #fantacalcioitalia #fantallenatore #ilveggentedainumeri
```

Testo TikTok (il titolare lo pubblica a mano con `tiktok.zip`):
```
Lo X% di possibilità. E ti pareva: proprio contro di me. Quale ti è capitata? #fantacalcio #serieA #fantallenatore #ilveggentedainumeri
```
