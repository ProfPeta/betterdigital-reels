# POSTAVILI TO · Česká edice #5 – Tomáš Mikolov (TikTok/Reels, ~65 s)

Stav: naplánováno na 5. 11. 2026: TikTok 18:00, Instagram 18:05, Facebook 18:10 (`post.json`). Bez prodeje, cíl je dosah a komentáře.

**Styl:** černá, bílá, žlutá. Jemná hudba bez bicích v `sfx.py`, efekty potichu, hlas ~15 dB nad hudbou, −14 LUFS.

## Fakta

| Věta | Ověření |
|---|---|
| Osobně ho přetahoval Zuckerberg, plat v milionech dolarů ročně | Mikolovova slova: „Do Facebooku mě přetahoval osobně Mark Zuckerberg, plat jsem měl v milionech dolarů ročně“ ([CzechCrunch, 15. 5. 2025](https://cc.cz/do-facebooku-me-pretahoval-sam-zuckerberg-nenecham-se-tu-sikanovat-uredniky-rika-mikolov-o-ceske-vede/)). |
| Za pět let nesehnal jediný normální grant | Mikolovova slova: „Po pěti letech snahy nemám jediný normální grant“ ([CzechCrunch, 2025](https://cc.cz/za-pet-let-jsem-nesehnal-penize-pro-svuj-tym-zlobi-se-spickovy-ai-vedec-mikolov-a-dal-vypoved/)). |
| Ze Šumperka | Tamtéž. |
| 2012 Google, přes Vánoce článek | [Seznam Zprávy, 2021](https://www.seznamzpravy.cz/clanek/jeho-figl-v-usa-nakopl-vyvoj-strojoveho-uceni-proc-se-expert-vratil-176156). |
| Král − muž + žena = královna | [Seznam Zprávy](https://www.seznamzpravy.cz/clanek/domaci-zivot-v-cesku-komentar-cesta-od-montoven-k-laboratorim-v-cesku-vazne-hlasi-ai-vyzkumnik-268530). Ve videu označit jako zjednodušení. |
| Konference článek zamítla | Mikolov: „zrovna ten můj článek tehdy na konferenci zamítli“ (Seznam Zprávy, 2021). Workshop ICLR 2013 ho pak přijal. [arXiv 1301.3781](https://arxiv.org/abs/1301.3781). |
| Jedna z nejcitovanějších prací v oboru | Seznam Zprávy, 2021. Navazující článek má přes 40 000 citací ([CIIRC ČVUT](https://ellis.ciirc.cvut.cz/?p=5512)). To číslo se týká navazujícího článku, ne zamítnutého. |
| ChatGPT nevymyslel, ale stojí na těchto principech | CzechCrunch: moderní jazykové modely „staví na principech této techniky“ ([článek](https://cc.cz/chceme-prulom-v-umele-inteligenci-jaroslav-beck-da-do-noveho-startupu-s-tomasem-mikolovem-ctvrt-miliardy/)). |
| 2020 návrat na ČVUT | V CIIRC od března 2020 (CzechCrunch, 2025). |
| Z veřejných peněz „jedna velká nula“ | Mikolovova slova (CzechCrunch, 2025). |
| Singapur: pár hodin práce, zhruba 3 mil. $ | Mikolovova slova, žádost z listopadu 2024 (CzechCrunch, 15. 5. 2025). Není jasné, jestli peníze dál čerpá, proto říkáme jen „zhruba tři miliony“. |
| 2025 odchod, startup BottleCap | Konec března 2025, oznámení začátkem března (CzechCrunch, 2025). |
| Investuje zakladatel Seznamu | [CzechCrunch, 29. 1. 2026](https://cc.cz/jaroslav-beck-a-tomas-mikolov-ziskavaji-150-milionu-pro-svuj-ai-startup-investuje-do-nej-i-ivo-lukacovic/). |
| 28. 10. 2026 medaile Za zásluhy | Za zásluhy o stát v oblasti vědy a techniky ([CzechCrunch, 28. 10. 2026](https://cc.cz/detsky-hospic-umela-inteligence-i-boj-s-dezinformacemi-prezident-ocenil-vlckovy-mikolova-a-buryska/)). |

## Druhá strana sporu

V dohledaných článcích není vyjádření ministerstva školství. [Lupa, 23. 4. 2025](https://www.lupa.cz/clanky/otazniky-kolem-ceskych-grantu-nejen-na-vyzkum-ai-problemy-nema-jen-mikolov-naznacuji-zkusenosti-dalsich-vedcu/):
- Ředitel CIIRC Ondřej Velek podmínku 40% spolufinancování potvrzuje a nazývá ji likvidační.
- GA ČR nesouhlasí, že by příčina odchodů byla v grantovém financování.
- Někteří odborníci říkají, že žádosti mohly být přesnější a že průlom pochází ze starší práce.

Proto je ve videu „jeho slovy“. Do prvního komentáře patří věta o druhé straně a zdroje.

## Hlas

Anet (Youthful and Lively), Eleven v4, nahrávka od Petra 63,7 s. `voice/prep.py 1.0 .30` → 63,25 s, 29 segmentů. Whisper po segmentech sedí se scénářem. Prompt je ve `voice/prompt.txt`.

## Materiály

Fotky dodal Petr, licence neověřené, proto nejsou v repu (`.gitignore`).

| Soubor v `photos/src/` | Scéna |
|---|---|
| `zuckerberg.jpg` | háček |
| `mikolov_portret.jpg` | představení |
| `arxiv_1301_3781.jpg` | zamítnutý článek |
| `bottlecap_tym.jpg` | BottleCap, popisek „tým BottleCap AI“ je předpoklad, Petr ověří |
| `mikolov_medaile.jpg` | medaile, Pražský hrad |

Koláž čtyř oceněných není použitá, medaile z Hradu je silnější. Loga nejsou, názvy firem jsou jen text.
V `materials/` je skutečný kód word2vec z [tmikolov/word2vec](https://github.com/tmikolov/word2vec), licence Apache 2.0, ve videu s popiskem.

## Výroba

`python3 -I photos/process.py`, `python3 build.py`, `python3 voice/timeline.py`, `python3 export_ev.py`, `python3 sfx.py audio.wav 1.33`, `engine/render.py video`, `engine/finalize.sh`, překódování CRF 27.
