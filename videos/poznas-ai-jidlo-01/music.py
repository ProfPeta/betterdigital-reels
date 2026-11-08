# Hravá soutěžní hudba, 104 BPM, jemně pod hlasem. Styly a funkce: engine/sfxlib.py.
def pizz(at, ch, d, k):
    notes = CH[ch] + [CH[ch][0] + 12]
    pad(at, CH[ch], d + .05, .022, a=.1, r=.3, fc=1400)
    for i in range(int(d / B + 1e-6)): pluck(at + i * B, notes[(i * 2) % 4] + 12, .06, .3, (i % 2 - .5) * .4, 2600, .07)
S4, S7, S9, S12, S13, S14 = (sc(x) for x in ('s4', 's7', 's9', 's12', 's13', 's14'))
bars(0, S4, ['C', 'G'], pizz)                                  # háček
bars(S4, S7, ['Am', 'F', 'C', 'G'], flow)                      # tři kola
bars(S7, S9, ['F', 'G'], pizz)                                 # napiš tipy
bars(S9, S12, ['C', 'G', 'Am', 'F'], flow)                     # odpovědi 1, 2
bars(S12, st('s13'), ['Dm', 'E'], hush)                        # napětí před pointou
bars(st('s13'), S14, ['F', 'G'], soft)                         # obě AI
bars(S14, DUR - 1.5, ['C', 'G'], outro)
ending()
