"""POSTAVILI TO #03 – Jensen Huang / Nvidia. Věty hlasu a titulky po kouscích; *hvězdičky* = zvýraznění.
Zdroje faktů: README.md."""
SENT = [
    ('s1', ['Tenhle kluk', 'v *devíti* letech', 'každý den drhnul', '*záchody.*']),
    ('s2', ['Rodiče ho poslali', 'z *Tchaj-wanu*', 'do *Ameriky.*']),
    ('s3', ['Strýc ho omylem', 'zapsal do *polepšovny*', 'v Kentucky.']),
    ('s4', ['Byl *nejmladší,*', 'tak dostal *záchody.*']),
    ('s5', ['Jako teenager', 'myl *nádobí*', 'v Denny\'s.']),
    ('s6', ['A právě u stolu', 'v Denny\'s', 'v roce *1993*', 'vymyslel', 'se dvěma kamarády', '*firmu.*']),
    ('s7', ['*Nvidia.*']),
    ('s8', ['První čip', 'byla *katastrofa.*']),
    ('s9', ['Vsadili na', '*špatnou* technologii,', 'zakázku pro Segu', '*nezvládli*']),
    ('s10', ['a peníze měli', 'na *30 dní.*']),
    ('s11', ['Huang letěl', 'do *Japonska*', 'a šéfovi Segy', 'na rovinu řekl:']),
    ('s12', ['*„Selhali jsme.“*']),
    ('s13', ['A stejně ho požádal,', 'ať je *zaplatí.*']),
    ('s14', ['Sega jim dala', '*5 milionů dolarů.*']),
    ('s15', ['Propustil víc', 'než *polovinu* lidí.']),
    ('s16', ['Ze *100*', 'zůstalo *40.*']),
    ('s17', ['Všechno vsadil', 'na *jeden čip.*']),
    ('s18', ['A ten *zabral.*']),
    ('s19', ['Dnes Nvidia pohání', 'skoro celou', '*umělou inteligenci.*']),
    ('s20', ['Jako první firma', 'v historii', 'překonala hodnotu', '*5 bilionů dolarů.*']),
    ('s21', ['A přesto říká,', 'že kdyby věděl,', 'kolik to bude *bolet,*', 'firmu by znovu', '*nezaložil.*']),
    ('s22', ['Ty bys do toho', '*šel?*']),
]
VOWELS = set('aáeéěiíoóuúůyýAÁEÉĚIÍOÓUÚŮYÝ')
def syllables(text):
    t = text.replace('*', '')
    for k, v in {'1993': 'devatenáctsetdevadesáttři', '30': 'třicet', '5 milionů': 'pětmilionů', '5 bilionů': 'pětbilionů',
                 '100': 'sta', '40': 'čtyřicet', "Denny's": 'denys', 'Nvidia': 'envidija', 'Huang': 'chuang',
                 'Kentucky': 'kentaky', 'teenager': 'týnejdžr'}.items():
        t = t.replace(k, v)
    n, prev = 0, False
    for ch in t:
        v = ch in VOWELS
        if v and not prev: n += 1
        prev = v
    return max(1, n)
