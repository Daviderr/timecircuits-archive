# Routine della domenica: bozze della settimana successiva

Usata dall'attività programmata "weekly-drafts" (ogni domenica alle 19:00, prima esecuzione utile 2026-10-11).
Cartella di lavoro: la cartella del progetto (root del repository).

## Preparazione (domenica sera)
0. **Statistiche:** `/opt/anaconda3/bin/python3 scripts/stats.py --save` (aggiunge lo snapshot a `strategy/metrics/history.csv`).
   Confronta con lo snapshot precedente e scrivi all'editore un rapporto di 5 righe: follower (variazione),
   post migliore per (salvati + condivisi) / copertura, Reel vs caroselli, una cosa da provare. Tienine conto nella scelta dei temi.
1. Leggi `CLAUDE.md`, `strategy/editorial-strategy.md`, `memory-editoriale/feedback.md` e tutti i `posts/*/post.json`
   (evita ripetizioni, rispetta la rotazione dei pilastri, il primo post deve corrispondere al "next story"
   dell'ultimo post pubblicato o approvato).
2. Scegli 3 temi per **martedì, giovedì e domenica della settimana successiva, alle 15:00 (Europe/Rome)**.
   Cartelle numerate in sequenza: `posts/P07-<slug>/`, `P08`, ...
3. Per ogni tema usa il sub-agente **researcher** → `research.md`.
4. Scrivi `post.json` con `"status": "draft"`, `"publish_mode": "auto"`, `"scheduled_at": "AAAA-MM-GGT15:00"`,
   `"timezone": "Europe/Rome"`. 8–10 slide (max 10), foto solo libere da Wikimedia Commons con credito.
5. `/opt/anaconda3/bin/python3 scripts/render.py posts/<cartella>` e controlla visivamente che nessun testo esca dalla slide.
6. Sub-agente **fact-checker** su ogni post → applica tutte le correzioni → nuovo render.
6b. **Reel:** `/opt/anaconda3/bin/python3 scripts/make_reel.py posts/<cartella>` per ogni post (video 9:16 in `reel/reel.mp4`,
    uscita lo stesso giorno alle 19:00, `reel.status` "draft").
7. `/opt/anaconda3/bin/python3 scripts/review_index.py posts/<le 3 cartelle>`; manda all'editore la pagina di approvazione
   con 3 righe di riepilogo per post.
8. **Non pubblicare e non approvare nulla da solo.**

## Dopo l'approvazione dell'editore (in chat)
- Solo per i post che l'editore approva esplicitamente: `"status": "approved"`, `"approved_at": "<data>"`, `"approved_by": "editor (chat)"`.
- I Reel hanno un'approvazione separata: solo se approvati esplicitamente, `"reel": {"status": "approved", "approved_at": "<data>"}`.
  Escono solo dopo il loro carosello.
- Registra il feedback in `memory-editoriale/feedback.md`.
- `git add posts memory-editoriale && git commit -m "Approve <post>" && git push`.
- La pubblicazione la fa GitHub Actions (`.github/workflows/publish.yml`) all'orario di `scheduled_at`.
