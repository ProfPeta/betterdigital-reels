# Runbook výroby videí (pro Clauda)

Přečti celé, než začneš. Petrovi piš česky, tykej, věcně, upřímná kritika je vítaná.

## 1. Kontext

- **Značka:** Better Digital (Knewbetter s.r.o.). Bílá, černá `#0B0B0B`, žlutá `#FFD400`, Inter Tight a JetBrains Mono, logo „Uzel“ (`uzel()` v `engine/story/lib.js`).
- **Sítě:** Instagram a TikTok `@betterdigital.cz`, Facebook. Vše přes Metricool, brand `7151077`, Europe/Prague.
- **Cíl obsahu:** dosah a značka, ne prodej. Stav a čísla jsou v Metricoolu a v projektu Better digital (`03-marketing-a-site.md`), ne tady.
- **Přehled starých dílů:** `archive/README.md`.

## 2. Pravidla

- **Nic nezveřejňuj, nenaplánuj ani nepushuj bez Petrova souhlasu.** Posty nemaž (zrušení = `draft: true`).
- **Všechno se dělá lokálně** v `videos/<díl>/build/`. Do GitHubu jdou jen zdroje dílu (po schválení) a hotové video přes `make.py push`.
- **Fakta:** každé tvrzení ověř na webu, zdroj do tabulky v `README.md` dílu, u čísel rok. Neověřené vynech. Tvrzení jedné strany označ („jeho slovy“) a druhou stranu dej do prvního komentáře.
- **Fotky a loga:** bez ověřené licence nesmí do gitu (`.gitignore` to hlídá). Fotky skutečných lidí nestahuj, dodá je Petr, ty pošleš odkazy na stránky. Ilustrační a archivní fotky ve videu označ. Cizí loga a postavy nekresli kódem.
- **Štítky:** hlas z ElevenLabs = `isAiGenerated` a `isAigc` zapnuté. Neprodejní obsah `commercialContentOwnBrand: false`.
- **Hudba:** jemný podklad, řeč musí být dobře slyšet. Převzatá hudba z TikToku může být licenční problém.

## 3. Formát

Jediný zdroj je `engine/spec.json`, kontroluje ho `make.py check`.

| | Hodnota |
|---|---|
| Video | 1080×1920, 30 fps, H.264 High, CRF 20, yuv420p, bez B-snímků a edit listů, do 95 MB |
| Zvuk | AAC 192 kb/s, 48 kHz, −14 LUFS, špička pod −1 dBFS |
| Příběh | 60–70 s, doporučený strop 75 s |
| Bezpečná zóna | obsah x 74–466, y 130–650, titulky y 664 (stage 540×960). QA hlásí chybu mimo x 60–480, y 118–760 |
| Fotky | zdroj aspoň 1080 px na šířku, jinak varování. Výstup sRGB, 1100 px, zdroj a licence v `photos/photos.json` |
| Carousel | 1080×1350 (IG, FB) a 1080×1920 (TikTok), z jednoho `slides.json` |

## 4. Obsah příběhu

Podle dat z Metricoolu (TikTok, 29. 9. až 4. 11.): české příběhy mají průměr přes 5 000 zhlédnutí, světové kolem 950, automatizace kolem 400. A/B otázka přinesla 193 komentářů, skóre 0–3 dohromady 2. Dokončení videa je jen v TikTok Studiu.

1. **První snímek a věta:** konflikt nebo výsledek, ne logo. Rohlík („prodával rohlíky“) měl 690 zhlédnutí, Seznam („dva roky před Googlem“) 10 338. Jeden příklad nestačí jako důkaz, ale konflikt testuj jako první.
2. **Tempo:** zvrat zhruba každých 5 s, žádný prázdný záběr (QA hlásí od 0,75 s).
3. **Konec:** jedna otázka s jednoslovnou odpovědí. Žádné skóre, žádné „napiš KLÍČOVÉ SLOVO“.
4. **Výsledek hlasování** řekni nahlas v dalším dílu, kde to dává smysl.
5. **Popisek:** háček v prvním řádku, jména a klíčová slova pro vyhledávání, nejvýš 5 hashtagů, pro každou síť zvlášť (šablona `post.json`).

