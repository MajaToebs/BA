from io import open
import re
import os

def process(input_filename, output_filename):
    # read in the given document
    with open(input_filename, "r", encoding="utf-8-sig") as raw:
        text_in = raw.readlines()
        raw.close()

    content = ""
    for line in text_in:
        # if the bibliography starts, we ignore the rest of the document
        if bool(re.search(r"^bibliography:?\s*$", line.lower())) or \
            bool(re.search(r"works cited", line.lower())) or \
            bool(re.search(r"^references:?\s*$", line.lower())):
            break

        # if a line contains meta-information about the document, ignore that line
        if not (bool(re.search(r"^words? count", line.lower()))  or
        bool(re.search(r"^(\W|\d|_)+$", line.lower()))  or
        bool(re.search(r"^date of submission", line.lower())) or
        bool(re.search(r"^signature:?", line.lower())) or
        bool(re.search(r"^author:?", line.lower())) or
        bool(re.search(r"^\d+ words\s*$", line.lower())) or
        bool(re.search(r"^==.+==$", line.lower())) ):
            content += line

    # if there has been a mistake and the file has become too short
    if len(content) < 3:
        print("TOO SHORT:", input_filename)
        return

    # some documents do not end with a final dot, but an end of sentence is needed for application of the readability indices
    if content[-1] not in [".", "?", "!"] and content[-2] not in [".", "?", "!"]:
        content += "."

    # tokenize the given text into sentences with nltk, sentences is then a list of lists consisting of strings
    content = content.replace("\n", " ")
    sentences = my_tokenizer.tokenize(content)

    # filter out sources, urls, page numbers
    for index, sentence in enumerate(sentences):
        # if a source is mentioned in parentheses, we substitute that part of the sentence with an empty string
        sentence = re.sub(r"\(.*\d+.*\)", " ", sentence)
        # if a source is mentioned in parentheses with " but no date, we substitute that part of the sentence with an empty string
        sentence = re.sub(r'\(.*[‘’“”\'\"]\w+[‘’“”\'\"].*\)', " ", sentence)
        # urls are deleted as well
        sentence = re.sub(r'^http.+', ' ', sentence)

        # split the sentence into words
        words = sentence.split(" ")

        # delete strange symbols like arrows at the beginning of a word and words that are only symbols
        words_without_symbols = []
        for w in words:
            if bool(re.search(r"^\W+$", w)) is True:
                pass
            elif bool(re.search(r"^\W\w+", w)) is True:
                words_without_symbols.append(w[1:])
            else:
                words_without_symbols.append(w)
        words = words_without_symbols

        # store the shortened sentences
        sentences[index] = words

    # open file where we put the output to write into it
    text_out = open(output_filename, "w")

    # iterate over sentences to filter out the ones which are too short to be real sentences
    for i, s in enumerate(sentences):
        # filter out words that contain only whitespaces
        s = [w for w in s if len(w) > 0]
        # filter out sentences that consist only out of one word
        if (len(s) > 1):
            for j, w in enumerate(s):
                # if the word ends with 2 dots, delete the last one
                if bool(re.search(r"\w+\.\.$", w)):
                    w = w[:-1]
                text_out.write(w)
                # separate words with white spaces
                if j != len(s) - 1:
                    text_out.write(" ")
                # for the last word of a sentence
                else:
                    # separate sentences with line breaks and a period, if there is no other symbol to mark the end of sentence
                    if bool(re.search(r"\w*[.?!]$", w)) or bool(re.search(r"\.[‘’“”\'\"]$", w)):
                        text_out.write('\n')
                    else:
                        text_out.write('.\n')

    text_out.close()



# abbreviations for sentence tokenisation
extra_abbreviations_en = ['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'i.e', 'e.g', 'approx', 'apt', 'appt', 'dept', 'est',
                       'min', 'max', 'misc', 'no', 'acc', 'fig', 'a.m', 'p.m', 'a.d', 'b.c', 'etc', 'ca', 'cf', 'ed',
                       'est', 'f', 'ff', 'pres']
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
punkt_param = PunktParameters()
# add the abbreviations to the tokenizer
punkt_param.abbrev_types = set(extra_abbreviations_en)
my_tokenizer = PunktSentenceTokenizer(punkt_param)

# execute the preprocessing for all files in one directory
for f in os.listdir("Data/English/homework/essays"):
    if not (f.startswith("cor") or f.startswith("dupl")):
        process("Data/English/homework/essays/" + f, "PreprocessedData/English/homework/essays/" + f + ".txt")
for f in os.listdir("Data/English/homework/aff-case"):
    if not (f.startswith("cor") or f.startswith("dupl")):
        process("Data/English/homework/aff-case/" + f, "PreprocessedData/English/homework/aff-case/" + f + ".txt")
for f in os.listdir("Data/English/homework/osmosis"):
    if not (f.startswith("cor") or f.startswith("dupl")):
        process("Data/English/homework/osmosis/" + f, "PreprocessedData/English/homework/osmosis/" + f + ".txt")
for f in os.listdir("Data/English/homework/mission-command"):
    if not (f.startswith("cor") or f.startswith("dupl")):
        process("Data/English/homework/mission-command/" + f, "PreprocessedData/English/homework/mission-command/" + f + ".txt")
