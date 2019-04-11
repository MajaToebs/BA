import textstat

import sys
from io import open



filename = sys.argv[1]

with open(filename, "r", encoding="utf-8-sig") as raw:
    text = raw.read().replace("\n", " ")

print(textstat.gunning_fog(text))