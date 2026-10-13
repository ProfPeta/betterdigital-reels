# POSTAVILI TO · Česká edice #2 – Seznam / Ivo Lukačovič (TikTok/Reels, ~66 s)

Druhý český díl série faktických příběhů lidí, kteří postavili tech. Bez prodeje, cíl je dosah, sdílení a komentáře. Seznam vybraný jako další díl po Avastu. Na konci výzva „Kterou českou firmu chceš příště?“ (Rohlík, Kiwi.com, Mews, Alza).

**Styl:** červená Seznamu, noční ložnice z roku 1996, okno Netscape s katalogem, vytáčecí modem, výplatní páska, plakát „Hledá se“ pro Krastyho. Nahoře časová osa 1996–2026. Na konci vtip o společné průmyslovce se zakladatelem Better Digital.

## Scénář (hlas) a fakta

| Věta | Ověření |
|---|---|
| Dva roky před Googlem spustil student z ložnice rodičů český vyhledávač | Seznam vznikl v roce 1996, Google v roce 1998 ([Seznam Zprávy](https://www.seznamzpravy.cz/clanek/tech-seznam-cz-vznikl-dva-roky-pred-googlem-podivejte-se-jak-se-za-30-let-promenil-306845)). Začátek v pokojíčku u rodičů ([Forbes](https://forbes.cz/cesta-z-pokojicku-k-miliardovym-ziskum-20-let-seznamu-ve-20-tweetech/)). |
| A Google ho tady pak roky nedokázal porazit | Obecně známé, Seznam byl v ČR dlouho jedničkou ve vyhledávání. Bez konkrétního čísla. |
| Podle amerického Yahoo programuje katalog českých webů a pojmenuje ho Seznam | Forbes, Seznam Zprávy. |
| Startovní kapitál 80 000 Kč: úspory, půjčka od táty, kupónová knížka | 50 000 Kč úspory, 15 000 Kč od otce, 15 000 Kč za prodanou kupónovou knížku (Forbes). |
| Modem, který v noci budil tátu | Forbes. |
| O dva roky později nejnavštěvovanější český web | 1998 (Forbes). |
| 2001 ztráta, Ivo si nebere plat | Forbes. |
| E-mail, Mapy, Sreality, zprávy | Služby Seznamu, různé roky. |
| Krasty se ztratil v lese, nikdo ho (offline) neviděl | Maskot od roku 2003, „ztratil se“ v roce 2008 (Forbes). Fotka psa ve videu je ilustrační, označená. |
| Dnes Seznam používá skoro 90 % českých uživatelů internetu | Údaj Seznamu k 30. výročí ([Seznam Zprávy](https://www.seznamzpravy.cz/clanek/domaci-zivot-v-cesku-seznam-cz-slavi-30-narozeniny-drzi-si-pozici-ceske-internetove-jednicky-305100)). |
| Ivo si koupil vlastní letiště | Letiště Praha-Točná, 2008 ([E15](https://www.e15.cz/nazory-a-analyzy/cesta-iva-lukacovice-od-cimrmanovskych-zacatku-mezi-nejnadejnejsi-bohace-sveta-751817)). Narozen 7. 2. 1974. |
| Chodil na stejnou průmyslovku jako zakladatel Better Digital | E15 uvádí „průmyslovou školu“. Že jde o Smíchovskou SPŠ, je údaj Petra Mrázka, veřejně jsme ho neověřili. |

## Hlas (ElevenLabs)

Hlas Anet (Youthful and Lively), Eleven v4. Nahrávku vygeneroval Petr (`voice/take_elevenlabs.mp3`, 68,9 s). `voice/prep.py 1.05 .28` zrychlí o 5 % a zkrátí pauzy: 63,8 s, 28 segmentů. Přepis Whisperem po segmentech sedí se scénářem.

## Fotky a loga

Nahrál Petr, licence neověřené, proto nejsou ve veřejném repu (`.gitignore`). Loga jsou ochranné známky vlastníků, použitá zpravodajsky.

| Soubor v `photos/src/` | Použití |
|---|---|
| `ivo_mlady.webp` | Ivo před nápisem SEZNAM.CZ, „archivní foto“ |
| `ivo_hory.jpg` | výřez, scéna s letištěm |
| `pes.jpg` | výřez psa, Krasty (ilustrační foto) |
| `logo_s.png`, `logo_mapy.png`, `logo_zpravy.png` | logo S, Mapy.cz, Seznam Zprávy |

## Výroba

1. `cd voice && python3 prep.py 1.05 .28 && python3 timeline.py` (`map.json` = první segment každé věty).
2. `python3 -I photos/process.py`.
3. `python3 export_ev.py` → `fx.json`.
4. `engine/render.py video promo/postavili-to-cz-02-seznam/reel.html raw.mp4`, `python3 sfx.py audio.wav` (−14 LUFS), `engine/finalize.sh raw.mp4 audio.wav video.mp4`, překódování CRF ~27 kvůli GitHubu.

Hudba je syntetizovaná v `sfx.py` (96 BPM), modem je vytáčecí sekvence (DTMF, handshake, šum).
