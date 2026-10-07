# POSTAVILI TO #01 – Steve Jobs (TikTok/Reels, 62,2 s, verze 2 „retro Mac“)

První díl série faktických příběhů lidí, kteří postavili tech (další na řadě: Gates, Wozniak, Ballmer, Musk…). Žádný prodej, cílem jsou dosahy, komunita a značka. Na konci je jen malý podpis Better Digital a otázka „Koho chceš v dalším díle?“.

**Styl (verze 2, retro Mac):** duhové pruhy z loga 1977 jako motiv celého videa: přechody mezi kapitolami, pruhované nadpisy („30“, „#1“), výplně a vrata garáže. Okna, dialogy, menu a kurzor připomínají počítače z 80. let. Kurzor kliká na tlačítka: OK u vyhazovu, Odejít u školy, menu Písmo, Restartovat po vyhazovu, anketa a Odeslat. Fotky jsou v 1bit Atkinsonově ditheringu (stejný algoritmus používal původní Macintosh). Mezi kapitolami se střídá pixelové rozpuštění, VHS šum a přetáčení u krize 1997 a bílý záblesk „restartu“ před NeXT. Na každý kousek titulku přijde nový podnět (zhruba každou sekundu). Titulky běží podle hlasu. Nahoře je duhový ukazatel času 1955–2011 s rokem scény.

## Scénář (hlas) a fakta

| Věta | Ověření |
|---|---|
| Ve třiceti ho vyhodili z firmy, kterou sám založil. | Jobs, Stanford 2005: „I had just turned 30. And then I got fired.“ Odchod 1985 po sporu se Sculleym (Wikipedia). |
| Z vysoké odešel po jednom semestru. Dál ale chodil na kurz kaligrafie. | Stanford 2005: po 6 měsících odešel z Reed College, dalších ~18 měsíců chodil jako „drop-in“, mimo jiné na kaligrafii. |
| Bez něj by prý Mac nikdy neměl krásná písma. | Stanford 2005: „If I had never dropped in on that single course in college, the Mac would have never had multiple typefaces or proportionally spaced fonts.“ |
| V roce 1976 založil se Stevem Wozniakem v garáži Apple. | Apple Computer Company založen 1. 4. 1976 (Jobs, Wozniak, Wayne). Jobs: „Woz and I started Apple in my parents' garage.“ |
| Za deset let to byla firma za dvě miliardy dolarů. | Stanford 2005: „a $2 billion company with over 4,000 employees“. |
| Založil NeXT a koupil malou firmu jménem Pixar. | NeXT 1985. V roce 1986 financoval odštěpení Graphics Group (později Pixar) od Lucasfilmu za 10 mil. $ (Wikipedia). |
| Ta pak natočila Toy Story, první celovečerák celý z počítače. | Toy Story (1995), první celovečerní film vytvořený celý na počítači (Stanford 2005, Wikipedia). |
| V roce 1997 se vrátil do Applu na pokraji bankrotu. | Apple koupil NeXT (dohoda 12/1996, dokončeno 2/1997). Jobs byl od 16. 9. 1997 dočasný CEO. Bloomberg 2011: „Apple Rises From Near Bankruptcy…“ |
| Michael Dell tehdy řekl, že by ho zavřel a peníze vrátil akcionářům. | 6. 10. 1997, Gartner Symposium: „I'd shut it down and give the money back to the shareholders.“ (Cult of Mac, CNET 1997) |
| Pak přišel iMac. iPod. iPhone. | 1998, 2001, 2007 (Wikipedia). |
| V srpnu 2011 byl Apple nejhodnotnější firmou na světě. | 9. 8. 2011 předběhl Exxon Mobil, 337,2 mld. $ (Bloomberg). |
| O dva měsíce později Steve Jobs zemřel. | 5. 10. 2011, Palo Alto, 56 let. |
| O vyhazovu řekl, že to bylo to nejlepší, co se mu mohlo stát. | Stanford 2005: „getting fired from Apple was the best thing that could have ever happened to me“. |
| Stay hungry. Stay foolish. | Závěr projevu na Stanfordu 2005 (citát z The Whole Earth Catalog). |

**Údaje navíc na obrazovce (verze 2):** Reed College 1972 · garáž v Los Altos · Apple I 1976 · duhové logo (používané 1977–1998) · NeXT založen 1985 · Pixar = Graphics Group Lucasfilmu, 1986, 10 mil. $ · Exxon Mobil 330,8 mld. $ vs. Apple 337,2 mld. $ při zavření burzy 9. 8. 2011 ([Bloomberg](https://www.bloomberg.com/news/articles/2011-08-09/apple-rises-from-near-bankruptcy-to-become-most-valuable-company)) · projev na Stanfordu 12. 6. 2005 · úmrtí 5. 10. 2011.

## Hlas (ElevenLabs)

Ve videu je ženský hlas, který Petr vybral v ElevenLabs (Eleven v3, `voice/take_elevenlabs.mp3`, 65,1 s). `voice/prep.py 1.05 .32` ho zrychlí o 5 % a zkrátí pauzy na 0,32 s, takže výsledek má 59,9 s a 25 segmentů. `voice/map.json` určuje, kterým segmentem začíná každá věta. Věta s11 má dva segmenty. Přepis Whisperem odpovídá scénáři. Původní 4 verze s mužským hlasem „Shoshi“ jsou ve flow [hULuH2PcQAiceVjYSF85](https://elevenlabs.io/app/flows/hULuH2PcQAiceVjYSF85). Jména jsou v textu pro hlas kvůli výslovnosti přepsaná foneticky:

```
[serious] Ve třiceti ho vyhodili z firmy, kterou sám založil. [pause] Stív Džobs.
[storytelling] Z vysoké odešel po jednom semestru. Dál ale chodil na kurz kaligrafie. Bez něj by prý mekintoš nikdy neměl krásná písma.
V roce devatenáct set sedmdesát šest založil se Stívem Vozniakem v garáži Ejpl. Za deset let to byla firma za dvě miliardy dolarů. [pause] A pak ho vyhodili.
[determined] Nevzdal to. Založil Nekst a koupil malou firmu jménem Piksar. Ta pak natočila Toj Stóry… první celovečerák celý z počítače.
[serious] V roce devatenáct set devadesát sedm se vrátil do Ejplu na pokraji bankrotu. Majkl Dell tehdy řekl, že by ho zavřel a peníze vrátil akcionářům.
[building up] Pak přišel ajmek. Ajpod. Ajfoun.
V srpnu dva tisíce jedenáct byl Ejpl nejhodnotnější firmou na světě.
[softly] O dva měsíce později Stív Džobs zemřel.
[warmly] O vyhazovu řekl, že to bylo to nejlepší, co se mu mohlo stát.
[slowly] Stay hungry. Stay foolish.
[casual] Koho chceš v dalším díle? Gejtse, Vozniaka, nebo Maska? Napiš to do komentářů.
```

## Fotky a obrázky

| Soubor v `photos/src/` | Zdroj | Autor, licence |
|---|---|---|
| `jobs_1984.*` | Petr (nahraná fotka) | Norman Seeff, 1984. **Není volně licencovaná.** Hrozí nárok nebo stažení videa. Bezpečná náhrada: [Bernard Gotfryd, leden 1984](https://commons.wikimedia.org/wiki/File:Steve_Jobs_and_Macintosh_computer,_January_1984,_by_Bernard_Gotfryd_-_edited.jpg) (Library of Congress, bez omezení). Stačí ji uložit jako `jobs_1984.*` a spustit `photos/retro.py`. |
| `apple_logo_1977.*` | Petr (nahraný obrázek) | Duhové logo Applu (1977–1998), ochranná známka Apple. Použité jen v historických scénách (1985, 1997) a nepřekreslené. |
| `jobs_2010.*` | File:Steve_Jobs_Headshot_2010-CROP_(cropped_2).jpg | Matthew Yohe, CC BY-SA 3.0 |
| `jobs_gates.*` | File:Steve_Jobs_and_Bill_Gates_(522695099).jpg | Joi Ito, CC BY 2.0 |
| `apple1.*` | File:Apple_I_Computer.jpg | Ed Uthman, CC BY-SA 2.0 |
| `nextcube.*` | File:NeXTcube.jpg | Rama, CC BY-SA 2.0 FR |

Originály `jobs_1984.*` a `apple_logo_1977.*` kvůli licenci nejsou ve veřejném repu (`.gitignore`). V repu jsou jen odvozené 1bit verze potřebné k renderu.

`photos/process.py` udělá rastr (`*_ht.png`) a černobílou verzi (`*_bw.png`) a pomocí rembg vyřízne lidi a předměty z pozadí. `photos/retro.py` z toho udělá 1bit verze s Atkinsonovým ditheringem:
- `j84_win.png` (okno v úvodu),
- `j84_cut.png` (výřez se samolepkovým okrajem, zároveň obálka),
- `jobsgates_1b.png`, `jobs_1b.png`,
- mozaiky `jobs_mos_*.png` (fotka se „načítá“ u smrti),
- `logo.png`.

Písma: Instrument Serif, Anton, Inter Tight, JetBrains Mono, Jersey 10 (okna a tlačítka) a VT323 (terminálové popisky). Všechna mají licenci OFL a jsou v `engine/fonts`.

## Výroba

1. `voice/prep.py 1.05 .32`: zrychlí hlas a zkrátí pauzy → `voice/voice.wav` + `segments.json`.
2. `voice/timeline.py`: časy vět a titulků → `timeline.js` + `timeline.json`.
3. `python3 -I photos/process.py` a `python3 -I photos/retro.py`: zpracování fotek.
4. `python3 export_ev.py`: zvukové události z animací (`window.EV`) → `fx.json`.
5. Render:
   - obraz: `engine/render.py video promo/postavili-to-01-jobs/reel.html raw.mp4`,
   - zvuk: `python3 sfx.py audio.wav` (−14 LUFS, true peak pod −1 dBFS),
   - spojení: `engine/finalize.sh`. Kvůli limitu GitHubu se video překóduje na CRF 27.

Zdroje: [Stanford – projev Steva Jobse 2005](https://news.stanford.edu/stories/2005/06/youve-got-find-love-jobs-says) · [Wikipedia – Steve Jobs](https://en.wikipedia.org/wiki/Steve_Jobs) · [Bloomberg 9. 8. 2011](https://www.bloomberg.com/news/articles/2011-08-09/apple-rises-from-near-bankruptcy-to-become-most-valuable-company) · [Cult of Mac – Michael Dell 1997](https://www.cultofmac.com/apple-history/michael-dell-quote-about-apple)
