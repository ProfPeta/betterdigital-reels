# POSTAVILI TO · Česká edice #3 – Alza / Aleš Zavoral (TikTok/Reels, ~70 s)

Třetí český díl série faktických příběhů lidí, kteří postavili tech. Alza vyhrála výzvu z dílu o Seznamu. Bez prodeje, cíl je dosah, sdílení a komentáře. Na konci výzva „Kterou českou firmu chceš příště?“ (Rohlík, Kiwi.com, Mews, Prusa Research).

**Styl:** modrá a zelená Alzy. Silueta s otazníkem („miliardář bez tváře“), pódium s vajgly, Didaktik M a padající jablka, živnosťák a pytel cukru, rozebraný počítač, dveře 710, prodejna Alzasoft s frontou a květinářstvím, Alzák, AlzaBoxy, kyperský vlastník, odhad Forbesu. Nahoře časová osa 1991–2026.

## Scénář (hlas) a fakta

| Věta | Ověření |
|---|---|
| Miliardář nedává rozhovory, skoro nikdo neví, jak vypadá | Zavoral se drží mimo veřejnost a podíl nikdy nepotvrdil ([Forbes 2021](https://forbes.cz/valka-o-miliardy-komu-skutecne-patri-alza/), [CzechCrunch](https://cc.cz/nejvetsi-cesky-e-shop-slavi-tricatiny-postupem-let-je-alza-tajemnejsi-nez-kdysi/)). |
| Jako kluk prodával limonádu a vajgly z pod pódia | [Forbes 2023](https://forbes.cz/byznys-s-cukrem-i-nedopalky-jak-ales-zavoral-vybudoval-nejvetsi-cesky-e-shop/) (podle knihy *Alza: Příběh firmy, která si do toho nenechala mluvit*). |
| První počítač za 2 990, vydělal si sběrem jablek | Didaktik M, 1991, peníze ze sběru a rozvozu jablek (Forbes). |
| V osmnácti živnosťák, prodává cukr z cukrovaru, kde dělal táta | 1994 (Forbes; Alza: živnost 29. 11. 1994). |
| Rozebere počítač, skládá z dílů, prodává z koleje, pokoj 710, první rok za milion | Kolej Blanice, pokoj 710 (Forbes). |
| První prodejna v Holešovicích bez reklamy, fronty, květinářka, krabice od bot | Dělnická ulice, 1998 (Forbes). |
| Alzák inspirovaný Cartmanem ze South Parku | Forbes (a také Mufem ze Studia Kamarád). Alza uvádí maskota od roku 2008. |
| Přes 60 mld. Kč tržeb, víc než 5 000 AlzaBoxů | Tržby 2024: 62,2 mld. Kč ([Forbes](https://forbes.cz/alza-slavi-historicke-trzby-a-cisty-zisk-23-miliardy-korun-navrat-k-normalu-rika-zakladatel-zavoral/)). 5 000 AlzaBoxů v listopadu 2025 ([Alza – historie](https://www.alza.cz/alza-history-then-and-now)). |
| Oficiálně patří firmě z Kypru, podíl nepotvrdil | L. S. Investments Limited, Kypr (Forbes 2021, 2023). |
| Forbes ho řadí mezi dolarové miliardáře | Odhad 46 mld. Kč, poprvé dolarový miliardář v roce 2023 (Forbes 2023). |

Název „Alza“ z **Al**eš **Za**voral ve videu záměrně není, zdroje to nepotvrzují.

## Hlas (ElevenLabs)

Anet (Youthful and Lively), Eleven v4. Nahrávku vygeneroval Petr (`voice/take_elevenlabs.mp3`, 75,0 s). `voice/prep.py 1.08 .28` zrychlí o 8 % a zkrátí pauzy: 67,4 s, 25 segmentů. Whisper po segmentech sedí se scénářem.

## Fotky a loga

Nahrál Petr, licence neověřené, nejsou ve veřejném repu (`.gitignore`). Loga a maskot jsou ochranné známky Alzy, použité zpravodajsky.

| Soubor v `photos/src/` | Použití |
|---|---|
| `zavoral_kresba.webp` | výřez kresby (háček, Forbes), označeno „ilustrace“ |
| `zavoral_foto.jpg` | mladý Zavoral v prodejně, „archivní foto“ (scéna s Kyprem) |
| `alzak.png` | maskot Alzák |
| `logo_alza.webp` | logo Alza.cz (`logo_alza_sk.png` nepoužité) |

## Výroba

1. `cd voice && python3 prep.py 1.08 .28 && python3 timeline.py`.
2. `python3 -I photos/process.py`.
3. `python3 export_ev.py` → `fx.json`.
4. `engine/render.py video promo/postavili-to-cz-03-alza/reel.html raw.mp4`, `python3 sfx.py audio.wav 1.33` (−14 LUFS), `engine/finalize.sh raw.mp4 audio.wav full.mp4`, překódování CRF 27 → `video.mp4`.
