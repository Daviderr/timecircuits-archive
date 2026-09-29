# Guida: creare l'account Instagram della pagina e collegarlo all'API

Tempo totale: circa 45 minuti. Le fasi 1–3 le fai tu dal telefono. La fase 4 la facciamo insieme.

---

## Fase 1 — Preparazione (5 min)
1. **Crea un'email dedicata**, per esempio un nuovo Gmail tipo `thewatchchronicle.ig@gmail.com`.
   Così la pagina resta separata dalla tua vita personale e potrai cederla o delegarla in futuro.
2. **Scegli il nome utente.** Controlla che sia libero cercandolo su Instagram. Serve anche il nome
   visualizzato (può contenere spazi, es. "The Watch Chronicle").

## Fase 2 — Crea il nuovo account senza toccare il tuo personale (10 min)
1. Apri Instagram sul telefono, dal tuo profilo personale.
2. Tocca il **tuo nome utente in alto** (o ☰ → Impostazioni → *Aggiungi account*) → **Crea nuovo account**.
3. Inserisci nome utente e password nuovi. Quando chiede email/telefono, usa **l'email nuova** della Fase 1.
4. Se ti chiede di aggiungere l'account al **Centro gestione account** insieme al tuo personale:
   puoi dire di sì (comodo per la fase 4). **I follower del tuo account personale non vedranno nulla**,
   gli account restano pubblicamente separati.
5. Da ora puoi passare da un account all'altro toccando il nome utente in alto.

> ⚠️ Attenzione nei primi giorni: controlla sempre su quale account sei prima di pubblicare o commentare.

## Fase 3 — Trasformalo in account professionale (5 min)
1. Sul nuovo account: ☰ → **Impostazioni e privacy** → **Tipo di account e strumenti** →
   **Passa a un account professionale**.
2. Categoria: **Creator digitale** oppure **Sito web di intrattenimento/educativo**.
3. Tipo: **Business** (consigliato per l'API). Salta pure la parte di collegamento alla Pagina Facebook:
   con il metodo che useremo **non serve una Pagina Facebook**.
4. Profilo: per ora lascia vuoti bio e immagine, li prepariamo noi (logo e bio in inglese).

### Riscaldamento dell'account (importante)
I nuovi account che pubblicano subito in automatico vengono spesso limitati. Per 5–7 giorni:
- Usalo come un utente normale: segui 20–30 pagine di orologi, metti qualche like, guarda le Stories.
- Pubblica **a mano** i primi 2–3 caroselli che prepariamo.
- Solo dopo attiviamo la pubblicazione automatica.

## Fase 4 — Collegamento all'API ufficiale (20 min, lo facciamo insieme)
Useremo la **"Instagram API with Instagram Login"**. Non richiede Pagina Facebook.

1. Vai su **developers.facebook.com** e accedi con il tuo Facebook personale
   (serve solo per l'account sviluppatore, è invisibile al pubblico). Se non hai Facebook, va creato.
2. Registrati come sviluppatore (accetta i termini, verifica telefono/email).
3. **Crea un'app** → caso d'uso relativo alla **gestione di messaggi e contenuti su Instagram**.
4. Nel pannello dell'app: aggiungi il tuo nuovo account Instagram come **tester**, poi accetta
   l'invito dall'account Instagram (Impostazioni → App e siti web → Inviti tester).
5. Genera un **token di accesso** con i permessi:
   - `instagram_business_basic`
   - `instagram_business_content_publish`
6. Il token lo salviamo in un file `.env` locale (mai nei file del progetto condivisi).
   Dura 60 giorni: lo rinnoverà uno script automatico.

L'app può restare in "modalità sviluppo": per pubblicare sul **proprio** account non serve la revisione di Meta.

> Le schermate di Meta cambiano spesso. Quando arrivi a questa fase aprile nel browser integrato
> e ti guido schermata per schermata. **Password e token li inserisci tu**, io non li digito.

## Fase 5 — Hosting delle immagini (lo configuro io)
L'API vuole le immagini a un indirizzo web pubblico. Useremo uno storage gratuito (es. Cloudflare R2)
dove lo script carica i JPEG approvati poco prima della pubblicazione.
