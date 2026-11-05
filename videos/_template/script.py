"""Scénář: věty hlasu a titulky po kouscích. *hvězdičky* = zvýraznění. Zdroje faktů patří do README.md."""
SENT = [
    ('s1', ['Háček:', 'konflikt nebo *výsledek.*']),
    ('s2', ['Kdo to je', 'a *proč* to zajímá lidi.']),
    ('s3', ['Hlavní *zvrat*', 'příběhu.']),
    ('s4', ['Pointa', 'na *jednu větu.*']),
    ('s5', ['Otázka', 'na *jedno slovo?*']),
]
# Čísla a cizí jména v titulcích se pro počet slabik přepíšou na výslovnost.
REPLACE = {}
VOWELS = set('aáeéěiíoóuúůyýAÁEÉĚIÍOÓUÚŮYÝ')
def syllables(text):
    t = text.replace('*', '')
    for k, v in REPLACE.items(): t = t.replace(k, v)
    n, prev = 0, False
    for ch in t:
        v = ch in VOWELS
        if v and not prev: n += 1
        prev = v
    return max(1, n)
