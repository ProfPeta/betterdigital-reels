# Jemný podklad, 100 BPM. Styly a funkce: engine/sfxlib.py.
def pizz(at, ch, d, k):
    notes = CH[ch] + [CH[ch][0] + 12]
    pad(at, CH[ch], d + .05, .022, a=.1, r=.3, fc=1400)
    for i in range(int(d / B + 1e-6)): pluck(at + i * B, notes[(i * 2) % 4] + 12, .055, .3, (i % 2 - .5) * .4, 2600, .07)
S4, S5, S7, S9, S12, S15, S16, S17, S20 = (sc(x) for x in ('s4', 's5', 's7', 's9', 's12', 's15', 's16', 's17', 's20'))
bars(0, S4, ['Am', 'F'], pizz)                         # hádanka
bars(S4, S5, ['C'], soft)                              # je to Kiwi
bars(S5, S7, ['Am', 'F', 'C', 'G'], soft)              # student, problém
bars(S7, S9, ['F', 'C', 'G', 'Am'], flow)              # 2012, investor
bars(S9, S12, ['C', 'G', 'Am', 'F'], flow)             # růst, hledání
bars(S12, S15, ['Dm', 'Am', 'E'], hush)                # spory
bars(S15, S16, ['F', 'G'], soft)                       # fond
bars(S16, S17, ['Dm', 'E'], hush)                      # covid
bars(S17, S20, ['C', 'G', 'F'], flow)                  # přežila
bars(S20, DUR - 1.5, ['C', 'G'], outro)
ending()
