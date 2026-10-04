# Progetto: pagina Instagram sulla storia dell'orologeria

Claude gestisce la pagina end-to-end (strategia → ricerca → testi → grafica → pubblicazione).
L'editore approva ogni post prima della pubblicazione. **Nessun post viene pubblicato senza approvazione esplicita.**

## Identità
- Nome provvisorio: vedi `brand.json` (da confermare quando l'account è creato).
- Lingua dei post: **inglese** (tono: colto ma accessibile, da storyteller, mai da catalogo).
- Lingua di lavoro con l'editore: italiano.
- Pubblico: appassionati di orologi e curiosi di storia/cinema, globale.

## Pilastri di contenuto
1. **Horology History** — invenzioni, pionieri, svolte tecniche (tourbillon, crisi del quarzo, ecc.).
2. **Brand Stories** — origini e momenti chiave delle maison.
3. **Watches on Screen** — orologi nei film e serie (Bond, Top Gun, Interstellar...).
4. **Icons & Curiosities** — modelli iconici, record d'asta, aneddoti.

Strategia e calendario: `strategy/editorial-strategy.md`.

## Ambiente
- Usa sempre **`/opt/anaconda3/bin/python3`** per gli script (il `python3` di sistema non ha Pillow né requests).
- Mai leggere o stampare il contenuto di `.env` (contiene il token di Instagram).

## Formato carosello
- 1080×1350 (4:5), 8–10 slide, JPEG.
- Slide 1 = gancio forte. Ogni slide = una sola idea, max ~40 parole, e termina spingendo allo swipe.
- Ultima slide = CTA (salva / segui / anticipazione del prossimo post).
- Caption: 3–6 righe di riassunto, sezione "Sources", 5–10 hashtag mirati.
- Struttura dati del post: `posts/<data>-<slug>/post.json` (vedi esempio esistente).
- Render: `/opt/anaconda3/bin/python3 scripts/render.py posts/<cartella>` → genera `slides/*.jpg` e `review.html`.
- Pagina di approvazione multipla: `/opt/anaconda3/bin/python3 scripts/review_index.py posts/<cartelle>` → `posts/launch-review.html`.
- Reel: `/opt/anaconda3/bin/python3 scripts/make_reel.py posts/<cartella>` → `reel/reel.mp4` (9:16, slide in sequenza, senza "Swipe"); approvazione separata in `post.json > reel`; escono alle 19:00 dopo il carosello, solo nella scheda Reel (`share_to_feed: false`).
- Statistiche: `/opt/anaconda3/bin/python3 scripts/stats.py [--save]` (sola lettura; storico in `strategy/metrics/history.csv`).
- Foto da Commons: `/opt/anaconda3/bin/python3 scripts/commons_fetch.py posts/<cartella> "File:Nome.jpg=nome-locale.jpg"`.
- Tipi di slide: `cover`, `year` (il campo `year` accetta anche orari come "10:04"), `text`, `cta`.
- Foto opzionale su qualsiasi slide: `"image": {"file": "images/x.jpg", "credit": "Autore · Licenza · Wikimedia Commons", "focus": "center 20%"}`. Sulla cover diventa sfondo sfumato, sulle altre un riquadro sopra il testo. Licenze e autori in `images/CREDITS.json` (scaricare via API di Commons, User-Agent esplicito, pause tra download).

## Regole non negoziabili
- **Accuratezza**: ogni fatto deve avere una fonte in `post.json > sources`. Se un fatto è controverso, dirlo o ometterlo.
- **Immagini**:
  - MAI generare con l'AI modelli di orologi reali, loghi o volti di persone reali.
  - AI solo per atmosfere (botteghe d'epoca, meccanismi astratti, ambientazioni).
  - Foto reali solo da fonti con licenza libera (Wikimedia Commons, pubblico dominio), citando l'autore.
  - Niente fotogrammi di film né foto ufficiali dei brand.
- **Pubblicazione**: solo tramite Instagram API ufficiale, mai automazione del browser.
  GitHub Actions (`.github/workflows/publish.yml`) pubblica i post con `status: approved` + `approved_at`,
  `publish_mode: auto` e `scheduled_at` passato. L1 è stato pubblicato a mano; L2–L6 sono `auto`.
  Routine settimanale: `routines/weekly-drafts.md`. Guida operativa: `docs/guida-lancio-e-automazione.md`.

## Flusso per ogni post
1. Scegli il tema dal calendario → 2. sub-agente **researcher** (`.claude/agents/researcher.md`) → `research.md` →
3. scrivi `post.json` (+ foto libere) → 4. render → 5. sub-agente **fact-checker** indipendente → `factcheck.md`, applica le correzioni →
6. presenta `review.html` / `launch-review.html` all'editore →
7. su "approvato" programma la pubblicazione → 8. registra feedback in `memory-editoriale/feedback.md`.

Leggi sempre `memory-editoriale/feedback.md` prima di scrivere un nuovo post.
