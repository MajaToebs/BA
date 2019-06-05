# !/usr/bin/python3
import warnings
import numpy as np

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

import nltk
#nltk.download('punkt') #only DL if don't already have
#nltk.download('popular')

# import the tokenizer from nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

# to find out whether a word contains only alphabetic characters (works only with english texts, since äöü are not included)
from string import ascii_letters

# import spacy with the English module
import spacy
nlp = spacy.load("en_core_web_sm")

import textstat
# set of easy words to get complicated ones
from textstat.textstat import easy_word_set

# for hyphenization
from pyphen import Pyphen

# file I/O
import sys
from io import open


# tokenize a text into alphabetical words
def word_tokenizing(text, tokenizer):
    # tokenize words and filter out punctuations, numbers etc (non-alpha)
    tokenized_words = []
    if tokenizer == "spacy":
        tokenized_words = nlp(text)
        # is_alpha takes only tokens which do not contain spaces or digits
        tokenized_words = [token.text.lower() for token in tokenized_words if token.is_alpha == True]
    elif tokenizer == "nltk":
        tokenized_words = word_tokenize(text)
        only_alpha_words = []
        for word in tokenized_words:
            word = word.lower()
            if all(c in ascii_letters + '-' for c in word):
                only_alpha_words.append(word)
        tokenized_words = only_alpha_words
    return tokenized_words


# count syllables
def count_syllables(word):
    # necessary for the syllable count
    dic = Pyphen(lang='en_EN')
    word_hyphenated = dic.inserted(word)
    count = max(1, word_hyphenated.count("-") + 1)
    return count


# get complex words out of all words
def get_complex_words(words, complexity):
    # difficult words are those with syllables >= complexity and a few other restrictions (see below)
    # easy_word_set is provided by Textstat as
    # a list of common words
    diff_words_set = []

    for word in words:
        syllable_count = count_syllables(word)
        # word not in easy set and longer than x syllables
        difficult = False
        if word not in easy_word_set \
                and syllable_count >= complexity:
            # word not a verb with 3 syllables that ends in -ed, -ing or -es (would usually have only 2 syllables)
            if (word.endswith("ed") == True or word.endswith("es") == True or word.endswith("ing")) \
            and syllable_count == 3 and nltk.tag.pos_tag([word])[0][1].startswith("V"):
                difficult = False
            # no proper nouns
            elif nltk.tag.pos_tag([word])[0][1] is "NNP":
                difficult = False
            else:
                difficult = True
        if difficult:
            diff_words_set.append(word)
    return diff_words_set


def analyse(i, sentences, tokenizer, complexity):
    tokenized_words = []
    for sent in sentences:
        words = word_tokenizing(sent, tokenizer)
        tokenized_words.extend(words)

    # Determine average sentence length
    average_sentence_length = len(tokenized_words) / len(sentences)

    diff_words_set = get_complex_words(tokenized_words, complexity)

    # calculate the percentage of complex words
    diff_word_freq = len(diff_words_set) / len(tokenized_words) * 100
    percentage_of_complex_words.append(diff_word_freq)

    # calculate the fog index
    fog = (diff_word_freq + average_sentence_length) * 0.4

    return round(fog, 4)


