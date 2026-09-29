#!/usr/bin/env python3
"""Contact sheet of rendered stills for visual QA.
Usage: python3 engine/sheet.py qa/ qa_sheet.png [columns]"""
import glob, sys
from PIL import Image
d, out = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 7
fs = sorted(glob.glob(f'{d}/*.png'))
sz = (240, 427); rows = (len(fs) + cols - 1) // cols
sh = Image.new('RGB', (cols * (sz[0] + 6), rows * (sz[1] + 6)), (120, 120, 120))
for i, f in enumerate(fs):
    sh.paste(Image.open(f).convert('RGB').resize(sz), ((i % cols) * (sz[0] + 6), (i // cols) * (sz[1] + 6)))
sh.save(out)
print(out)
