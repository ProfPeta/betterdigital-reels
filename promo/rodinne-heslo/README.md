# „Tvoje máma nepozná tvůj hlas od AI.“ (TikTok/Reels, 27 s, varianta bez natáčení)

Mámin telefon ve 23:47: hlasovka od „Kubíčka“ (nehoda, peníze, číslo účtu), zvrat „Tohle nebyl Kuba. Byla to AI. Včetně hlasu, který jsi právě slyšel.“, tři fakta, test rodinného hesla (podvodník přestane psát) a závěr „Pošli to mámě. Dřív, než jí zavolají oni.“ Konec plynule navazuje na začátek.

- `reel.html`: animace pro `engine/render.py` (540×960, 30 fps, 26,8 s). Kompozice je vycentrovaná, obsah je ve sloupci x 74–466 (symetrické okraje 74 px) a y 130–740. Emoji kreslí systémový Noto Color Emoji.
- `voice/`: skutečný mluvený hlas. Je to neuronové TTS Piper `cs_CZ-jirka-medium` (offline přes sherpa-onnx), upravené jako hlasovka nahraná telefonem venku v noci: nádech, spěch (rychlost 1,3), lehké chvění, EQ mikrofonu, komprese, tichá ulice a krátký prostor. Text: „Mami, to jsem já. Měl jsem nehodu. Potřebuju hned peníze. Nemůžu volat.“
  - `make_voice.py <složka s modelem>` vygeneruje `voice.wav` a `words.json` (časy slov). Model: `https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-cs_CZ-jirka-medium.tar.bz2`.
  - VITS dává při každém běhu trochu jiný výsledek, takže zdrojem pravdy je uložený `voice.wav`. Po přegenerování přepiš `WORDS` a `V0`/`V1` v `reel.html` podle `words.json` (+2,408 s). Když se změní délka, uprav i `SHIFT` v `reel.html` a `sfx.py`.
  - Kontrola srozumitelnosti: Whisper large-v3-turbo přepsal finální mix (hudba, efekty, AAC) slovo od slova.
- Časová osa: v t = 7,3 s obraz 0,8 s stojí, než hlas doběhne. `reel.html` přepočítá čas (`SHIFT`) a `sfx.py` posune všechny zvuky od 7,3 s o stejnou hodnotu.
- `sfx.py`: zvuk (hudba, efekty, hlas z `voice/voice.wav`, ducking hudby pod hlasem). Úroveň je zhruba −13,7 LUFS, true peak pod −1 dBTP.
- `post.json`: popisek, první komentář, doporučený čas a štítek AI obsahu.

**Štítek AI:** hlas je syntetický a realisticky simuluje skutečnou situaci. Při plánování proto zapni štítek AI obsahu (Metricool: `tiktokData.isAigc: true`, `instagramData.isAiGenerated: true`). Pointu to nekazí, protože háček o AI mluví od prvního snímku.

Čísla: McAfee (2023, 7 000 lidí v 9 zemích): 3 s nahrávky = 85% shoda hlasu, 70 % lidí si není jistých, že by klon poznalo. ČBA (září 2026): kyberpodvody za 1–7/2026 = 1,9 mld. Kč, meziročně +79 %. FBI IC3 PSA I-120324: domluvte si s rodinou tajné slovo.
