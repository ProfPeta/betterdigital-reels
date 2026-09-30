# „ZASTAV VIDEO“ (TikTok, 15 s)

Pause challenge: karty s firemní rutinou se střídají 7,5× za sekundu (tvrdé střihy, každý snímek je čitelný i po pauze). Mezi nimi jsou schované karty: jackpot „Celý pátek volno“ (2× plus na konci), „Ranní káva“ a „Tvůj šéf“. Jackpot má v rytmu vlastní cinknutí.

- `reel.html`: animace pro `engine/render.py` (540×960, 30 fps).
- `schedule.json`: pořadí a časy karet exportované z `reel.html` (`window.SCHED`), podle nich `sfx.py` klade tiky.
- `sfx.py`: hudba a zvuky, 112,5 BPM (šestnáctina = 4 snímky = 1 karta); konec navazuje na začátek kvůli smyčce.
- `post.json`: popisek a první komentář.

Výroba: `python3 engine/render.py video promo/zastav-video/reel.html raw.mp4`, `python3 promo/zastav-video/sfx.py a.wav`, `bash engine/finalize.sh raw.mp4 a.wav video.mp4`.
