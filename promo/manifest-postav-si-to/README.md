# „Postav si to.“ – manifest Better Digital (TikTok/Reels, 42,6 s)

Česká verze formátu z manifestu Builder Cult: nejlepší zakladatelé byli naštvaní → příběhy → „Dost. Postavím si to sám.“ → pivot značky → „můžeš to postavit teď“. Kinetická typografie s tvrdými střihy na doby (100 BPM, doba 0,6 s), bez hlasu. Text je časovaný tak, aby se dal přečíst i bez zvuku.

## Scénář (co je na obrazovce)

| Čas | Text | Obraz |
|---|---|---|
| 0,0 | Nejlepší zakladatelé světa / mají jedno společné: | papírová koláž, „Better Digital uvádí“ |
| 2,4 | Byli sakra **NAŠTVANÍ.** | černá, úder, glitch, ozvěny slova |
| 4,2 | Příběh 1/3: **Melanie Perkins** učila spolužáky grafické programy. Byly složité a drahé. Tak udělala vlastní: **Canva** (2013) | přeplácaný grafický program, „Zkušební verze vypršela“ |
| 8,4 | Příběh 2/3: **Tobi Lütke** chtěl prodávat snowboardy online. Žádný e-shopový systém mu nevyhovoval. Tak si napsal vlastní: **Shopify** (2006) | snowboard, kaskáda chybových hlášek |
| 12,6 | Příběh 3/3 🇨🇿: **Richard Valtr** ve 14 letech v rodinném hotelu ručně pároval účtenky. V 1 ráno. Každou noc. Dvě hodiny. Tak postavil vlastní systém: **Mews** (český jednorožec, 2,5 mld. $) | noc, hodiny 01:00 → 03:00, hromada účtenek |
| 18,6 | Skvělé produkty vznikají, když tě něco štve tak dlouho, až řekneš: **DOST.** Postavím si to sám. | papír, počítadlo dnů; na „DOST.“ ticho a úder |
| 25,2 | Celou dobu stavíme weby a AI automatizace pro firmy. Ale upřímně? Chceme pomoct postavit **ty další.** | diagram Web → Formulář → AI → E-mail/Faktura/CRM; seznam Canva / Shopify / Mews / ▍ |
| 30,0 | Je jedno, jestli jsi kadeřnice, účetní nebo kuchař. Nemusíš umět ~~programovat~~. | rychlé střihy s emoji, přeškrtnutý kód |
| 33,6 | Když rozumíš problému a věříš, že to jde líp, můžeš si to postavit. **TEĎ.** | ukazatel „Stavím… 100 %“, drop |
| 38,4 | Co tě v práci nejvíc štve? Napiš to do komentářů 👇 | psaní komentáře „přepisování faktur do Excelu 😤“, podpis Uzel + Better Digital |

## Soubory

- `reel.html`: animace pro `engine/render.py` (540×960, 30 fps). Scény jsou v poli `S` (id, pozadí, začátek, konec), obsah v `P`, zvláštní pohyby v `AN`. Text drží sloupec x 74–466, y 130–740. Dekorace (koláž, okna programů, účtenky) smí přesahovat.
- `sfx.py`: hudba a zvuky syntetizované v numpy, časy stejné jako `S` v `reel.html`. Temná část v a moll s trap rytmem, UI zvuky (klikání myši, chybová hlášení, tiskárna účtenek, hodiny). Na „DOST.“ hudba ztichne a zůstane jen úder. Pak světlá část (F–G–Am) s gradací a dropem v C dur na „TEĎ.“. Mix je laděný pro reproduktory telefonu: méně subbasů, víc středů. Limiter s předstihem dává ve finálním videu −14,8 LUFS a true peak −1,4 dBFS.
- `video.mp4`: finální video (H.264 + AAC, faststart, bez edit listů). Kvůli zrnu by render s CRF 18 měl 92 MB, proto je přeenkódovaný x264 `-preset slow -crf 24 -bf 0` na 45,6 MB (SSIM 0,984 vůči CRF 18, okem bez rozdílu), aby se vešel pod limit GitHubu. `cover.jpg`: obálka (snímek 0,4 s).
- `post.json`: popisek, první komentář se zdroji a doporučená nastavení.

## Zdroje

- Canva: [Guy Kawasaki – Melanie Perkins (Remarkable People)](https://guykawasaki.com/melanie-perkins-canva-ceo/). Doučovala spolužáky grafické programy na University of Western Australia, „far too complex and expensive“. Canva vznikla v roce 2013.
- Shopify: [Wikipedia – Shopify, History](https://en.wikipedia.org/wiki/Shopify). V roce 2004 vznikl Snowdevil (snowboardy online). Lütke nebyl spokojený s existujícími e-commerce produkty, a protože byl programátor, napsal si vlastní. Jako Shopify spuštěno v červnu 2006.
- Mews: [Fortune, 27. 5. 2026](https://fortune.com/2026/05/27/founder-hotelier-mews-richard-valtr-2-5-billion-unicorn). Ve 14 letech o prázdninách v rodinném hotelu v Praze v 1 ráno ručně pároval platby kartou s účty hostů, zhruba 2 hodiny každou noc. Nápad přišel v roce 2012. V lednu 2026 série D 300 mil. $ při ocenění 2,5 mld. $.

## Hlasová verze (volitelně)

Reference stojí na hlase vypravěče. Až bude hlas, přečasuju scény podle něj: posunou se časy v `S` a v `sfx.py` a hudba ustoupí pod hlas. Nejlíp funguje Petrův vlastní hlas (zakladatel mluví za značku). Druhá možnost je ElevenLabs, model Eleven v3, hluboký mužský hlas, který umí česky. Text do ElevenLabs:

```
[confident, calm documentary narrator] Nejlepší zakladatelé světa mají jedno společné. [short pause] Byli sakra naštvaní.
[storytelling] Melanie Perkins učila spolužáky grafické programy. Byly složité a drahé. Tak udělala vlastní. Canva.
Tobi Lütke chtěl prodávat snowboardy online. Žádný e-shopový systém mu nevyhovoval. Tak si napsal vlastní. Shopify.
Richard Valtr ve čtrnácti letech v rodinném hotelu ručně pároval účtenky. V jednu ráno. Každou noc. Dvě hodiny. Tak postavil vlastní systém. Mews.
[slower, intense] Skvělé produkty vznikají, když tě něco štve tak dlouho, až řekneš: [pause] Dost. [pause] Postavím si to sám.
[warm] Celou dobu stavíme weby a AI automatizace pro firmy. Ale upřímně? Chceme pomoct postavit ty další.
Je jedno, jestli jsi kadeřnice, účetní nebo kuchař. Nemusíš umět programovat.
[building up] Když rozumíš problému a věříš, že to jde líp, můžeš si to postavit. [emphatic] Teď.
[casual] Co tě v práci nejvíc štve? Napiš to do komentářů.
```
