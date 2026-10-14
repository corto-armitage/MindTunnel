import base64
import gzip
import sys
from pathlib import Path

# Save the single QR's scanned text to a text file, then run:
# python decode_mindtunnel.py scanned.txt
# For the three plain Base64 QRs, save each scan separately, then run:
# python decode_mindtunnel.py --plain part1.txt part2.txt part3.txt
plain = sys.argv[1:2] == ['--plain']
paths = sys.argv[2:] if plain else sys.argv[1:]
if not paths:
    raise SystemExit('Provide scanned text file(s); use --plain for the three-part version.')
text = ''.join(''.join(Path(p).read_text().split()) for p in paths)
data = base64.b64decode(text, validate=True)
if not plain:
    data = gzip.decompress(data)
destination = Path('MindTunnel.py')
with destination.open('xb') as f:
    f.write(data)
print('Saved MindTunnel.py')
