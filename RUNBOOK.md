# Runbook Better Digital videí (pro Clauda)

Tenhle soubor je předávka pro nový chat nebo naplánovanou úlohu. Přečti ho celý, než začneš. Petrovi piš česky, tykej, věcně a bez vaty, upřímná kritika je vítaná.

## 1. Kontext a stav (k 18. 10. 2026)

**Kdo a kde**
- Petr Mrázek, zakladatel Better Digital (Knewbetter s.r.o.). Značka: bílá, černá `#0B0B0B`, žlutá `#FFD400`, Inter Tight + JetBrains Mono, logo „Uzel“ (funkce `uzel()` v každém `reel.html`).
- Sítě: Instagram [@betterdigital.cz](https://www.instagram.com/betterdigital.cz/), TikTok [@betterdigital.cz](https://www.tiktok.com/@betterdigital.cz). Obojí jedním postem přes **Metricool**, brand `blogId` **7151077**, timezone **Europe/Prague**.
- Repo je veřejné: `ProfPeta/betterdigital-reels` (raw URL videí slouží Metricoolu).

**Série a co už vyšlo**

| Série | Složka | Stav |
|---|---|---|
| Leadgen „Stejný úkol. Dva světy.“ | `episodes/` | **Ukončená** po dílu 3 (vyšel 14. 10.). Další díly nedělat, úlohy A/B níže neběží. |
| POSTAVILI TO (globální příběhy) | `promo/postavili-to-01-jobs`, `-02-musk` | vyšly |
| POSTAVILI TO · Česká edice | `promo/postavili-to-cz-01-avast` (12. 10. 16:00), `-02-seznam` (14. 10. 12:00), `-03-alza` (15. 10. 10:00) | vyšly / naplánované, odkazy a ID v `post.json` |
| JEDNA VĚTA (AI postaví appku z jedné věty) | `promo/jedna-veta-01-porada` | vyšel 12. 10. 10:00 |
| Jednorázové | `promo/predstaveni`, `zastav-video`, `mobil-vs-prace`, `rodinne-heslo`, `fakta-cteni-ai`, `manifest-postav-si-to` | hotové |

- Analýza sítí a plán růstu: Claude Doc „Better Digital – analýza sociálních sítí a plán růstu“ (https://claude.ai/code/artifact/44db7598-8a85-4d79-8639-36e816a86ffe), shrnutí v projektu Better digital (`claude/socialni-site-analyza-2026-10.md`).
- Pozorování: TikTok videa zůstávají na ~250–300 zhlédnutích (testovací dávka). Navrženo zkusit nativní upload v aplikaci TikTok místo přes Metricool. Instagram data v Metricoolu se zpožďují.

**Na čem se skončilo (další krok)**
Petr chce **celosvětově virální video s technologickými značkami** podle reelu https://www.instagram.com/reel/DekNf6VoVPi/. Instagram se nedá stáhnout (robots) a Chrome rozšíření nebylo připojené, takže předlohu je potřeba mít od Petra jako soubor nebo popis. Navržené nápady (vše bez hlasu, jen text + hudba, anglicky):
1. **„They said NO“** – odmítli koupit firmy, které dnes stojí miliardy (Blockbuster × Netflix, Yahoo/Excite × Google…). Doporučeno jako první.
2. „Their first product wasn't tech“ (Nokia, Samsung, Nintendo…), formát hádanky.
3. „Bought for X, now worth Y“ (Instagram, Android, YouTube).
4. „What their names actually mean“ (googol, Samsung = tři hvězdy, Intel…), pauza na hádání.
5. „How old they were when they started“.
6. „From garage to trillion“ – 3 firmy po 10 s.
Loga cizích značek Claude nekreslí; buď je dodá Petr jako soubory, nebo jsou jen textem. Fakta před výrobou ověř ve zdrojích.

## 2. Pravidla, která platí vždy

- **Nic nezveřejňuj ani neplánuj bez Petrova souhlasu.** Posty nikdy nemaž (zrušení = `draft: true`).
- Když Petr řekne „zveřejni zítra v optimální čas“: zjisti `getBestTimeToPostByNetwork` pro IG i TikTok a `getScheduledPosts` na ten den, vyber čas s nejlepším skóre, který se nekryje s jiným postem (mezera aspoň ~3 h). Píše-li „zítra“ po půlnoci, bralo se to jako ten nový den – vždy napiš, jak jsi to vyložil.
- **Štítky:** video s hlasem z ElevenLabs = `instagramData.isAiGenerated: true` a `tiktokData.isAigc: true` (realistický syntetický hlas, platformy uvádí, že dosah nesnižuje). Neprodejní obsah (POSTAVILI TO, JEDNA VĚTA, virální) = `commercialContentOwnBrand: false`. Leadgen měl `true`.
- **Fotky a loga od Petra jsou bez ověřené licence**: zdroje i zpracované verze jsou v `.gitignore` a v repu nejsou. Nový chat je nemá – pro přerender starého dílu je musí Petr nahrát znovu. Ilustrační nebo archivní fotky ve videu vždy označ („ILUSTRACE“, „ARCHIVNÍ FOTO“, „ILUSTRAČNÍ FOTO“).
- **Fakta:** každé tvrzení ve scénáři ověř na webu, zdroje dej do tabulky v `README.md` dílu. Neověřené věci vynech (např. „Alza = ALeš ZAvoral“). U čísel uváděj rok.
- Videa mají okraje: důležitý obsah v x **74–466**, y **130–740** CSS px (stage 540×960), titulky na y 664.
- Cizí loga, postavy, maskoty nekreslit kódem. Dodané soubory použít zpravodajsky.

## 3. Výroba příběhového videa s hlasem (POSTAVILI TO a podobné)

Vzor: `promo/postavili-to-cz-03-alza/` (nejnovější, nejčistší). Délka ~60–70 s.

**3.1 Scénář a prompt pro ElevenLabs**
1. Rešerše (WebSearch/WebFetch, hlavně Forbes CZ, Seznam Zprávy, E15, CzechCrunch, oficiální historie firmy). Šok nebo inspirace zhruba každých 5 s, hook v první větě, na konci výzva do komentářů (anketa další firmy).
2. Pošli Petrovi prompt: hlas **Anet – Youthful and Lively**, model **Eleven v4**. Tagy na začátku vět (`[excited]`, `[storytelling]`, `[playful]`, `[impressed]`, `[serious]`, `[amazed]`, `[casual]`, `[pause]`). Čísla a cizí jména foneticky (`dva tisíce devět set devadesát`, `Kártmenem ze Sautparku`, `Jahů`, `ímejl`, `Betr Didžitl`). Petr hlas vygeneruje a pošle mp3.

**3.2 Hlas a časy**
1. `mkdir -p promo/<slug>/voice photos/src`, mp3 jako `voice/take_elevenlabs.mp3`, zkopíruj `voice/prep.py`, `voice/timeline.py` a `export_ev.py` z Alzy.
2. `cd voice && python3 prep.py 1.08 .28` (TEMPO, max pauza) → `voice.wav` + `segments.json`. Cíl: hlas ~64–67 s, celé video ≤ 70 s.
3. Přepis segmentů: `python3 -I engine/tools/seg_asr.py voice.wav segments.json /tmp/seg.json` (model: `engine/tools/get_whisper.sh`, na pozadí). Uříznuté konce slov u krátkých segmentů jsou artefakt Whisperu – ověř delším úsekem `engine/tools/asr.py voice.wav --start 14 --end 26`.
4. `script.py`: `SENT = [('s1', ['kousek titulku', 'další *zvýraznění*']), …]` + `syllables()` s přepisem čísel na slova. `voice/map.json` = první segment (od 1) každé věty. `python3 voice/timeline.py` → `timeline.js`/`timeline.json` (END = konec hlasu + 2,4 s).

**3.3 Obraz (`reel.html`)**
- Kostra (styly, `render(t)`, titulky `#cap`, časová osa `#tl`, přechody `scan`/`glitch`/`flash`, zrno) zkopíruj z Alzy; měníš pole `SCN`, barvy v `:root`, `YEARS`/`Y0`/`Y1`.
- Scéna: `{id, from:'sN', cls, cap:1 | capS:['s3','s4'], year, dk:1 (tmavá osa na světlém pozadí), tr, html:()=>…, anim:(t,s)=>…, ev:s=>[[čas,'událost',param]]}`. Časy z `st('sN')`, `en('sN')`, `ck('sN',i)` (začátek kousku titulku). Pomocníci: `popIn`, `slideIn`, `slideX`, `stampIn`, `fade`, `typeTo`, `slamT`, `rgbSplit`, `fmt`.
- `render(t)` musí být čistá funkce času (žádné `Date.now()`, náhoda jen přes `rng(seed)`).
- Fotky: `photos/process.py` (rembg `isnet-general-use` na výřezy, `bg_alpha` na loga), spouštět `python3 -I`.
- **QA:** `python3 engine/render.py stills promo/<slug>/reel.html promo/<slug>/qa 0.3,3.5,…` (~2 snímky na scénu) a `python3 engine/sheet.py promo/<slug>/qa promo/<slug>/qa_sheet.jpg 7`, pak si arch prohlédni (Read). Hledej překryvy, přetečení, texty mimo okraje, překlepy. Opravuj, dokud není čisto.

**3.4 Zvuk (`sfx.py`)**
- Zkopíruj z Alzy: nástroje, hudební sekce (`bars(t0, t1, ['C','G','Am','F'], styl)` se styly `retro`, `light`, `full`, `dark`, `pizz`, `big`, `outro`), obsluha událostí z `fx.json` a mix (hudba uhýbá hlasu, hlas ~9 dB nad hudbou).
- `python3 export_ev.py` → `fx.json`; `python3 sfx.py audio.wav 1.33`. Hlasitost ověř `ffmpeg -i audio.wav -af ebur128=peak=true -f null -` a PRE dolaď na **−14 LUFS**. Nové typy událostí přidej do obsluhy (neznámé se vypíšou jako POZOR).

**3.5 Render a finál**
- Nástroj má limit 10 min na příkaz: render (~10 min) spouštěj na pozadí skriptem s „done“ souborem a čekej `sleep`.
  `python3 engine/render.py video promo/<slug>/reel.html promo/<slug>/raw.mp4`
- `bash engine/finalize.sh raw.mp4 audio.wav full.mp4`, pak `ffmpeg -i full.mp4 -c:v libx264 -preset slow -crf 27 -bf 0 -pix_fmt yuv420p -c:a copy -movflags +faststart video.mp4` (GitHub limit 50 MB, vychází ~22–25 MB).
- Oprava jedné scény bez celého renderu: `engine/tools/render_range.py` + `engine/tools/splice.sh`, pak znovu finalize a encode.
- Kontrola mixu Whisperem po 28 s (`engine/tools/asr.py audio.wav --start 0 --end 28` …).
- Cover: `ffmpeg -ss <s> -i full.mp4 -frames:v 1 -q:v 2 cover.jpg` (nejsilnější snímek s obličejem nebo otázkou).
- Petrovi pošli náhled 720p (`-vf scale=720:1280 -preset veryfast -crf 26`, SendUserFile má limit 30 MB) + cover.
- `README.md` dílu (scénář, fakta se zdroji, prompt, fotky), `post.json` (text, firstComment, coverMs, settings, status). `.gitignore`: `photos/src/`, `photos/*.png|*.jpg`, `qa*/`, `raw.mp4`, `full.mp4`, `audio.wav`, `qa_sheet.jpg`.
- Commit + push: `git fetch -q origin main && git rebase -q FETCH_HEAD && git push -q origin HEAD:main`.

**3.6 Popisek a plánování**
- Popisek: hook v 1. řádku (vidět bez rozkliknutí), klíčová jména v textu i hashtazích (vyhledávání TikToku), otázka do komentářů, 5 hashtagů. První komentář: bonus fakt nebo anketa + zdroje.
- Plánování: šablona JSON v části *Plánování v Metricoolu* níž, ale `providers` IG + TikTok, `isAiGenerated`/`isAigc` a `commercialContentOwnBrand` podle pravidel výše, `videoCoverMilliseconds` = coverMs, `tiktokData.title` = celý text. Před plánováním `curl -sI` na raw URL (HTTP 200). Po naplánování ulož `metricool` (id, uuid, plannerUrl) a `status: scheduled` do `post.json`, commit.

## 4. Známé pasti

- `pkill -f <vzor>` s textem, který je i ve vlastním příkazu, zabije vlastní shell. Nepoužívat.
- Instagram nejde přes WebFetch; zrcadla neobcházet. Reel buď Petr pošle jako soubor, nebo otevřít přes Chrome rozšíření (když je připojené).
- Raw URL na GitHubu se cachuje – změněné video ukládej pod novým názvem (`video-v2.mp4`).
- `updateScheduledPost` mění `id`, `uuid` zůstává.

---

# Archiv: leadgen série „Stejný úkol. Dva světy.“ (ukončená)

Návod pro automatické běhy (naplánované úlohy Clauda), které sérii vyrábějí, plánují a posílají Petrovi ke kontrole. Zprávy Petrovi piš česky, tykej a jdi rovnou k věci.

## Přehled

- Leadgen Reels pro **Better Digital**. Vychází **každou středu v 9:00 (Europe/Prague)** na Instagramu **@betterdigital.cz** a na TikToku **@betterdigital**. Obojí jde jedním postem přes **Metricool** (brand `blogId` **7151077**).
- **Zdroj pravdy je `plan.json`**: pořadí dílů, termíny, stavy a ID postů v Metricoolu.
- Každý díl je ve složce `episodes/<slug>/`:
  - `reel.html` obsahuje animaci a vykresluje se po snímcích,
  - `sfx.py` syntetizuje zvuk,
  - `video.mp4` je finální video,
  - `cover.jpg` je obálka,
  - `post.json` obsahuje popisek, první komentář, čas obálky, klíčové slovo a šablonu DM.
- Veřejná URL videa pro Metricool: `https://raw.githubusercontent.com/<repo z plan.json>/main/episodes/<slug>/<soubor videa>`.

**Stavy dílu:**

| Stav | Význam |
|---|---|
| `planned` | Díl je jen v plánu. |
| `ready` | Video a `post.json` jsou v repu. |
| `scheduled` | Díl je naplánovaný v Metricoolu a `metricool` obsahuje `id`, `uuid` a `plannerUrl`. |
| `published` | Díl už vyšel. |

Po každé změně udělej commit a push s krátkou zprávou.

## Úloha A: Výroba (pondělí dopoledne)

1. Naklonuj repo a načti `plan.json`. Projdi budoucí díly podle `publishAt` a vezmi **první, který ještě není `scheduled`**. Díky tomu výroba běží s předstihem, obvykle na díl za 9 dní. Za jeden běh dotáhni jen jeden díl.
2. Je-li ve stavu `planned`, vyrob ho podle části *Výroba nového dílu*. Pak nastav `ready`, commit a push.
3. Je-li ve stavu `ready` a `metricool` je `null`, ověř, že raw URL videa vrací HTTP 200 (repo musí být veřejné). Pak ho naplánuj podle části *Plánování v Metricoolu*. Ulož `id`, `uuid` a `plannerUrl`, nastav `scheduled`, commit a push.
4. Díly, jejichž `publishAt` už minul, přepni na `published`.
5. Udržuj v plánu aspoň 2 budoucí díly. Chybějící doplň z `topics.md`: `publishAt` o 7 dní později, `status: planned` a `teaserNext` podle následujícího tématu.
6. Když cokoli selže, pošli Petrovi krátkou zprávu, co selhalo a co je potřeba. Nikdy nic nepublikuj „natvrdo“ a nemaž posty.

## Úloha B: Kontrola (úterý 20:00)

1. Naklonuj repo a najdi díl, jehož `publishAt` připadá na **zítřek**.
2. Ověř přes `getScheduledPosts` (brandId `7151077`, rozsah od zítřka 00:00 do 23:59, timezone `Europe/Prague`), že post existuje, má video a čas 9:00 a že v `providers` je **instagram i tiktok**.
3. Když post chybí nebo nesedí, proveď úlohu A pro tento díl hned. Do zprávy Petrovi napiš, že se to dělalo na poslední chvíli.
4. Pošli Petrovi finální `video.mp4` souborem a k němu zprávu:
   - **„Zítra v 9:00 vyjde díl N: <téma>.“**
   - popisek a první komentář přesně tak, jak jsou naplánované,
   - klíčové slovo,
   - odkaz `plannerUrl`,
   - **„Když je vše v pořádku, nemusíš nic dělat. Změny mi napiš sem do středy 8:30, nebo post uprav či zastav přímo v Metricoolu.“**
5. Když Petr v té konverzaci požádá o změnu:
   - **Text:** použij `updateScheduledPost` a pošli **celý** původní obsah, změň jen to, co chce.
   - **Video:** přerenderuj ho, ulož pod **novým názvem** (`video-v2.mp4`, raw URL se cachuje), pushni a aktualizuj `media`.
   - **Zrušení:** nastav post jako draft (`draft: true`). Nemaž ho.
   - Každou změnu Petrovi potvrď.

## Výroba nového dílu

### Vizuální systém (neměnit)

**Formát a značka:**
- Rozlišení 1080×1920 (stránka 540×960 CSS px, device scale 2), 30 fps, délka **23,2 s**.
- Barvy: bílá, černá `#0B0B0B`, žlutá `#FFD400`, šedá `#8C8C8C`.
- Písmo: Inter Tight, mono JetBrains Mono (obojí v `engine/fonts`).
- Hlavička: mono „Díl N · <téma>“ a pod ní „Stejný úkol. **Dva světy.**“ se žlutým zvýrazněním.

**Časová osa:**

| Čas | Obsah |
|---|---|
| 0–14,8 s | **Split screen.** Nahoře šedý panel **RUČNĚ**: okna se vrší, bloudí kurzor, časovač letí, jsou tam typické chyby a humor ze života (`FINAL_v3.xlsx`, překlep, „Snad je to všechno…“). Dole bílý panel s černým rámem **S AUTOMATIZACÍ**: čistý tok, data „přeletí“ žlutými tečkami a vždy je tam **schválení člověkem** (tlačítko „Zkontrolovat…“ nebo „Schválit…“) a ✓. Po dokončení běží dole **Ušetřený čas** s živou poznámkou o ruční verzi („…a ruční verze je u faktury 8/30 ↑“). |
| 14,8–17,6 s | Bílý přepočet na měsíc nebo rok: „Ručně X“ vs. „S automatizací Y“ a pod tím `*modelový příklad…`. |
| 17,6–19,8 s | Černá ztrátová pointa, například „To jsou skoro 2 pracovní dny. Každý měsíc.“ |
| 19,8–23,2 s | Žlutá CTA přes `ctaScene(19.8, 23.2, 'KLÍČOVÉSLOVO', 'Díl N+1: téma')` z `engine/cta.js`. |

**Bezpečné zóny a okraje** (telefony ořezávají okraje videa a část plochy zakrývá UI TikToku a Reels; platí pro díly i pro všechna ostatní videa v `promo/`):
- Důležitý obsah drž v oblasti x 48–440 CSS px a y 130–740. Na výstupu 1080×1920 to odpovídá x 96–880 a y 260–1480.
- Vpravo je v pásmu y 430–830 lišta TikToku, proto obsah končí na x = 440.
- Šablona dílu kreslí rozvržení na původní mřížce (panely `left: 20px; width: 452px`). Konstanta `SAFE` v `render()` ho pak zmenší do bezpečné oblasti. `SAFE` nikdy neodstraňuj.
- Pozice počítané z `getBoundingClientRect()` přepočítej na layoutové px (vyděl měřítkem jako `k` u letících teček), jinak prvky ujedou.
- Pozadí scén (`.w`, `.b`, `.y`) zůstávají přes celou plochu.

**Technika:** `render(t)` musí zůstat čistou funkcí času, protože se renderuje po snímcích. Žádný `Date.now()` ani `Math.random()` bez seedu.

### Čísla

- Čísla jsou modelová, ale realistická a **vnitřně konzistentní**: součty, přepočty na měsíc a rok, časovače, ušetřený čas.
- Ve videu musí být značka `*modelový příklad`.
- Nepoužívej vymyšlené statistiky ani skutečné firmy, loga, domény nebo čísla účtů. Používej fiktivní jména a zástupné údaje (`1234567890/0100`, IČO s neplatným kontrolním součtem).

### Postup

1. `cp -r episodes/<poslední díl> episodes/<nový-slug>` a smaž v kopii `video.mp4` a `cover.jpg`.
2. Uprav `reel.html`: téma, okna, kroky, časy, čísla, texty, klíčové slovo a teaser dalšího dílu. Uprav i `DURATION`, `CUTS` a klíčové časy.
3. **QA snímky:**
   `python3 engine/render.py stills episodes/<slug>/reel.html /tmp/qa 0.5,1.5,3,4.2,6,8,10,12,13.5,14.3,16.5,18.6,21,22.9`
   a pak `python3 engine/sheet.py /tmp/qa /tmp/sheet.png`. Prohlédni kontaktní arch a detailně i 2–3 snímky v plném rozlišení. Hledej:
   - překryvy a přetečení textu,
   - dva kurzory naráz,
   - text v bezpečných zónách,
   - překlepy v češtině,
   - sedící čísla.

   Oprav a opakuj, dokud to není čisté.
4. **Zvuk:** uprav časy událostí v `sfx.py` podle `reel.html` (psaní, kliknutí, švihy, zvonek při schválení, úder na 17,6 s, CTA na 20,22 s). Pak spusť `python3 episodes/<slug>/sfx.py /tmp/audio.wav`.
5. **Video:**
   `python3 engine/render.py video episodes/<slug>/reel.html /tmp/raw.mp4` (trvá asi 2 minuty)
   a pak `bash engine/finalize.sh /tmp/raw.mp4 /tmp/audio.wav episodes/<slug>/video.mp4`. Z finálu vytáhni pár snímků a zkontroluj je.
6. **Obálka:** snímek z okamžiku, kdy je dole ✓ a nahoře chaos, ulož jako `cover.jpg`. Čas v ms dej do `post.json` jako `coverMs`.
7. **`post.json`:** vzor jsou předchozí díly.
   - `text`: hook do 125 znaků s konkrétními čísly, 2–3 krátké odstavce, CTA „Napiš KLÍČOVÉSLOVO a pošlu ti, jak by to fungovalo u vás. 👇“ a 5 hashtagů.
   - `firstComment`: zopakuje CTA a obsahuje poznámku o modelovém příkladu.
   - Dále `keyword`, `coverMs` a `dm`.

### Pravidla pro texty

- Tykej, piš krátké věty a konkrétní čísla. Ztráta motivuje víc než zisk.
- Nepoužívej fráze typu „zefektivníme procesy“, „řešení na míru“, „pomáháme firmám růst“.
- Klíčové slovo volíme ideálně bez diakritiky. Když ji má, Petr musí v ManyChatu nastavit obě varianty.

## Plánování v Metricoolu

Použij `createScheduledPost` s `blogId: "7151077"`, `date: "<publishAt>"` a `info` jako JSON řetězec:

```json
{
  "autoPublish": true,
  "descendants": [],
  "draft": false,
  "firstCommentText": "<post.json firstComment>",
  "hasNotReadNotes": false,
  "media": ["https://raw.githubusercontent.com/<repo>/main/episodes/<slug>/video.mp4"],
  "videoCoverMilliseconds": <post.json coverMs>,
  "mediaAltText": [],
  "providers": [{"network": "instagram"}, {"network": "tiktok"}],
  "publicationDate": {"dateTime": "<YYYY-MM-DDT09:00:00>", "timezone": "Europe/Prague"},
  "shortener": false,
  "smartLinkData": {"ids": []},
  "text": "<post.json text>",
  "instagramData": {"type": "REEL", "showReelOnFeed": true, "collaborators": [], "isAiGenerated": false},
  "tiktokData": {"disableComment": false, "disableDuet": false, "disableStitch": false, "privacyOption": "PUBLIC_TO_EVERYONE",
                 "commercialContentThirdParty": false, "commercialContentOwnBrand": true,
                 "title": "<post.json text>", "autoAddMusic": false, "photoCoverIndex": 0, "isAigc": false}
}
```

K TikToku:
- `tiktokData.title` je povinný a v TikToku funguje jako popisek videa. Dej do něj stejný text jako do `text`.
- `commercialContentOwnBrand: true` je povinné označení propagace vlastní firmy. Nevypínej ho.

Po naplánování ověř post přes `getScheduledPosts` a do `plan.json` ulož `id`, `uuid` a `plannerUrl`. Pozor: `updateScheduledPost` mění `id`, `uuid` zůstává stejné.

## Co nedělat

- Nepublikuj nic mimo plán a nic, co neprošlo QA.
- Neměň termíny bez Petrova souhlasu.
- Nemaž posty ani historii v repu.
- Nepřidávej sítě, které Petr nepřipojil.
