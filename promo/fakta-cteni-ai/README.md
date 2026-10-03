# „Tohle přečetla AI.“ (TikTok/Reels, 14,5 s, fakta bez natáčení)

Video vypadá jako nahrávka obrazovky mobilu: Poznámky v tmavém režimu a psaní na klávesnici. Jeden ověřený fakt a pointa.

- **Háček (od prvního snímku):** „11 000 000 000 000 slov. Tolik „přečetla“ jedna AI.“ + „Kolik let bys to četl ty? Tipni si 👇“ (výzva ke komentářům).
- **Výpočet:** Llama 3 od Mety se učila na víc než 15 bilionech tokenů ≈ 11 bilionech slov (1 token ≈ 0,75 slova). Průměrné tiché čtení je 238 slov za minutu. Při 8 hodinách denně a 5 dnech v týdnu (261 dní) je to zhruba 29,8 milionu slov za rok, tedy asi **377 000 let**.
- **Zvrat:** Homo sapiens je na Zemi asi 300 000 let, takže „musel bys začít číst dřív, než existoval člověk 🤯“. Pak „A to je jen jedna AI. 😅“ a výzva ke sdílení „Pošli to někomu, kdo pořád čte 📚“. Konec navazuje na začátek (smyčka).
- `reel.html`: animace pro `engine/render.py` (540×960, 30 fps). Psaní (TYPE) a počítadlo jsou čisté funkce času. Obsah je ve sloupci x 74–466, y 130–740, stavový řádek a klávesnice jsou jen dekorace na okrajích.
- `sfx.py`: lo-fi podkres 88 BPM, cvakání klávesnice přesně na psané znaky (stejný rozvrh a jitter jako v `reel.html`), tikání počítadla, cink, basový úder na zvrat. Úroveň −14 LUFS, true peak −3,7 dBFS.
- `post.json`: popisek, nastavení a doporučený čas.

Zdroje: [Meta – Llama 3 (2024)](https://ai.meta.com/blog/meta-llama-3/) · Brysbaert (2019), *How many words do we read per minute?*, Journal of Memory and Language · [Smithsonian Human Origins – Our species arose at least 300,000 years ago](https://humanorigins.si.edu/research/whats-hot-human-origins/our-species-arose-least-300000-years-ago).
