"""POSTAVILI TO · Česká edice #6: Kiwi.com / Oliver Dlouhý. Věty hlasu a titulky; *hvězdičky* = zvýraznění. Zdroje: README.md."""
SENT = [
    ('s1', ['Jedna z těch firem', 'vznikla v *Brně.*']),
    ('s2', ['*Skyscanner,*', 'nebo *Kiwi.com?*']),
    ('s3', ['Tipni si.']),
    ('s4', ['Je to *Kiwi.com.*']),
    ('s5', ['Student *Oliver Dlouhý*', 'sháněl levnou letenku', 'do *Portugalska.*']),
    ('s6', ['Zjistil,', 'že vyhledávače', 'neumí spojit lety', 'aerolinek, které spolu', '*nespolupracují.*']),
    ('s7', ['Tak to v roce *2012*', 's kamarádem programátorem', 'naprogramovali *sami.*']),
    ('s8', ['První investor', 'jim dal', '*450 tisíc korun.*']),
    ('s9', ['Za dva roky', 'měli tržby', '*140 milionů.*']),
    ('s10', ['O další dva roky později', 'přes *8 miliard.*']),
    ('s11', ['A lidé u nich', 'hledali letenky', '*100milionkrát* denně.']),
    ('s12', ['*Aerolinkám*', 'se to nelíbilo.']),
    ('s13', ['*Ryanair*', 'se s nimi', 'roky přel.']),
    ('s14', ['Americký *Southwest*', 'je zažaloval', 'a u soudu v Texasu', '*vyhrál.*']),
    ('s15', ['V roce *2019*', 'koupil většinu firmy', 'americký *fond.*']),
    ('s16', ['Pak přišel *covid,*', 'letadla zůstala', 'na zemi', 'a firma spadla', 'do miliardové *ztráty.*']),
    ('s17', ['*Přežila.*']),
    ('s18', ['A Ryanair?']),
    ('s19', ['Ten s ní dnes', '*spolupracuje.*']),
    ('s20', ['Koupil bys letenku', 'přes Kiwi?']),
    ('s21', ['Napiš *ano,*', 'nebo *ne.*']),
]
REPLACE = {'Skyscanner': 'skajskener', 'Kiwi.com': 'kivikom', '2012': 'dvatisícedvanáct', '450': 'čtyřistapadesát', '140': 'stočtyřicet', '100milionkrát': 'stomilionkrát',
           '8 ': 'osm ', 'Ryanair': 'rajenér', 'Southwest': 'sautvest', '2019': 'dvatisícedevatenáct', 'covid': 'kovid'}
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
