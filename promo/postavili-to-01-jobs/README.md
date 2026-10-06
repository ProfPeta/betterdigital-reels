# POSTAVILI TO #01 – Steve Jobs (TikTok/Reels, 62,2 s)

První díl série faktických příběhů lidí, kteří postavili tech (další na řadě: Gates, Wozniak, Ballmer, Musk…). Žádný prodej, cílem jsou dosahy, komunita a značka. Na konci je jen malý podpis Better Digital a otázka „Koho chceš v dalším díle?“.

**Styl:** záměrně vybočuje z čistého Better Digital. Novinový papír, rastrované fotky, červený akcent, Instrument Serif + Anton, razítka, VHS glitch na krizi 1997. Titulky běží po kouscích podle hlasu. Nahoře je časová osa 1955–2011 s rokem scény.

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

## Fotky (Wikimedia Commons, volné licence)

| Soubor v `photos/src/` | Zdroj | Autor, licence |
|---|---|---|
| `jobs_2010.*` | File:Steve_Jobs_Headshot_2010-CROP_(cropped_2).jpg | Matthew Yohe, CC BY-SA 3.0 |
| `jobs_gates.*` | File:Steve_Jobs_and_Bill_Gates_(522695099).jpg | Joi Ito, CC BY 2.0 |
| `apple1.*` | File:Apple_I_Computer.jpg | Ed Uthman, CC BY-SA 2.0 |
| `nextcube.*` | File:NeXTcube.jpg | Rama, CC BY-SA 2.0 FR |

`photos/process.py` z nich udělá rastr (`*_ht.png`) a černobílou verzi (`*_bw.png`). Lidi a předměty vyřízne z pozadí pomocí rembg. Dokud zdroj chybí, použije zástupný obrázek.

## Výroba

1. `voice/prep.py`: zrychlí hlas a zkrátí pauzy, vznikne `voice/voice.wav` + `segments.json`.
2. `voice/timeline.py`: časy vět a titulků, vznikne `timeline.js` + `timeline.json`. Bez hlasu vzniknou prozatímní časy podle slabik.
3. `photos/process.py`: zpracuje fotky.
4. Render: `engine/render.py video promo/postavili-to-01-jobs/reel.html raw.mp4`, zvuk `python3 sfx.py audio.wav`, pak `engine/finalize.sh`.

Zdroje: [Stanford – projev Steva Jobse 2005](https://news.stanford.edu/stories/2005/06/youve-got-find-love-jobs-says) · [Wikipedia – Steve Jobs](https://en.wikipedia.org/wiki/Steve_Jobs) · [Bloomberg 9. 8. 2011](https://www.bloomberg.com/news/articles/2011-08-09/apple-rises-from-near-bankruptcy-to-become-most-valuable-company) · [Cult of Mac – Michael Dell 1997](https://www.cultofmac.com/apple-history/michael-dell-quote-about-apple)
