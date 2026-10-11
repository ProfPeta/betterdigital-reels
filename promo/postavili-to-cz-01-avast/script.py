"""POSTAVILI TO · Česká edice #1 – Avast. Scénář: věty hlasu (VO) a titulky po kouscích.
Text pro ElevenLabs je v README (fonetický přepis McAfee, AVG, Jumpshot). Tady je pravopisná verze pro titulky.
Kousek s *hvězdičkami* = zvýrazněné slovo. Zdroje faktů: README.md."""

SENT = [
    ('s1', ['Antivirus,', 'který dnes chrání', '*stovky milionů* lidí,', 'začal na počítači,', 'kterému šéfové', 'říkali *hračka.*']),
    ('s2', ['Je rok *1988.*']),
    ('s3', ['A do pražského', 'výzkumného ústavu', 'dorazí první počítač', 'z *Itálie.*']),
    ('s4', ['Vedení ho odbude', 'jako *hračku.*']),
    ('s5', ['A tak skončí', 'na stole', 'mladého grafika', '*Pavla Baudiše.*']),
    ('s6', ['Jednoho dne', 'mu kolega přinese', '*disketu,*', 'na které je', 'virus *Vienna.*']),
    ('s7', ['Pavel ho rozebere', 'do posledního *bajtu*', 'a napíše program,', 'který ho dokáže', '*zničit.*']),
    ('s8', ['Jenže za komunismu', 'se podnikat *nesmělo*', 'a jedinou cestou', 'bylo *družstvo.*']),
    ('s9', ['Pavel ho založí', 's kolegou', '*Eduardem Kučerou*', 'v listopadu *1989.*']),
    ('s10', ['Ve stejném měsíci', '*padne režim.*']),
    ('s11', ['Svůj program', 'pojmenují *Avast,*', 'zkratkou z', 'Antivirus Advanced Set.']),
    ('s12', ['O pár let později', 'jim volá', 'americký *McAfee,*', 'že by firmu', 'rád *koupil.*']),
    ('s13', ['Oni *odmítnou*', 'a prodají mu', 'jen *licenci.*']),
    ('s14', ['Kolem roku *2000*', 'jsou přesto', 'na pokraji *krachu.*']),
    ('s15', ['A tak udělají něco,', 'co vypadá', 'jako *šílenství:*']),
    ('s16', ['svůj antivirus', 'začnou rozdávat', '*zadarmo.*']),
    ('s17', ['Jejich první e-shop', '*devět dní*', 'neprodá vůbec *nic.*']),
    ('s18', ['Pak se to ale', '*zlomí.*']),
    ('s19', ['Přijde první', '*milion* uživatelů,', 'potom *20 milionů,*']),
    ('s20', ['a když jich je', '*40 milionů,*', 'má celá firma', 'pořád jen', '*38 zaměstnanců.*']),
    ('s21', ['Později koupí', 'konkurenční *AVG*', 'za *1,3 miliardy*', 'dolarů']),
    ('s22', ['a jejich vstup', 'na londýnskou burzu', 'je *největším*', 'evropským', 'technologickým', 'vstupem roku.']),
    ('s23', ['Pak ale přijde', '*skandál.*']),
    ('s24', ['Jejich dceřiná firma', '*Jumpshot*', 'prodávala data', 'o tom, co lidé', 'dělají *na internetu.*']),
    ('s25', ['Musela *skončit*', 'a americký úřad', 'jim později vyměřil', 'pokutu', '*16,5 milionu*', 'dolarů.']),
    ('s26', ['V roce *2022*', 'se Avast spojí', 's americkým *Nortonem*', 'za víc než', '*8 miliard* dolarů']),
    ('s27', ['a Pavel Baudiš', 'je dnes', 'podle Forbesu', 'dolarový *miliardář.*']),
    ('s28', ['Spolu s Eduardem', 'a svými ženami', 'pak založili nadaci,', 'která už rozdala', 'skoro *400 milionů*', 'korun lidem,', 'kteří to *potřebují.*']),
    ('s29', ['Od hračky na stole', 'k *miliardám.*']),
    ('s30', ['Kterou českou firmu', 'chceš', 'v dalším díle?']),
    ('s31', ['Napiš to', 'do *komentářů.*']),
]

VOWELS = set('aáeéěiíoóuúůyýAÁEÉĚIÍOÓUÚŮYÝ')


def syllables(text):
    """Hrubý odhad slabik (české samohlásky, číslice a cizí jména jako čtená slova)."""
    t = text.replace('*', '')
    for k, v in {'1988': 'devatenáctsetosmdesátosm', '1989': 'osmdesátdevět', '2000': 'dvatisíce', '2022': 'dvatisícedvacetdva',
                 '1,3': 'jednucelоutři'.replace('о','o'), '16,5': 'šestnáctapůl', '400': 'čtyřista', '38': 'třicetosm', '40': 'čtyřicet', '20': 'dvacet',
                 '8': 'osm', 'McAfee': 'mekafí', 'AVG': 'ávégé', 'Jumpshot': 'džampšot', 'Antivirus Advanced Set': 'antivirus edvenst set',
                 'Vienna': 'viena', 'Forbesu': 'forbsu', 'e-shop': 'íšop'}.items():
        t = t.replace(k, v)
    n, prev = 0, False
    for ch in t:
        v = ch in VOWELS
        if v and not prev: n += 1
        prev = v
    return max(1, n)


if __name__ == '__main__':
    print('slabik', sum(syllables(c) for _, cs in SENT for c in cs))
