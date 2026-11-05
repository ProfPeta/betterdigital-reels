# POSTAVILI TO #03 – Jensen Huang / Nvidia (TikTok/Reels, ~64 s)

Třetí globální díl série faktických příběhů lidí, kteří postavili tech. Bez prodeje, cíl je dosah, sdílení a komentáře. Na konci otázka „Šel bys do toho i ty?“ (ANO / NE).

**Styl:** kostra Better Digital (žlutý odznak, titulky, Uzel v závěru) a vlastní „Nvidia“ vrstva: černá, zelená `#76B900`, technická mřížka, HUD rohy, šikmé štítky, mono popisky. Krizové scény (NV1, 30 dní) jsou v červené. Nahoře časová osa 1978–2025.

Hudba: 96 BPM, tmavá elektronika v A moll (synth puls, pad, groove), efekty jen jemně (FX sběrnice −40 %), hlas ~12 dB nad hudbou. Integrovaná hlasitost −14,2 LUFS.

## Scénář (hlas) a fakta

| Věta | Ověření |
|---|---|
| V devíti letech každý den drhnul záchody | Jako nejmladší v Oneida Baptist Institute uklízel záchody ([Wikipedia](https://en.wikipedia.org/wiki/Jensen_Huang), [Britannica](https://www.britannica.com/biography/Jensen-Huang), [Fortune 2025](https://www.fortune.com/2025/12/05/jensen-huang-nine-year-old-janitor-before-nvidia-joe-rogan-podcast)). |
| Rodiče ho poslali z Tchaj-wanu do USA, strýc ho omylem zapsal do polepšovny v Kentucky | Strýc myslel, že jde o prestižní internát; byla to náboženská škola pro „problémovou“ mládež (Wikipedia, Britannica). |
| Jako teenager myl nádobí v Denny's | Myčka nádobí, pomocník a číšník, 1978–1983 (Wikipedia, [Fortune 2024](https://fortune.com/article/how-nvidias-billionaire-ceo-went-from-dennys-dishwasher-to-leading-a-company-with-a-2-9-trillion-market-cap)). |
| U stolu v Denny's v roce 1993 vymyslel se dvěma kamarády firmu | S Chrisem Malachowskym a Curtisem Priemem, Denny's ve východním San Jose (Fortune, Nvidia). Založeno 5. 4. 1993. |
| První čip katastrofa, špatná technologie, zakázku pro Segu nezvládli | NV1 sázel na čtyřúhelníky místo trojúhelníků; čip pro Segu nedodali ([Tom's Hardware](https://www.3dtested.com/tech-industry/nvidia-nearly-went-out-of-business-in-1996-trying-to-make-segas-dreamcast-gpu-instead-sega-americas-ceo-offered-the-company-a-dollar5-million-lifeline)). |
| Peníze na 30 dní | Neoficiální motto „naše firma je 30 dní od krachu“ ([Wikipedia – Nvidia](https://en.wikipedia.org/wiki/Nvidia)). |
| Letěl do Japonska, šéfovi Segy řekl „selhali jsme“ a požádal o zaplacení; Sega dala 5 milionů dolarů | Shoichiro Irimajiri; Huang navrhl převést dlužné peníze na investici 5 mil. $ ([Webull/Benzinga](https://www.webull.com.au/news-detail/15235628473525248), Tom's Hardware). |
| Propustil víc než polovinu lidí, ze 100 zůstalo 40 | 1996, ze 100 na 40 zaměstnanců (Wikipedia – Nvidia). |
| Všechno vsadil na jeden čip a ten zabral | RIVA 128, 1997 (Wikipedia – Nvidia). |
| První firma v historii nad 5 bilionů dolarů | Říjen 2025 ([Motley Fool / Nasdaq](https://www.nasdaq.com/articles/prediction-nvidia-will-be-worth-6-trillion-end-2026)). |
| Kdyby věděl, kolik to bude bolet, firmu by znovu nezaložil | [Yahoo Finance / Business Insider](https://finance.yahoo.com/markets/stocks/articles/jensen-huang-says-wouldnt-start-111413161.html). Ve videu jako parafráze, ne citát. |

## Hlas (ElevenLabs)

Anet (Youthful and Lively), Eleven v4. Nahrávku vygeneroval Petr (`voice/take_elevenlabs.mp3`, 65,6 s). `voice/prep.py 1.0 .30` bez zrychlení, jen zkrácení pauz: 62,1 s, 28 segmentů. Whisper po segmentech i výsledný mix sedí se scénářem.

## Fotky

Nahrál Petr (vypadají jako Wikimedia Commons), licence neověřené, nejsou ve veřejném repu (`.gitignore`): portrét Huanga, Oneida Baptist Institute, cedule Denny's (japonská, označeno „ILUSTRAČNÍ FOTO“), Sega Saturn (označeno „ILUSTRAČNÍ FOTO“, zakázka byla na čip pro další konzoli), čip RIVA 128, sídlo Endeavor. Zpracování: `python3 -I photos/process.py`.

## Výroba

`voice/prep.py` → `seg_asr.py` → `script.py` + `voice/map.json` → `voice/timeline.py` → `reel.html` → `export_ev.py` → `sfx.py audio.wav 1.42` → `engine/render.py video` → `engine/finalize.sh` → encode CRF 27.
