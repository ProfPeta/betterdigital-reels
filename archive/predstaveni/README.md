# Představení Better Digital (45 s)

Filmové promo video firmy: chaos → logo → ukázky (web, automatizace, školení) → „Vy řeknete co. My to postavíme.“

- `intro.html` obsahuje animaci; `window.render(t)` vykreslí snímek v čase t, formát se řídí velikostí okna (540×960 = 9:16, 960×540 = 16:9).
- `sfx.py` syntetizuje hudbu a zvuky (`python3 sfx.py intro.wav`).
- `render.py` vykresluje snímky nebo video: `python3 render.py v|h stills|video intro.html <výstup> [časy]`.

Finální export: video bez B-snímků (`-bf 0`), AAC 128 kb/s 48 kHz, `-movflags +faststart -use_editlist 0`.
