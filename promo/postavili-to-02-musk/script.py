"""Postavili to #02 – Elon Musk. Scénář: věty hlasu (VO) a titulky po kouscích.
Text pro ElevenLabs je v README (fonetický přepis jmen). Tady je pravopisná verze pro titulky.
Kousek s *hvězdičkami* = zvýrazněné slovo. Zdroje faktů: README.md."""

SENT = [
    ('s1', ['Jeho první', 'tři rakety', '*selhaly.*']),
    ('s2', ['Kdyby selhala', 'i čtvrtá,', 'byl by *konec.*']),
    ('s3', ['*Elon Musk.*']),
    ('s4', ['Ve dvanácti', 'naprogramoval hru', 'a prodal ji', 'za *500 dolarů.*']),
    ('s5', ['Stanford', '*vzdal*', 'dřív, než začal.']),
    ('s6', ['S bratrem', 'rozjel firmu', 'a spal', 'v kanceláři.']),
    ('s7', ['Prodali ji', 'za *307 milionů*', 'dolarů.']),
    ('s8', ['Pak založil', '*X.com.*', 'Z něj vznikl', 'PayPal.']),
    ('s9', ['Zatímco letěl', 'na líbánky,', '*sesadili ho.*']),
    ('s10', ['Pak založil', '*SpaceX.*']),
    ('s11', ['Teslu', '*nezaložil.*']),
    ('s12', ['Přišel do ní', 'jako investor.']),
    ('s13', ['Rok *2008.*']),
    ('s14', ['Tesla skoro', '*krachuje*', 'a rakety padají.']),
    ('s15', ['Čtvrtý start', '*vyšel.*']),
    ('s16', ['Pak přišla zakázka', 'od NASA', 'za *1,6 miliardy.*']),
    ('s17', ['Pak rakety,', 'které *přistávají.*']),
    ('s18', ['Auto', 've *vesmíru.*']),
    ('s19', ['Raketa', 'chycená *věží.*']),
    ('s20', ['Za jeden tweet', 'zaplatil', '*20 milionů*', 'dolarů.']),
    ('s21', ['Twitter koupil', 'za *44 miliard*', 'a přejmenoval ho', 'na *X.*']),
    ('s22', ['Pro Trumpa', 'škrtal', 'státní výdaje.']),
    ('s23', ['Pak se', '*pohádali.*']),
    ('s24', ['Letos se stal', 'prvním *bilionářem*', 'v historii.']),
    ('s25', ['Prý chce', 'umřít', 'na *Marsu.*']),
    ('s26', ['Jen ne', 'při *dopadu.*']),
    ('s27', ['Koho chceš', 'v dalším díle?']),
    ('s28', ['*Gatese,*', '*Wozniaka,*', 'nebo *Bezose?*']),
    ('s29', ['Napiš to', 'do *komentářů.*']),
]

VOWELS = set('aáeéěiíoóuúůyýAÁEÉĚIÍOÓUÚŮYÝ')


def syllables(text):
    """Hrubý odhad slabik (české samohlásky, číslice a cizí jména jako čtená slova)."""
    t = text.replace('*', '')
    for k, v in {'2008': 'dvatisíceosm', '500': 'pětset', '307': 'třistasedm', '1,6': 'jednucelouššest', '20': 'dvacet',
                 '44': 'čtyřicetčtyři', 'Elon Musk': 'Ílon Mask', 'Stanford': 'stenford', 'X.com': 'eksdotkom',
                 'PayPal': 'pejpal', 'SpaceX': 'spejseks', 'NASA': 'nasa', 'tweet': 'tvít', 'Twitter': 'tvitr',
                 'X.': 'iks.', 'Trumpa': 'trampa', 'Gatese': 'gejtse', 'Wozniaka': 'vozniaka', 'Bezose': 'bejzose'}.items():
        t = t.replace(k, v)
    n, prev = 0, False
    for ch in t:
        v = ch in VOWELS
        if v and not prev: n += 1
        prev = v
    return max(1, n)


if __name__ == '__main__':
    tot = sum(syllables(c) for _, cs in SENT for c in cs)
    ep01 = 0
    print('slabik', tot, ' odhad (jako #01: 59,9 s hlasu)')
