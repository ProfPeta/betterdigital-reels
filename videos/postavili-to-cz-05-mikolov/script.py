"""POSTAVILI TO · Česká edice #5 – Tomáš Mikolov. Věty hlasu a titulky po kouscích; *hvězdičky* = zvýraznění.
Zdroje faktů: README.md."""
SENT = [
    ('s1', ['Osobně ho přetahoval', 'Mark *Zuckerberg.*']),
    ('s2', ['Plat v *milionech*', 'dolarů ročně.']),
    ('s3', ['V Česku pak', 'za *pět let* nesehnal', 'jediný normální *grant.*']),
    ('s4', ['*Tomáš Mikolov*', 'ze Šumperka.']),
    ('s5', ['V roce *2012*', 'nastupuje do *Googlu*', 'a přes Vánoce', 'napíše článek,', 'jak převést', '*slova na čísla.*']),
    ('s6', ['Král,', 'minus muž,', 'plus žena.']),
    ('s7', ['Vyjde *královna.*']),
    ('s8', ['Konference článek', '*zamítne.*']),
    ('s9', ['Přesto se z toho stane', '*word2vec,*', 'jedna z nejcitovanějších', 'prací v oboru.']),
    ('s10', ['*ChatGPT* nevymyslel.']),
    ('s11', ['Ale stojí', 'na těchto *principech.*']),
    ('s12', ['V roce *2020*', 'se vrací z Ameriky', 'na *ČVUT.*']),
    ('s13', ['Chce tu postavit', '*vlastní tým.*']),
    ('s14', ['Z veřejných peněz', 'má po pěti letech,', 'jeho slovy,', 'jednu velkou *nulu.*']),
    ('s15', ['Žádost', 'do *Singapuru?*']),
    ('s16', ['Pár hodin práce', 'a zhruba', '*tři miliony dolarů.*']),
    ('s17', ['V roce *2025* odchází', 'a zakládá startup', '*BottleCap.*']),
    ('s18', ['Investuje i', 'zakladatel *Seznamu.*']),
    ('s19', ['A letos 28. října', 'mu prezident předá', 'medaili *Za zásluhy.*']),
    ('s20', ['Takže peníze', 'na tým *ne.*']),
    ('s21', ['Medaile *ano.*']),
    ('s22', ['Měl se vracet', 'do Česka?']),
    ('s23', ['Napiš *ano,*', 'nebo *ne.*']),
]
VOWELS = set('aáeéěiíoóuúůyýAÁEÉĚIÍOÓUÚŮYÝ')
def syllables(text):
    t = text.replace('*', '')
    for k, v in {'2012': 'dvatisícedvanáct', '2020': 'dvatisícedvacet', '2025': 'dvatisícedvacetpět', '28.': 'osmadvacátého',
                 'Zuckerberg': 'cukrberg', 'Googlu': 'gúglu', 'word2vec': 'vordtuvek', 'ChatGPT': 'četdžípítý', 'ČVUT': 'čévéúté',
                 'BottleCap': 'botlkep'}.items():
        t = t.replace(k, v)
    n, prev = 0, False
    for ch in t:
        v = ch in VOWELS
        if v and not prev: n += 1
        prev = v
    return max(1, n)
