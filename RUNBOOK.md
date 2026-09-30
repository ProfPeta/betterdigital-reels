# Runbook: série „Stejný úkol. Dva světy.“

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
