import sys
from io import open
from nltk.tokenize import sent_tokenize
import re
import os

#for f in os.listdir("Data/homework/essays"):
#    process(f, "PreprocessedData/homework/essays/f.txt")

#def process(input_filename)
# the second argument is the input document and the third document the output argument
if len(sys.argv) == 3:
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

# read in the given document
with open(input_filename, "r", encoding="utf-8-sig") as raw:
    text_in = raw.read().replace("\n", " ")
    raw.close()

# tokenize the given text into sentences with nltk, sentences is then a list of lists consisting of strings
sentences = sent_tokenize(text_in)

# split each sentence into words and filter out different things
for index, sentence in enumerate(sentences):
    #print(sentence)

    # if the bibliography starts, we ignore the rest of the document
    if "bibliography" in sentence.lower() or "references" in sentence.lower():
        sentences = sentences[0:index]
        break

    # if a source is mentioned in parentheses, we substitute that part of the sentence with an empty string
    sentence = re.sub(r"\(.*\d+.*\)", " ", sentence)
    # if a source is mentioned in parentheses with " but no date, we substitute that part of the sentence with an empty string
    sentence = re.sub(r'\(.*[‘’“”\'\"].+[‘’“”\'\"].*\)', " ", sentence)
    # delete page numbers
    sentence = re.sub(r" \d+  ", " ", sentence)

    # if a sentence contains a comment from a reader, delete that sentence
    if "kommentiert" in sentence.lower():
        sentence = " "


    words = sentence.split(" ")
    # delete urls
    words = [w for w in words if bool(re.search(r"^http.+", w)) is False]
    # delete page breaks
    words = [w for w in words if bool(re.search(r"^==.+==$", w)) is False]




    # filter out special characters (non-word, e.g. "&")


    #words = [w for w in words if bool(re.search(r"^\W+$", w)) is False]
    #print(words)
    # filter out digits, numbers, floating point numbers, version numbers etc
    #words = [w for w in words if bool(re.search(r"^(\W|\d)+$", w)) is False]
    #print(words)
    #words = [w for w in words if bool(re.search(r"(^\W+$|([a-zA-Z]*\d+[a-zA-Z]*)+)", w)) is False]
    #print(words)

    # store the shortened sentences
    sentences[index] = words

# open file where we put the output
text_out = open(output_filename, "w")



# iterate over sentences to filter those
for i, s in enumerate(sentences):
    # filter out sentences that are shorter than three words
    if (len(s) >= 3):
        # filter out sentences that contain only whitespaces
        for w in s:
            if len(w)>0:
                text_out.write(w)
                text_out.write(" ")
        text_out.write('\n')


text_out.close()
