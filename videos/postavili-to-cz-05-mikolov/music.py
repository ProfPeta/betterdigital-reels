# Jemný podklad bez bicích. Funkce a styly jsou v engine/sfxlib.py. sc('sN') = začátek scény.
S4, S5, S8, S9, S12, S14, S15, S17, S19, S22 = (sc(x) for x in ('s4', 's5', 's8', 's9', 's12', 's14', 's15', 's17', 's19', 's22'))
bars(0, S4, ['Am', 'F'], hush)                         # háček
bars(S4, S5, ['C'], soft)                              # Mikolov
bars(S5, S8, ['Am', 'F', 'C', 'G'], flow)              # Google, slova na čísla
bars(S8, S9, ['Dm'], hush)                             # zamítnuto
bars(S9, S12, ['F', 'C', 'G', 'Am'], flow)             # word2vec, ChatGPT
bars(S12, S14, ['Am', 'F'], soft)                      # návrat
bars(S14, S15, ['Dm', 'Am'], hush)                     # nula
bars(S15, S17, ['C', 'G'], flow)                       # Singapur
bars(S17, S19, ['F', 'C', 'G', 'Am'], flow)            # BottleCap
bars(S19, S22, ['F', 'G', 'C'], soft)                  # medaile, pointa
bars(S22, DUR - 1.5, ['C', 'G'], outro)
ending()

