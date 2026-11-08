"""POZNÁŠ AI? Jídlo #1. Věty hlasu a titulky po kouscích; *hvězdičky* = zvýraznění."""
import re
SENT = [
    ('s1', ['Jedna z těch fotek', 'je *skutečná.*']),
    ('s2', ['Druhou uvařila', '*umělá inteligence.*']),
    ('s3', ['*Poznáš to?*']),
    ('s4', ['První kolo.', 'Svíčková.', '*A,* nebo *B?*']),
    ('s5', ['Druhé kolo.', 'Smažák.', '*A,* nebo *B?*']),
    ('s6', ['A poslední.', 'Vepřo knedlo zelo.', '*A,* nebo *B?*']),
    ('s7', ['Napiš svoje *tři tipy*', 'do komentářů.']),
    ('s8', ['Teprve pak', 'se dívej *dál.*']),
    ('s9', ['*Odpovědi.*']),
    ('s10', ['Svíčková.', 'Pravá je *A.*']),
    ('s11', ['Smažák.', 'Pravá je *B.*']),
    ('s12', ['A vepřo knedlo zelo?']),
    ('s13', ['Obě fotky jsou', 'od *umělé inteligence.*']),
    ('s14', ['Kolik jsi *dal?*']),
    ('s15', ['A pošli to *mámě,*', 'ať se taky zapotí.']),
]
VOWELS = set('aáeéěiíoóuúůyýAÁEÉĚIÍOÓUÚŮYÝ')
def syllables(text):
    t = re.sub(r'\bB\b', 'bé', text.replace('*', ''))
    n, prev = 0, False
    for ch in t:
        v = ch in VOWELS
        if v and not prev: n += 1
        prev = v
    return max(1, n)
