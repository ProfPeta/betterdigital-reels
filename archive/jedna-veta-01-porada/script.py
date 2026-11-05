"""JEDNA VĚTA #01 – Kalkulačka porad. Scénář: věty hlasu (VO) a titulky po kouscích.
Text pro ElevenLabs je v README (AI foneticky „ej aj“). Tady je pravopisná verze pro titulky.
Kousek s *hvězdičkami* = zvýrazněné slovo. Věta s4 je samotné zadání – ve videu se píše do pole, ne do titulků."""

SENT = [
    ('s1', ['*Jedna věta.*']),
    ('s2', ['*Hotová aplikace.*']),
    ('s3', ['Napsali jsme AI', '*jediné zadání:*']),
    ('s4', ['Udělej kalkulačku,', 'která v reálném čase', 'ukáže,', 'kolik stojí porada.']),
    ('s5', ['AI napsala *kód,*', 'navrhla *design*', 'a aplikaci *spustila.*']),
    ('s6', ['Bez jediného', '*řádku od nás.*']),
    ('s7', ['Zadáš, kolik lidí', 'sedí v místnosti', 'a kolik zhruba *berou.*']),
    ('s8', ['Zmáčkneš *start.*']),
    ('s9', ['A díváš se,', 'jak porada', '*pálí peníze.*']),
    ('s10', ['Pošli to tomu,', 'kdo svolává', '*zbytečné porady.*']),
    ('s11', ['A napiš, co máme', '*postavit příště.*']),
]

VOWELS = set('aáeéěiíoóuúůyýAÁEÉĚIÍOÓUÚŮYÝ')


def syllables(text):
    """Hrubý odhad slabik (české samohlásky; AI a design jako čtená slova)."""
    t = text.replace('*', '')
    for k, v in {'AI': 'ejaj', 'design': 'dyzajn'}.items():
        t = t.replace(k, v)
    n, prev = 0, False
    for ch in t:
        v = ch in VOWELS
        if v and not prev: n += 1
        prev = v
    return max(1, n)


if __name__ == '__main__':
    print('slabik', sum(syllables(c) for _, cs in SENT for c in cs))
