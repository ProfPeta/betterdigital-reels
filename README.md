# Better Digital: výroba videí

Krátká videa a carousely generované kódem pro [Instagram](https://www.instagram.com/betterdigital.cz/), [TikTok](https://www.tiktok.com/@betterdigital.cz) a Facebook. Bez natáčení: HTML animace vykreslená po snímcích, syntetizovaný zvuk, hlas z ElevenLabs.

**Claude: začni v `RUNBOOK.md`.**

| Složka | Obsah |
|---|---|
| `engine/make.py` | jeden příkaz na celou výrobu |
| `engine/story/` | sdílený vzhled a engine scén |
| `engine/sfxlib.py` | sdílené nástroje, efekty, styly hudby, mix |
| `engine/spec.json` | jednotný technický formát |
| `engine/carousel/` | carousel do 1080×1350 a 1080×1920 z jednoho souboru |
| `videos/_template/` | šablona nového dílu |
| `videos/<díl>/` | zdroje dílu, výstupy vznikají v `build/` a do gitu nejdou |
| `archive/` | starší díly a ukončená série |

Hlavní větev neobsahuje videa. Hotové video jde před plánováním do větve `media` (`make.py push`), odkud si ho Metricool stáhne a uloží k sobě. Fotky bez ověřené licence v repu nejsou.
