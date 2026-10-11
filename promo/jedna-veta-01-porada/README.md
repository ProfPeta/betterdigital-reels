# JEDNA VĚTA #01 – Kalkulačka porad (TikTok/Reels, 30,1 s)

První díl série, ve které AI z jediné věty postaví hotovou aplikaci. Na konci je výzva „Co máme postavit příště?“, aby další díly vybírali diváci. Video neprodává, má přinést dosah, sdílení a komentáře.

## Co je skutečné

- **Zadání.** AI (Claude) dostala jedinou větu: „Udělej kalkulačku, která v reálném čase ukáže, kolik stojí porada.“ Věta je uložená v `app/zadani.txt`.
- **Aplikace.** `app/index.html` napsala AI z té věty v jednom kroku. Člověk do kódu nesáhl a po spuštění se už nic neopravovalo.
- **Čas stavby.** 3 min 44 s (224 s), měřeno od začátku psaní kódu po ověřené spuštění v prohlížeči. Časové značky jsou v `app/build_start` a `app/build_end`. Ve videu se čas zobrazuje jako „skutečný čas stavby“.
- **Kód ve videu.** Je to skutečný soubor, 226 řádků, přehraný zrychleně jako v editoru. Video ho označuje „záznam zrychlen“. Paleta „design“ je vytažená z CSS proměnných aplikace.
- **Záznam aplikace.** Skutečná aplikace běží v Chromiu, nic se v ní nemění. Snímky natočil `app_capture.py`:
  - Ťuknutí jsou kliknutí na její tlačítka.
  - Čas aplikace řídí falešné hodiny Playwrightu (přesně 30 fps).
  - „1 hodina porady za 3 sekundy“ je skutečný výpočet aplikace, jen se hodiny posouvají rychleji. Video to označuje „záznam aplikace · čas zrychlen“.
  - Systémové písmo záznamového „telefonu“ je Inter Tight. V kontejneru je jinak jen DejaVu, zatímco telefony mají SF Pro nebo Roboto.
- **Čísla ve videu jsou čísla z aplikace.** 8 lidí, hrubá mzda 50 000 Kč, s odvody: 3 088 Kč za hodinu, 51 Kč za minutu. Výpočet: mzda ÷ 173,3 h × 1,338 (sociální 24,8 % + zdravotní 9 %).

Známá drobnost aplikace: částky od 10 000 Kč výš mohou na úzkých telefonech přetéct kartu, protože velké číslo má pevnou velikost. Ve videu se neprojeví, maximum je 3 089 Kč. Kdyby se kalkulačka sdílela odkazem, je potřeba to opravit.

## Scény a hlas

| Čas | Scéna | Hlas |
|---|---|---|
| 0,0 | Háček: běžící kalkulačka hned v prvním snímku | Jedna věta. Hotová aplikace. |
| 2,4 | Zadání se píše do pole přesně podle hlasu | Napsali jsme AI jediné zadání: Udělej kalkulačku, která v reálném čase ukáže, kolik stojí porada. |
| 9,3 | Editor: skutečný kód, časomíra 0:00 → 3:44, paleta, spuštění | AI napsala kód, navrhla design a aplikaci spustila. |
| 13,3 | Řádky kódu: AI 226, my 0 | Bez jediného řádku od nás. |
| 15,4 | Telefon: +, +, 50 tis., Spustit, tma, uhlíky, zrychlená hodina | Zadáš, kolik lidí sedí v místnosti a kolik zhruba berou. Zmáčkneš start. A díváš se, jak porada pálí peníze. |
| 22,2 | „8 lidí × 1 hodina = 3 088 Kč“, papírová vlaštovka | Pošli to tomu, kdo svolává zbytečné porady. |
| 25,9 | Výzva a podpis Better Digital | A napiš, co máme postavit příště. |

## Hlas (ElevenLabs)

Hlas je Anet (Youthful and Lively), model Eleven v4, stejně jako u série POSTAVILI TO. Nahrávku vygeneroval Petr (`voice/take_elevenlabs.mp3`, 30,0 s). Skript `voice/prep.py 1.05 .30` ji zrychlí o 5 % a zkrátí pauzy na 27,9 s. Přepis Whisperem sedí se scénářem. Jedinou odchylkou je slovo „řádku“, kde Whisper slyší „ádku“ i v originále. V titulcích je správně.

```
[excited] Jedna věta. Hotová aplikace.
[storytelling] Napsali jsme ej aj jediné zadání: Udělej kalkulačku, která v reálném čase ukáže, kolik stojí porada.
[impressed] Ej aj napsala kód, navrhla design a aplikaci spustila. Bez jediného řádku od nás.
[playful] Zadáš, kolik lidí sedí v místnosti a kolik zhruba berou. Zmáčkneš start. [pause] A díváš se, jak porada pálí peníze.
[casual] Pošli to tomu, kdo svolává zbytečné porady. A napiš, co máme postavit příště.
```

## Výroba

1. `cd voice && python3 prep.py 1.05 .30 && python3 timeline.py`. `map.json` určuje, kterým segmentem hlasu začíná každá věta. Vznikne `timeline.js` a `timeline.json`.
2. `python3 app_capture.py`. Vznikne 408 snímků aplikace v `app_frames/` (nejsou v gitu) a `app_data.js` s kódem, rozměry prvků, plánem ťuknutí a časem stavby.
3. `python3 export_ev.py`: zvukové události z animací se uloží do `fx.json`.
4. Render:
   - obraz: `engine/render.py video promo/jedna-veta-01-porada/reel.html raw.mp4`,
   - zvuk: `python3 sfx.py audio.wav` (−14 LUFS),
   - spojení: `engine/finalize.sh raw.mp4 audio.wav video.mp4`.

Hudba je syntetizovaná v `sfx.py`: F dur, 116 BPM. Klávesnice cvaká přesně na psaná písmena, kód zní jako „datový“ proud, oheň praská a ke zrychlené hodině patří mince a pokladna. Písma jsou Inter Tight a JetBrains Mono (OFL) z `engine/fonts`.