## 5. Postup

```
python3 engine/make.py new <slug>
```
1. **Rešerše a scénář:** `script.py` (věty a titulky), zdroje do `README.md`, text pro ElevenLabs do `voice/prompt.txt`.
2. **Hlas:** Anet – Youthful and Lively, Eleven v4. Tagy na začátku vět (`[serious]`, `[storytelling]`, `[playful]`, `[impressed]`, `[amazed]`, `[casual]`, `[pause]`). Čísla a cizí jména foneticky (`dva tisíce dvanáct`, `Gúglu`, `Čet Džípítý`). Petr vygeneruje mp3, ulož jako `voice/take_elevenlabs.mp3`. Generování přes konektor stojí kredity, jen když o to Petr požádá.
3. **Fotky:** do `photos/src/`, popis do `photos/photos.json`.
4. **Scény a hudba:** `scenes.js`, `music.py`, `episode.json`. Pomocníci jsou v `engine/story/lib.js`, styly hudby v `engine/sfxlib.py`. Nové efekty a pomocníky přidávej do sdíleného engine, ne do dílu.
5. **Kontrola bez renderu (asi 15 s):**
   ```
   python3 engine/make.py draft <díl>
   ```
   Oprav všechny CHYBY a prohlédni `build/qa_sheet.jpg`. Mapa vět se najde sama, když sedí špatně, nastav `"map"` v `episode.json`.
6. **Výroba:**
   ```
   python3 engine/make.py all <díl>
   python3 engine/make.py transcript <díl>
   ```
   Spouštěj na pozadí. Přepis stáhne model poprvé za session (asi 2 min), číselné a cizí rozdíly proti scénáři jsou běžné.
7. **Petrovi** pošli `build/preview_720p.mp4` a `build/cover.jpg` a popisky z `post.json`.

## 6. Plánování

Po Petrově souhlasu:
1. `getBestTimeToPostByNetwork` pro každou síť a `getScheduledPosts` na daný den. Vyber nejlepší čas, který se nekryje s jiným postem. Dopiš časy do `post.json`.
2. `python3 engine/make.py push <díl>` nahraje video do větve `media`. Ověř `curl -sI` (HTTP 200).
3. `python3 engine/make.py payload <díl>` vypíše data, pro každou síť jeden `createScheduledPost`. Odpověď ukazuje `media` na `static.metricool.com`: Metricool má vlastní kopii a větev `media` ji pak nepotřebuje.
4. Id a uuid ulož do `post.json`, `status: scheduled`, commit zdrojů dílu do `main`.

Změna videa po naplánování: `updateScheduledPost` mění `id`, `uuid` zůstává. Nové video pushni pod stejným dílem a v Metricoolu vyměň `media`. Raw URL se cachuje, při opravě přejmenuj soubor (`video-v2.mp4`).

## 7. Carousel

`slides.json` ve složce dílu, pak `python3 engine/carousel/carousel.py <složka>`. Výstup je v `build/feed/` a `build/vertical/`. Přetečení textu skript hlásí.

## 8. Pasti

- `pkill -f <vzor>` s textem z vlastního příkazu zabije vlastní shell.
- Instagram nejde přes WebFetch. Předlohu reelu dodá Petr jako soubor.
- Weby mimo povolený seznam shell nestáhne, GitHub ano. Soubor na Google Drive přes konektor by musel projít celý konverzací, u videa to není reálné.
- Oprava jedné scény bez celého renderu: `engine/render.py video reel.html seg.mp4 --from F --to F`, vložení `engine/tools/splice.sh`.
- Klon: `git clone --depth 1`. Historie obsahuje stará videa a má přes 500 MB.
