from io import open
from nltk.tokenize import sent_tokenize
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
            bool(re.search(r"^references:?\s*$", line.lower())):
            break

        # if a line starts with a comment or formatting from a reader or contains meta-information about the document, ignore that line
        if not (bool(re.search(r"^kommentiert", line.lower())) or \
                bool(re.search(r"^formatiert", line.lower())) or \
                bool(re.search(r"^formatted", line.lower())) or \
                bool(re.search(r"^commented", line.lower()))  or \
                bool(re.search(r"^words? count", line.lower()))  or \
                bool(re.search(r"^(\W|\d|_)+$", line.lower()))  or \
                bool(re.search(r"^date of submission", line.lower())) or \
                bool(re.search(r"^signature:?", line.lower())) or \
                bool(re.search(r"^\d+ words\s*$", line.lower())) or \
                bool(re.search(r"^==.+==$", line.lower())) ):
            content += line

    # some documents do not end with a final dot, but an end of sentence is needed for application of the readability indices
    if content[-1] != ".":
        content += "."

    # tokenize the given text into sentences with nltk, sentences is then a list of lists consisting of strings
    content = content.replace("\n", " ")
    sentences = sent_tokenize(content)

    # filter out sources, urls, page numbers
    for index, sentence in enumerate(sentences):
        # if a source is mentioned in parentheses, we substitute that part of the sentence with an empty string
        sentence = re.sub(r"\(.*\d+.*\)", " ", sentence)
        # if a source is mentioned in parentheses with " but no date, we substitute that part of the sentence with an empty string
        sentence = re.sub(r'\(.*[‘’“”\'\"].+[‘’“”\'\"].*\)', " ", sentence)
        # delete page numbers
        sentence = re.sub(r" \d+  ", " ", sentence)

        # split the sentence into words
        words = sentence.split(" ")
        # delete urls
        words = [w for w in words if bool(re.search(r"^http.+", w)) is False]
        # delete strange symbols like arrows at the beginning of a word
        words_without_symbols = []
        for w in words:
            if bool(re.search(r"^\W\w+", w)) is True:
                words_without_symbols.append(w[1:])
            else:
                words_without_symbols.append(w)
        words = words_without_symbols

        #words = [w for w in words if bool(re.search(r"(^\W+$|([a-zA-Z]*\d+[a-zA-Z]*)+)", w)) is False]

        # store the shortened sentences
        sentences[index] = words

    # open file where we put the output to write into it
    text_out = open(output_filename, "w")

    # iterate over sentences to filter out the ones which are too short to be real sentences
    for i, s in enumerate(sentences):
        # filter out sentences that are shorter than three words
        if (len(s) >= 3):
            for w in s:
                # filter out sentences that contain only whitespaces
                if len(w)>0:
                    text_out.write(w)
                    # separate words with white spaces
                    text_out.write(" ")
            # separate sentences with line breaks
            text_out.write('\n')

    text_out.close()



# executes for all files in one directory
for f in os.listdir("Data/homework/essays"):
    process("Data/homework/essays/" + f, "PreprocessedData/homework/essays/" + f + ".txt")
for f in os.listdir("Data/homework/aff-case"):
    process("Data/homework/aff-case/" + f, "PreprocessedData/homework/aff-case/" + f + ".txt")
for f in os.listdir("Data/homework/osmosis"):
    process("Data/homework/osmosis/" + f, "PreprocessedData/homework/osmosis/" + f + ".txt")
for f in os.listdir("Data/homework/mission-command"):
    process("Data/homework/mission-command/" + f, "PreprocessedData/homework/mission-command/" + f + ".txt")