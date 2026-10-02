# „Tvoje máma nepozná tvůj hlas od AI.“ (TikTok/Reels, 27,4 s, varianta bez natáčení)

Mámin telefon ve 23:47: hlasovka od „Kubíčka“ (nehoda, peníze, číslo účtu), zvrat „Tohle nebyl Kuba. Byla to AI. Včetně hlasu, který jsi právě slyšel.“, tři fakta, test rodinného hesla (podvodník přestane psát) a závěr „Pošli to mámě. Dřív, než jí zavolají oni.“ Konec plynule navazuje na začátek.

- `reel.html`: animace pro `engine/render.py` (540×960, 30 fps, 27,4 s). Kompozice je vycentrovaná, obsah je ve sloupci x 74–466 (symetrické okraje 74 px) a y 130–740. Emoji kreslí systémový Noto Color Emoji.
- `voice/`: hlasovka „Kubíčka“, dětský hlas zhruba desetiletého kluka. Text: „Mami, to jsem já. Měl jsem nehodu. Potřebuju hned peníze. Nemůžu volat.“
  - Základ je neuronové TTS Piper `cs_CZ-jirka-medium` (offline přes sherpa-onnx). Pro každou větu se vygeneruje 8 variant a vybere se nejživější intonace.
  - Vokodér WORLD převede hlas na dětský: výška kolem 270 Hz, formanty ×1,27 (menší hlasové ústrojí), širší melodie, dýchavost a jemné chvění. Časování se nemění.
  - Rytmus dělají různě dlouhé pauzy a nádechy. Zvuk odpovídá hlasovce nahrané telefonem venku v noci: EQ mikrofonu, jemná komprese, tichá ulice.
  - Pro TTS se píše hovorově „Měl sem“ a protažené „Mamí“, protože Piper čte „jsem“ s j („Měli jsem“) a krátké „Mami“ zní jako „Máme“. Ve videu zůstává spisovný přepis.
  - `make_voice.py <model TTS> [<sherpa-onnx-whisper-turbo>]` vygeneruje `voice.wav` a `words.json`. S Whisperem ověří každou větu přepisem a nesrozumitelnou variantu vyřadí. Časy slov se počítají DTW zarovnáním na samostatně vyslovená slova. Model TTS: `https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-cs_CZ-jirka-medium.tar.bz2`.
  - VITS dává při každém běhu jiné varianty, takže zdrojem pravdy je uložený `voice.wav`. Po přegenerování přepiš v `reel.html` `WORDS` (časy z `words.json` + 2,66 s), `V0`, `V1` a `VTOT`. `SHIFT` = `V1` − 7,3 nastav v `reel.html` i v `sfx.py` a `DURATION` = 26 + `SHIFT`.
  - Kontrola: Whisper large-v3-turbo přepsal finální mix (hudba, efekty, AAC) slovo od slova.
- Časová osa: hlasovka startuje hned po ťuknutí na Přehrát (2,66 s), první slovo zazní ve 2,84 s. V t = 7,3 s obraz 1,4 s stojí, než hlas doběhne. `reel.html` přepočítá čas (`SHIFT`) a `sfx.py` posune všechny zvuky od 7,3 s o stejnou hodnotu.
- `sfx.py`: zvuk (hudba, efekty, hlas z `voice/voice.wav`, ducking hudby pod hlasem). Úroveň je zhruba −13,7 LUFS, true peak pod −1 dBTP.
- `post.json`: popisek, první komentář, doporučený čas a štítek AI obsahu.

**Štítek AI:** hlas je syntetický (dětský hlas z TTS) a realisticky simuluje skutečnou situaci. Při plánování proto zapni štítek AI obsahu (Metricool: `tiktokData.isAigc: true`, `instagramData.isAiGenerated: true`). Pointu to nekazí, protože háček o AI mluví od prvního snímku.

Čísla: McAfee (2023, 7 000 lidí v 9 zemích): 3 s nahrávky = 85% shoda hlasu, 70 % lidí si není jistých, že by klon poznalo. ČBA (září 2026): kyberpodvody za 1–7/2026 = 1,9 mld. Kč, meziročně +79 %. FBI IC3 PSA I-120324: domluvte si s rodinou tajné slovo.