def process (f, c, x):
    tokenizer = "nltk"
    filename = "PreprocessedData/English/theses/" + f
    complexity = x
    sentences_per_chunk = c

    # read in the document
    with open(filename, "r", encoding="utf-8-sig") as raw:
        text_in = raw.read().replace("\n", " ")
        # TRY to shorten sentences
        #text_in = text_in.replace(";", ".")
        #text_in = text_in.replace(":", ".")
        #raw.close()

    # tokenize the text into sentences with nltk and then print how many there are
    sentences = sent_tokenize(text_in)

    # store all fog indices of the different chunks
    fog_indices = []
    indices_GFI = []
    indices_FKGL = []
    indices_ARI = []
    indices_SMOG = []
    indices_CLI = []

    # analyse the whole text as one chunk, if 0 is given as sentences_per_chunk or sentences_per_chunk is bigger than the document
    if sentences_per_chunk == 0 or sentences_per_chunk > len(sentences):
        sentences_per_chunk = len(sentences)
        fog_indices.append(analyse(0, sentences, tokenizer, complexity))
        text = text_in
        indices_GFI.append(textstat.textstat.gunning_fog(text))
        indices_FKGL.append(textstat.textstat.flesch_kincaid_grade(text))
        indices_CLI.append(textstat.textstat.coleman_liau_index(text))
        indices_ARI.append(textstat.textstat.automated_readability_index(text))
        indices_SMOG.append(textstat.textstat.smog_index(text))
    # the user wants to analyse chunks of a given length
    else:
        n = len(sentences)/sentences_per_chunk
        for i in range(1, int(n+1)):
            chunk_i = sentences[(i-1)*sentences_per_chunk:i*sentences_per_chunk]
            text = ' '.join(chunk_i)
            fog_indices.append(analyse(i, chunk_i, tokenizer, complexity))
            indices_GFI.append(textstat.textstat.gunning_fog(text))
            indices_FKGL.append(textstat.textstat.flesch_kincaid_grade(text))
            indices_CLI.append(textstat.textstat.coleman_liau_index(text))
            indices_ARI.append(textstat.textstat.automated_readability_index(text))
            indices_SMOG.append(textstat.textstat.smog_index(text))



        # calculate the variances of GFIs of this document for this chunk size
        #variances['length_of_chunk'].append(str(sentences_per_chunk))
        #variances['complexity'].append(complexity)
        #variances['variance'].append(np.var(fog_indices))
        #variances['std'].append(np.std(fog_indices))

    # add this document's calculated GFIs
    for j in range(len(fog_indices)):
        data['document'].append(f)
        data['complexity'].append(complexity)
        data['length_of_chunk'].append(sentences_per_chunk)
        data['number_of_chunk'].append(j+1)
        data['fog'].append(fog_indices[j])
        # append other measures from textstat
        data['GFI'].append(indices_GFI[j])
        data['FKGL'].append(indices_FKGL[j])
        data['ARI'].append(indices_ARI[j])
        data['SMOG'].append(indices_SMOG[j])
        data['CLI'].append(indices_CLI[j])



import os
import pandas as pd

# get the theses we want to analyze
theses_to_analyze = []
# executes for all files in one directory
for f in os.listdir("PreprocessedData/English/theses"):
    if f.startswith("en"):
        theses_to_analyze.append(f)

number_of_theses = len(theses_to_analyze)
print("Analyse", number_of_theses, "theses.............")

data = { 'document' : [],
         'complexity' : [],
        'length_of_chunk' : [],
        'number_of_chunk' : [],
        'fog' : [],
        'GFI' : [],
        'FKGL' : [],
         'ARI' : [],
         'SMOG' : [],
         'CLI' : []}

#variances = { 'length_of_chunk' : [],
#              'complexity' : [],
#                'variance' : [],
#                'std' : [] }


# analyse each thesis
for k, thesis in enumerate(theses_to_analyze):
    print("Analysing thesis", k+1, "of", len(theses_to_analyze))
    # complexity x can be adjusted to get a more robust measure
    for x in [3]:
        percentage_of_complex_words = []
        # number of sentences per chunk
        for m in [0, 1000, 750, 500, 450, 400, 350, 300, 250, 200, 150, 100, 75, 50, 40, 30, 20, 10]:
            process(thesis, m, x)

print("The analysis is finished. \nStoring data.............")

# convert the dictionary with the data to a dataframe
df_fog = pd.DataFrame(data=data)
# drop duplicate rows
df_fog = df_fog.drop_duplicates(keep='first')

# write the collected data into a csv-file
data_out = open("Results/resultsIndicesTheses.csv", "w")
# convert the data to a csv and write it into the given file
data_out.write(df_fog.to_csv())
data_out.close()

# store variances
#data_out = open("Results/variancesTheses.csv", "w")
#df_var = pd.DataFrame(variances)
#data_out.write(df_var.to_csv())
#data_out.close()


print("The collected data has been written to 'Results/resultsIndicesTheses.csv'. \nGo, have a look!")

sys.exit()
