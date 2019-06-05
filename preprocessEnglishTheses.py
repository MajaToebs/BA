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
        # if the bibliography starts, we ignore the rest of the document by breaking the loop
        if bool(re.search(r"^bibliography:?\s*$", line.lower())) or \
            bool(re.search(r"^appendix ([\sa-z0-9:])+$", line.lower())) or \
            bool(re.search(r"^7 -  undertaking of the research team", line.lower())) or \
            bool(re.search(r"^references:?\s*$", line.lower())):
            break

        # if a line contains meta-information about the document or is a heading or page break, ignore that line
        if (bool(re.search(r"^(\W|\d|_)+$", line.lower()))  or
                bool(re.search(r"^\d\.(\d\.?)* \w+( [\w-]+)* \d+ ?$", line.lower())) or #?
                bool(re.search(r"^date of submission:? ", line.lower())) or
                bool(re.search(r"^signature:? ", line.lower())) or
                bool(re.search(r"^\d(\.\d\.?)+ \w+", line.lower())) or
                bool(re.search(r" \.{4,}", line.lower())) or
                bool(re.search(r"P a g e", line)) or
                bool(re.search(r"^==.+==$", line.lower())) ) :
            pass
        else:
            if line.count(" ") < 6:
                # the line has to be the end of a sentence to be considered further, if it is so short
                # line[-3] is needed, since many lines end with a space and a line break after the dot
                if len(line) > 2 and (line[-1] in [".", ",", "?", "!", ";", ":"] or
                                      line[-2] in [".", ",", "?", "!", ";", ":"] or line[-3] in [".", ",", "?", "!", ";", ":"]):
                    content += line
            else:
                content += line

    if len(content) < 3:
        return

    # some documents do not end with a final dot, but an end of sentence is needed for application of the readability indices
    if content[-1] not in [".", "?", "!"] and content[-2] not in [".", "?", "!"]:
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
        # delete unknown symbols which lead into a sentence
        if re.findall(r"^\W( \w+)+", sentence):
            sentence = sentence[1:]

        # split the sentence into words
        words = sentence.split(" ")
        # delete urls and words that consist of at least 4 dots
        words = [w for w in words if (bool(re.search(r"^http.+", w)) is False) and \
                 (bool(re.search(r"(\.{4,})|…{2,}", w)) is False)]
        # delete strange symbols like arrows at the beginning of a word
        words_without_symbols = []
        for w in words:
            if bool(re.search(r"^(\.\.\.?)|…$", w)) is True:
                words_without_symbols.append(".")
            elif bool(re.search(r"^[^(‘’“”\'\"\w]\w*", w)) is True:
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
                if bool(re.search(r"\w+\.\.$", w)):
                    w = w[:-1]
                text_out.write(w)
                # separate words with white spaces
                if j != len(s)-1:
                    text_out.write(" ")
                # for the last word of a sentence
                else:
                    # separate sentences with line breaks and a period, if there is no other symbol to mark the end of sentence
                    if bool(re.search(r"\w*[.?!]$", w)) or bool(re.search(r"\.[‘’“”\'\"]$", w)):
                        text_out.write('\n')
                    else:
                        text_out.write('.\n')

    text_out.close()



# execute the preprocessing for all files in one directory
for f in os.listdir("Data/English/theses"):
    # look for English texts only
    if f.startswith("en"):
        process("Data/English/theses/" + f, "PreprocessedData/English/theses/" + f + ".txt")
