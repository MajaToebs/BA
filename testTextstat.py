import textstat

import sys
from io import open

filename = sys.argv[1]

with open(filename, "r", encoding="utf-8-sig") as raw:
    text = raw.read().replace("\n", " ")

print('FOG:', textstat.gunning_fog(text))
print('flesch_reading_ease:', textstat.flesch_reading_ease(text))
print('smog_index:', textstat.smog_index(text))
print('flesch_kincaid_grade:', textstat.flesch_kincaid_grade(text))
print('coleman_liau_index:', textstat.coleman_liau_index(text))
print('automated_readability_index:', textstat.automated_readability_index(text))
print('dale_chall_readability_score:', textstat.dale_chall_readability_score(text))
print('difficult_words:', textstat.difficult_words(text))
print('linsear_write_formula:', textstat.linsear_write_formula(text))
print('text_standard:', textstat.text_standard(text))
