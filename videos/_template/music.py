# Jemný podklad. Styly: hush, soft, flow, outro, pulse. Funkce jsou v engine/sfxlib.py.
S2, S3, S5 = sc('s2'), sc('s3'), sc('s5')
bars(0, S2, ['Am', 'F'], hush)
bars(S2, S3, ['C', 'G'], soft)
bars(S3, S5, ['F', 'C', 'G', 'Am'], flow)
bars(S5, DUR - 1.5, ['C', 'G'], outro)
ending()
