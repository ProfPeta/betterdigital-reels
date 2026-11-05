"""Postavili to #01 – Steve Jobs. Scénář: věty hlasu (VO) a titulky po kouscích.
Text pro ElevenLabs je v README (fonetický přepis jmen). Tady je pravopisná verze pro titulky.
Kousek s *hvězdičkami* = zvýrazněné slovo. Zdroje faktů: README.md."""

SENT = [
    ('s1', ['Ve třiceti', 'ho *vyhodili*', 'z firmy,', 'kterou sám', 'založil.']),
    ('s2', ['*Steve Jobs.*']),
    ('s3', ['Z vysoké', 'odešel', 'po jednom', 'semestru.']),
    ('s4', ['Dál ale', 'chodil na', 'kurz *kaligrafie.*']),
    ('s5', ['Bez něj', 'by prý Mac', 'nikdy neměl', 'krásná *písma.*']),
    ('s6', ['V roce *1976*', 'založil', 'se Stevem Wozniakem', 'v garáži', '*Apple.*']),
    ('s7', ['Za deset let', 'to byla firma', 'za *dvě miliardy*', 'dolarů.']),
    ('s8', ['A pak', 'ho *vyhodili.*']),
    ('s9', ['*Nevzdal to.*']),
    ('s10', ['Založil *NeXT*', 'a koupil', 'malou firmu', 'jménem *Pixar.*']),
    ('s11', ['Ta pak natočila', '*Toy Story…*', 'první celovečerák', 'celý z počítače.']),
    ('s12', ['V roce *1997*', 'se vrátil', 'do Applu', 'na pokraji', '*bankrotu.*']),
    ('s13', ['Michael Dell', 'tehdy řekl,', 'že by ho *zavřel*', 'a peníze vrátil', 'akcionářům.']),
    ('s14', ['Pak přišel', '*iMac.*']),
    ('s15', ['*iPod.*']),
    ('s16', ['*iPhone.*']),
    ('s17', ['V srpnu 2011', 'byl Apple', '*nejhodnotnější*', 'firmou na světě.']),
    ('s18', ['O dva měsíce', 'později', 'Steve Jobs', '*zemřel.*']),
    ('s19', ['O vyhazovu', 'řekl, že to bylo', 'to *nejlepší,*', 'co se mu', 'mohlo stát.']),
    ('s20', ['*Stay hungry.*']),
    ('s21', ['*Stay foolish.*']),
    ('s22', ['Koho chceš', 'v dalším díle?']),
    ('s23', ['*Gatese,*', '*Wozniaka,*', 'nebo *Muska?*']),
    ('s24', ['Napiš to', 'do *komentářů.*']),
]

VOWELS = set('aáeéěiíoóuúůyýAÁEÉĚIÍOÓUÚŮYÝ')


def syllables(text):
    """Hrubý odhad slabik (české samohlásky + slabikotvorné r/l mezi souhláskami, číslice jako čtená slova)."""
    t = text.replace('*', '')
    for k, v in {'1976': 'devatenáctsetsedmdesátšest', '1997': 'devatenáctsetdevadesátsedm',
                 '2011': 'dvatisícejedenáct', 'Jobs': 'Džobs', 'Steve': 'Stív', 'iPhone': 'ajfoun',
                 'iPod': 'ajpod', 'iMac': 'ajmek', 'Mac': 'mek', 'NeXT': 'nekst', 'Toy Story': 'tojstóry',
                 'Apple': 'ejpl', 'Applu': 'ejplu', 'hungry': 'hangry', 'foolish': 'fúliš'}.items():
        t = t.replace(k, v)
    n, prev = 0, False
    for ch in t:
        v = ch in VOWELS
        if v and not prev: n += 1
        prev = v
    return max(1, n)
