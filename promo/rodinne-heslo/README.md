# „Tvoje máma nepozná tvůj hlas od AI.“ (TikTok/Reels, 28 s, varianta bez natáčení)

Mámin telefon ve 23:47: hlasovka od „Kubíčka“ (nehoda, peníze, číslo účtu), zvrat „Tohle nebyl Kuba. Byla to AI. Včetně hlasu, který jsi právě slyšel.“, tři fakta, test rodinného hesla (podvodník přestane psát) a závěr „Pošli to mámě. Dřív, než jí zavolají oni.“ Konec plynule navazuje na začátek.

- `reel.html`: animace pro `engine/render.py` (540×960, 30 fps, 28 s). Kompozice je vycentrovaná, obsah je ve sloupci x 74–466 (symetrické okraje 74 px) a y 130–740. Emoji kreslí systémový Noto Color Emoji.
- `voice/`: hlasovka „Kubíčka“. Vyděšené dítě (zhruba deset let) šeptá, protože nemůže mluvit nahlas („Nemůžu volat.“). Text: „Mami, to jsem já. Měl jsem nehodu. Potřebuju hned peníze. Nemůžu volat.“
  - Proč šepot: jediný offline český model (Piper `cs_CZ-jirka-medium`) je dospělý mužský předčítač. Převod na normální dětský hlas pořád zněl uměle (intonace a „bzučení“ vokodéru). Šepot nemá hlasivky, takže tyhle stopy zmizí. Navíc podvodníci šepot a pláč opravdu používají, protože se hlas hůř pozná.
  - `make_voice.py <model TTS> --asr <whisper> --style whisper|hushed|voice`: 8 variant TTS na větu, převod vokodérem WORLD (dětské formanty ×1,25, šepot / dýchavý hlas / hlas). Whisper ověří srozumitelnost každé věty a časy slov dopočítá DTW zarovnání. Přidá šustnutí telefonu, roztřesené nádechy, popotáhnutí nosem a výdech. Zvuk telefonu dělá EQ, automatické zesílení, tichá ulice a kodek Opus 24 kb/s jako u hlasových zpráv.
  - Pro TTS se píše hovorově „Měl sem“ a protažené „Mamí“, protože Piper čte „jsem“ s j („Měli jsem“) a krátké „Mami“ zní jako „Máme“. Ve videu zůstává spisovný přepis.
  - VITS dává při každém běhu jiné varianty, takže zdrojem pravdy je uložený `voice.wav`. Po přegenerování přepiš v `reel.html` `WORDS` (časy z `words.json` + 2,66 s), `V0`, `V1`, `VEND` a `VTOT`. `SHIFT` = `V1` − 7,3 nastav v `reel.html` i v `sfx.py` a `DURATION` = 26 + `SHIFT`.
  - Kontrola: Whisper large-v3-turbo přepsal šepot z finálního mixu slovo od slova.
- Časová osa: hlasovka startuje hned po ťuknutí na Přehrát (2,66 s), první slovo zazní ve 2,99 s a poslední doznívá v 9,22 s. V t = 7,3 s obraz 2 s stojí, než hlas doběhne. `reel.html` přepočítá čas (`SHIFT`) a `sfx.py` posune všechny zvuky od 7,3 s o stejnou hodnotu. Tlukot srdce běží pod celou hlasovkou (`hold=True`).
- `sfx.py`: zvuk (hudba, efekty, hlas z `voice/voice.wav`, ducking hudby pod hlasem). Šepot je v mixu o 4,6 dB hlasitější a hudba pod ním ustoupí o 68 %. Úroveň je zhruba −13,3 LUFS, true peak pod −1 dBTP.
- `post.json`: popisek, první komentář, doporučený čas a štítek AI obsahu.

**Štítek AI:** hlas je syntetický (šepot z TTS) a realisticky simuluje skutečnou situaci. Při plánování proto zapni štítek AI obsahu (Metricool: `tiktokData.isAigc: true`, `instagramData.isAiGenerated: true`). Pointu to nekazí, protože háček o AI mluví od prvního snímku.

Čísla: McAfee (2023, 7 000 lidí v 9 zemích): 3 s nahrávky = 85% shoda hlasu, 70 % lidí si není jistých, že by klon poznalo. ČBA (září 2026): kyberpodvody za 1–7/2026 = 1,9 mld. Kč, meziročně +79 %. FBI IC3 PSA I-120324: domluvte si s rodinou tajné slovo.
