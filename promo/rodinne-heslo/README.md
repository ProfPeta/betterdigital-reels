# „Tvoje máma nepozná tvůj hlas od AI.“ (TikTok/Reels, 28,8 s, varianta bez natáčení)

Mámin telefon ve 23:47: hlasovka od „Kubíčka“ (nehoda, peníze, číslo účtu), zvrat „Tohle nebyl Kuba. Byla to AI. Včetně hlasu, který jsi právě slyšel.“, tři fakta, test rodinného hesla (podvodník přestane psát) a závěr „Pošli to mámě. Dřív, než jí zavolají oni.“ Konec plynule navazuje na začátek.

- `reel.html`: animace pro `engine/render.py` (540×960, 30 fps, 28,8 s). Kompozice je vycentrovaná, obsah je ve sloupci x 74–466 (symetrické okraje 74 px) a y 130–740. Emoji kreslí systémový Noto Color Emoji.
- `voice/`: hlasovka „Kubíčka“, mladého kluka kolem 19 let, který po nehodě vyděšeně prosí o peníze.
  - Hlas je navržený v ElevenLabs (Voice Design, uložený jako „Kubíček – mladý kluk (rodinné heslo)“). Nahrávku `take_elevenlabs.mp3` vygeneroval Petr v aplikaci ElevenLabs tímto promptem:
    `[scared] [breathless] Mami… to jsem já. [trembling voice] Měl jsem nehodu. [on the verge of tears] Potřebuju hned peníze. [softly] Nemůžu volat.`
  - Dětský hlas ElevenLabs navrhnout nedovolí (bezpečnostní pravidla). Proto je Kubíček mladý muž, což do příběhu sedí (jel autem a měl nehodu).
  - `process_take.py` udělá z nahrávky hlasovou zprávu z telefonu: ořízne ticho, přidá šustnutí telefonu, EQ mikrofonu a jemnou kompresi, tichou noční ulici místo digitálního ticha v pauzách a kodek Opus 24 kb/s. Výstup je `voice.wav` a `words.json`.
  - Časy slov jsou ručně zarovnané na nahrávku: konce vět podle ticha, hranice uvnitř vět podle sykavek a souhlásek. Ověřil je přepis Whisperu na postupně prodlužovaných úsecích. Vzlyky mezi slovy se nezvýrazňují, „Mami,“ svítí i přes vzlyk po něm.
  - Při nové nahrávce přepiš `WORDS` v `process_take.py`, spusť ho a pak přepiš v `reel.html` `WORDS` (časy z `words.json` + 2,66 s), `V0`, `V1`, `VEND` a `VTOT`. `SHIFT` = `V1` − 7,3 nastav v `reel.html` i v `sfx.py` a `DURATION` = 26 + `SHIFT`.
  - `make_voice.py` je offline náhradní cesta (Piper TTS + WORLD: šepot, přidušený nebo dětský hlas). Ve finálním videu se nepoužívá.
  - Kontrola: Whisper large-v3-turbo přepsal hlas z finálního mixu slovo od slova.
  - Licence: komerční použití nahrávek z ElevenLabs je povolené jen z placeného tarifu (od Starteru), free tarif ho nemá.
- Časová osa: hlasovka startuje hned po ťuknutí na Přehrát (2,66 s), první slovo zazní ve 2,71 s, poslední doznívá v 10,0 s a zpráva má 0:07. V t = 7,3 s obraz 2,8 s stojí, než hlas doběhne. `reel.html` přepočítá čas (`SHIFT`) a `sfx.py` posune všechny zvuky od 7,3 s o stejnou hodnotu. Tlukot srdce běží pod celou hlasovkou (`hold=True`).
- `sfx.py`: zvuk (hudba, efekty, hlas z `voice/voice.wav`, ducking hudby pod hlasem). Hlas je v pásmu řeči 22–29 dB nad hudbou, hudba pod ním ustoupí o 68 %. Úroveň je zhruba −13,6 LUFS, true peak pod −1 dBTP.
- `post.json`: popisek, první komentář, doporučený čas a štítek AI obsahu.

**Štítek AI:** hlas je syntetický (ElevenLabs) a realisticky simuluje skutečnou situaci. Při plánování proto zapni štítek AI obsahu (Metricool: `tiktokData.isAigc: true`, `instagramData.isAiGenerated: true`). Pointu to nekazí, protože háček o AI mluví od prvního snímku.

Čísla: McAfee (2023, 7 000 lidí v 9 zemích): 3 s nahrávky = 85% shoda hlasu, 70 % lidí si není jistých, že by klon poznalo. ČBA (září 2026): kyberpodvody za 1–7/2026 = 1,9 mld. Kč, meziročně +79 %. FBI IC3 PSA I-120324: domluvte si s rodinou tajné slovo.
