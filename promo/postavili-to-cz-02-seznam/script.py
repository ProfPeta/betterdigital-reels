"""POSTAVILI TO · Česká edice #2 – Seznam (Ivo Lukačovič). Věty hlasu a titulky po kouscích; *hvězdičky* = zvýraznění.
Zdroje faktů: README.md."""
SENT = [
    ('s1', ['Dva roky', 'před *Googlem*', 'spustil student', 'z ložnice rodičů', 'český *vyhledávač.*']),
    ('s2', ['A Google ho tady', 'pak roky', 'nedokázal *porazit.*']),
    ('s3', ['*Ivo Lukačovič.*']),
    ('s4', ['Rok *1996.*']),
    ('s5', ['Podle amerického *Yahoo*', 'programuje katalog', 'českých webů', 'a pojmenuje ho *Seznam.*']),
    ('s6', ['Startovní *kapitál?*']),
    ('s7', ['*80 000 korun.*']),
    ('s8', ['Úspory,', 'půjčka od táty', 'a prodaná', '*kupónová knížka.*']),
    ('s9', ['Největší *problém?*']),
    ('s10', ['Modem,', 'který v noci', 'budil *tátu.*']),
    ('s11', ['O dva roky později', 'je to *nejnavštěvovanější*', 'český web.']),
    ('s12', ['V roce *2001*', 'je ale firma', 've *ztrátě*', 'a Ivo si nebere *plat,*', 'dokud zase', 'nevydělává.']),
    ('s13', ['Pak přidá *e-mail,*', '*Mapy,* *Sreality*', 'i *zprávy.*']),
    ('s14', ['Maskot pes *Krasty*', 'se mezitím ztratí', 'při procházce v lese', 'a od té doby', 'ho nikdo *neviděl.*']),
    ('s15', ['Aspoň ne *offline.*']),
    ('s16', ['Dnes Seznam používá', 'skoro *90 %*', 'českých uživatelů', 'internetu.']),
    ('s17', ['A Ivo si koupil', 'vlastní *letiště.*']),
    ('s18', ['Mimochodem,', 'chodil na stejnou', '*průmyslovku*', 'jako zakladatel', '*Better Digital.*']),
    ('s19', ['Takže jsme', 'na *dobré cestě.*']),
    ('s20', ['Zatím nám chybí jen', '*pár miliard.*']),
    ('s21', ['Kterou českou firmu', 'chceš *příště?*']),
    ('s22', ['Napiš to', 'do *komentářů.*']),
]
VOWELS = set('aáeéěiíoóuúůyýAÁEÉĚIÍOÓUÚŮYÝ')
def syllables(text):
    t = text.replace('*', '')
    for k, v in {'1996': 'devatenáctsetdevadesátšest', '2001': 'dvatisícejedna', '80 000': 'osmdesáttisíc', '90 %': 'devadesátprocent',
                 'Yahoo': 'jahů', 'Better Digital': 'betrdidžitl', 'e-mail': 'ímejl', 'offline': 'oflajn'}.items():
        t = t.replace(k, v)
    n, prev = 0, False
    for ch in t:
        v = ch in VOWELS
        if v and not prev: n += 1
        prev = v
    return max(1, n)
