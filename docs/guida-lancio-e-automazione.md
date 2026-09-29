# Guida: lancio manuale + configurazione dell'automazione

## Calendario
| Data | Cosa |
|---|---|
| mar 29/9 → dom 4/10, ore 15:00 | Pubblichi **a mano** L1 → L6, uno al giorno |
| entro dom 4/10 | Configurazione Meta + GitHub (parti B e C) |
| lun 5/10, 08:05 | Prima attività automatica: 3 bozze per mar 6, gio 8, dom 11 |
| dopo la tua approvazione | GitHub Actions pubblica all'orario previsto, anche con il Mac spento |

---

## A. Pubblicare a mano un post di lancio (10 minuti)

**Sul Mac**
1. Apri la cartella del post, es. `posts/L1-omega-speedmaster-moon/slides/`.
2. Seleziona le slide da `01.jpg` all'ultima → tasto destro → **Condividi → AirDrop** → il tuo iPhone.
   Finiscono nell'app Foto.
3. Apri `caption.txt` nella stessa cartella del post e copia tutto il testo (⌘A, ⌘C).
   Con lo stesso ID Apple e Handoff attivo, lo potrai incollare direttamente sull'iPhone.
   In alternativa, mandati il file con AirDrop.

**Sull'iPhone, in Instagram**
4. Controlla di essere su **@timecircuits.archive**, non sul tuo profilo personale.
5. Tocca **+** → **Post**.
6. Tocca la slide **01**, poi l'**icona con le due frecce** in basso a sinistra dell'anteprima, finché
   vedi l'immagine **intera e verticale** (formato 4:5, non quadrato).
7. Tocca **Seleziona più elementi** (icona dei quadrati sovrapposti) e poi le altre slide **in ordine**
   02, 03, …. Il numero sul pallino deve corrispondere al nome del file.
8. **Avanti** → nessun filtro → **Avanti**. Se Instagram propone della musica, saltala.
9. Incolla la caption.
10. **Impostazioni avanzate**: disattiva la condivisione su Facebook. Non attivare l'etichetta AI:
    queste slide non sono generate con l'AI.
11. Alle 15:00 tocca **Condividi**.
12. Nella prima ora rispondi a eventuali commenti. Se vuoi, condividi il post nelle Storie (icona aeroplanino → Aggiungi alla storia).
13. Scrivimi "**L1 pubblicato**" con il link al post: lo segno come pubblicato.

| Post | Data |
|---|---|
| L1 Omega Speedmaster | mar 29/9 |
| L2 John Harrison | mer 30/9 |
| L3 Cartier Santos | gio 1/10 |
| L4 Quartz Crisis | ven 2/10 |
| L5 Marty McFly's Casio | sab 3/10 |
| L6 Why 10:10 | dom 4/10 (per ultimo, così resta in cima alla griglia) |

---

## B. Collegare Instagram all'API di Meta (20–30 minuti, una volta sola)
Password e token li inserisci **tu**. Claude non li digita e non li legge in chat.

1. Vai su **developers.facebook.com** → *Inizia* e accedi con il tuo Facebook personale.
   L'account sviluppatore non è visibile al pubblico. Accetta i termini e verifica telefono/email.
2. **Le mie app → Crea app** → nome es. "Time Circuits Publisher" → caso d'uso
   **"Gestisci messaggi e contenuti su Instagram"** → tipo **Business** (se richiesto) → crea.
3. Nel menu dell'app: **Ruoli dell'app → Ruoli → Tester Instagram → Aggiungi** → `timecircuits.archive`.
4. Sull'iPhone, account @timecircuits.archive: **Impostazioni → Autorizzazioni sito web →
   App e siti web → Inviti tester → Accetta**.
5. Torna nell'app Meta: **Casi d'uso → Instagram → Configurazione API con login di Instagram** →
   *Genera token di accesso* → aggiungi l'account → accedi con @timecircuits.archive e concedi i permessi
   (`instagram_business_basic`, `instagram_business_content_publish`).
6. Annota due valori: l'**ID utente Instagram** (numero accanto all'account) e il **token di accesso**
   (lunga stringa). Non incollarli in chat: li userai nella parte C, punto 6.

> Le schermate di Meta cambiano spesso. Se qualcosa non corrisponde, apriamo la pagina nel browser
> integrato e ti guido schermata per schermata.

---

## C. Configurare GitHub (20 minuti, una volta sola)

1. **Crea un account** su github.com, gratuito. Puoi usare la stessa email della pagina Instagram.
2. **Installa lo strumento GitHub** nel Terminale del Mac:
   ```bash
   brew install gh
   ```
3. **Accedi** (si apre il browser, conferma tu):
   ```bash
   gh auth login
   ```
   Scegli: GitHub.com → HTTPS → Login with a web browser.
4. **Dimmi il tuo nome utente GitHub.** Io faccio il primo commit e creo il repository **pubblico**
   `timecircuits-archive`: deve essere pubblico perché Instagram possa scaricare le immagini.
   Prima di pubblicarlo ti chiederò conferma.
5. **Crea un token dedicato al rinnovo automatico:** github.com → Settings → Developer settings →
   *Personal access tokens* → **Fine-grained tokens** → *Generate new token*.
   - Repository access: **Only select repositories** → `timecircuits-archive`
   - Permissions → Repository → **Secrets: Read and write** (nient'altro)
   - Scadenza: 1 anno
6. **Salva i segreti nel repository** dal Terminale, nella cartella del progetto. Ogni comando ti chiede di
   incollare il valore, che non appare a schermo:
   ```bash
   gh secret set IG_USER_ID
   ```
   ```bash
   gh secret set IG_ACCESS_TOKEN
   ```
   ```bash
   gh secret set GH_SECRETS_PAT
   ```
7. Scrivimi "**segreti impostati**". Farò un controllo in sola lettura dell'account, senza pubblicare nulla.

## Cosa succede dopo, ogni settimana
1. **Lunedì 08:05:** Claude prepara 3 bozze verificate e ti manda la pagina di approvazione.
2. **Tu:** rispondi con "approvo P07, P08" oppure con le correzioni.
3. **Claude:** segna i post approvati e li carica su GitHub.
4. **GitHub Actions:** controlla ogni 30 minuti e pubblica ogni post approvato quando arriva la sua ora.
   Non pubblica mai un post non approvato.
5. **Il 1° di ogni mese:** il token di Instagram si rinnova da solo.

⚠️ L'attività del lunedì gira sul Mac, con l'app Claude aperta. Se l'app è chiusa, parte alla prima apertura.
La pubblicazione invece gira nel cloud di GitHub.
