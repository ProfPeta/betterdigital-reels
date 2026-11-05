"""POSTAVILI TO · Česká edice #4 – Rohlík (Tomáš Čupr). Věty hlasu a titulky po kouscích; *hvězdičky* = zvýraznění.
Zdroje faktů: README.md."""
SENT = [
    ('s1', ['Ve *dvanácti*', 'prodával spolužákům', 'rohlíky plněné', '*čokoládou.*']),
    ('s2', ['Dnes má firmu,', 'která se jmenuje…', '*Rohlík.*']),
    ('s3', ['A stojí skoro', '*dvě miliardy dolarů.*']),
    ('s4', ['*Tomáš Čupr.*']),
    ('s5', ['První peníze', 'si vydělal hraním', '*Counter-Striku.*']),
    ('s6', ['Se svým týmem', 'byl *dvakrát*', 'mistrem republiky.']),
    ('s7', ['V roce *2005*', 'odjíždí do *Anglie.*']),
    ('s8', ['Začíná jako', '*pomocník* v tiskárně…', 'a končí jako', '*spolumajitel*', 'marketingové agentury.']),
    ('s9', ['Vrátí se domů']),
    ('s10', ['a v roce *2010*', 'spustí *Slevomat.*']),
    ('s11', ['*Tři dny*', 'po spuštění', 'za ním přijde investor', 'a koupí *49 %.*']),
    ('s12', ['O dva roky později', 'založí *DámeJídlo.*']),
    ('s13', ['Z obou firem', '*odejde.*']),
    ('s14', ['A pustí se', 'do projektu,', 'o kterém říká,', 'že je *na celý život.*']),
    ('s15', ['*Rohlík.*']),
    ('s16', ['V roce *2021* je z něj', 'první český *jednorožec.*']),
    ('s17', ['Firma za víc než', '*miliardu dolarů.*']),
    ('s18', ['Dnes vozí nákupy', 'v *pěti zemích.*']),
    ('s19', ['Včetně *Německa,*', 'kde se jmenuje *Knuspr.*']),
    ('s20', ['A celé to začalo…', '*rohlíkem s čokoládou.*']),
    ('s21', ['Nakupuješ', 'na *Rohlíku?*']),
    ('s22', ['Napiš *ANO,*', 'nebo *NE.*']),
]
VOWELS = set('aáeéěiíoóuúůyýAÁEÉĚIÍOÓUÚŮYÝ')
def syllables(text):
    t = text.replace('*', '')
    for k, v in {'2005': 'dvatisícepět', '2010': 'dvatisícedeset', '2021': 'dvatisícedvacetjedna', '49 %': 'čtyřicetdevětprocent',
                 'Counter-Striku': 'kaunterstrajku', 'Knuspr': 'knusper', 'ANO': 'ano', 'NE': 'ne'}.items():
        t = t.replace(k, v)
    n, prev = 0, False
    for ch in t:
        v = ch in VOWELS
        if v and not prev: n += 1
        prev = v
    return max(1, n)
