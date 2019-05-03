import sys
from io import open
from nltk.tokenize import sent_tokenize
import re

if len(sys.argv) == 2:
    filename = sys.argv[1]

with open(filename, "r", encoding="utf-8-sig") as raw:
    text_in = raw.read().replace("\n", " ")
    raw.close()

sentences = sent_tokenize(text_in)

# sentences is list of lists consisting of strings
for index, sentence in enumerate(sentences):
    words = sentence.split(" ")
    # filter out special characters (non-word, e.g. "&")
    print(words)
    #words = [w for w in words if bool(re.search(r"^\W+$", w)) is False]
    #print(words)
    # filter out digits, numbers, floating point numbers, version numbers etc
    #words = [w for w in words if bool(re.search(r"^(\W|\d)+$", w)) is False]
    #print(words)
    words = [w for w in words if bool(re.search(r"(^\W+$|([a-zA-Z]*\d+[a-zA-Z]*)+)", w)) is False]
    print(words)
    sentences[index] = words

# open file where we put the output
text_file = open("r1.txt", "w")



# iterate over sentences to filter those
for i, s in enumerate(sentences):
    # filter out sentences that are shorter than three words
    if (len(s) >= 3):
        # filter out sentences that contain only whitespaces
        for w in s:
            if len(w)>0:
                text_file.write(w)
                text_file.write(" ")
        #text_file.write('/n')


text_file.close()
