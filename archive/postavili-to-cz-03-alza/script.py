"""POSTAVILI TO · Česká edice #3 – Alza (Aleš Zavoral). Věty hlasu a titulky po kouscích; *hvězdičky* = zvýraznění.
Zdroje faktů: README.md."""
SENT = [
    ('s1', ['Tenhle český *miliardář*', 'nedává rozhovory', 'a skoro nikdo neví,', 'jak *vypadá.*']),
    ('s2', ['Jeho e-shop', 'ale zná *každý.*']),
    ('s3', ['*Aleš Zavoral.*']),
    ('s4', ['Jako kluk prodával', '*limonádu* a *vajgly,*', 'které po koncertech', 'našel pod *pódiem.*']),
    ('s5', ['První počítač', 'si koupil', 'za *2 990 korun.*']),
    ('s6', ['Vydělal si na něj', 'sběrem *jablek.*']),
    ('s7', ['V osmnácti', 'si udělá *živnosťák*', 'a prodává…', '*cukr.*']),
    ('s8', ['Z cukrovaru,', 'kde dělal jeho *táta.*']),
    ('s9', ['Pak rozebere počítač', 'a zjistí, že se dá', 'složit z *dílů.*']),
    ('s10', ['Začne je skládat', 'a prodávat', 'přímo z *koleje.*']),
    ('s11', ['Pokoj *710.*']),
    ('s12', ['První rok prodá', 'počítače', 'za *milion korun.*']),
    ('s13', ['Jeho první prodejna', 'v Holešovicích', 'nemá žádnou *reklamu,*']),
    ('s14', ['a přesto jsou před ní', 'takové *fronty,*', 'že si stěžuje', 'sousední *květinářka.*']),
    ('s15', ['Peníze nosí', 'v *krabici od bot.*']),
    ('s16', ['Pak přijde', 'zelený mimozemšťan', '*Alzák.*']),
    ('s17', ['Inspirovaný *Cartmanem*', 'ze South Parku.']),
    ('s18', ['Dnes má Alza', 'přes *60 miliard*', 'korun tržeb', 'a víc než', '*5 000 AlzaBoxů.*']),
    ('s19', ['Oficiálně ale patří', 'firmě z *Kypru.*']),
    ('s20', ['Zavoral svůj podíl', 'nikdy veřejně', '*nepotvrdil.*']),
    ('s21', ['Forbes ho přesto řadí', 'mezi dolarové', '*miliardáře.*']),
    ('s22', ['Od vajglů pod pódiem', 'k *miliardám.*']),
    ('s23', ['Kterou českou firmu', 'chceš *příště?*']),
    ('s24', ['Napiš to', 'do *komentářů.*']),
]
VOWELS = set('aáeéěiíoóuúůyýAÁEÉĚIÍOÓUÚŮYÝ')
def syllables(text):
    t = text.replace('*', '')
    for k, v in {'2 990': 'dvatisícedevětsetdevadesát', '710': 'sedmsetdeset', '60': 'šedesát', '5 000': 'pěttisíc',
                 'e-shop': 'íšop', 'Cartmanem': 'kártmenem', 'South Parku': 'sautparku', 'AlzaBoxů': 'alzaboxů', 'Forbes': 'forbs'}.items():
        t = t.replace(k, v)
    n, prev = 0, False
    for ch in t:
        v = ch in VOWELS
        if v and not prev: n += 1
        prev = v
    return max(1, n)
