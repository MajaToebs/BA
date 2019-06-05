# coding: utf-8

# # Gunning Fog Calculator
# The purpose of this calculator is to determine the readability of a text. Readability is defined as the level
# of education an individual needs to understand a text on the first reading.
# Gunning Fog is calculated by adding the average sentence length to the percentage of difficult words
# (words comprising of 3 or more syllables) multiplied by 0.4.
# This program opens a file, calculates the number of words, sentences, average number of words per sentence
# and the percentage of difficult words in the overall text before outputting a reading level the text is assigned to.
# For the curious, difficult words in a text are also printed.
# For more information on Gunning Fog: http://www.readabilityformulas.com/gunning-fog-readability-formula.php
# the slight difference in results from online calculators is probably due to the count of complex words # working on this issue


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



# for hyphenization
from pyphen import Pyphen

# file I/O
import sys
from io import open


# tokenize a text into alphabetical words
def word_tokenizing(text, tokenizer):
    # tokenize words and filter out punctuations, numbers etc (non-alpha)
    tokenized_words = []
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
    dic = Pyphen(lang='de_DE')
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
            # no proper nouns
            if nltk.tag.pos_tag([word])[0][1] is "NNP":
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
    filename = "PreprocessedData/German/theses/" + f
    complexity = x
    sentences_per_chunk = c

    # read in the document
    with open(filename, "r", encoding="utf-8-sig") as raw:
        text_in = raw.read().replace("\n", " ")
        # TRY to shorten sentences
        #text_in = text_in.replace(";", ".")
        #text_in = text_in.replace(":", ".")
        #raw.close()

    # tokenize the text into sentences with nltk
    sentences = sent_tokenize(text_in)

    # store all fog indices of the different chunks
    fog_indices = []

    # analyse the whole text as one chunk, if 0 is given as sentences_per_chunk or sentences_per_chunk is bigger than the document
    if sentences_per_chunk == 0 or sentences_per_chunk > len(sentences):
        sentences_per_chunk = len(sentences)
        fog_indices.append(analyse(0, sentences, tokenizer, complexity))
    # the user wants to analyse chunks of a given length
    else:
        n = len(sentences)/sentences_per_chunk
        for i in range(1, int(n+1)):
            chunk_i = sentences[(i-1)*sentences_per_chunk:i*sentences_per_chunk]
            fog_indices.append(analyse(i, chunk_i, tokenizer, complexity))
            # calculate the variances of GFIs of this document for this chunk size
        variances['length_of_chunk'].append(str(sentences_per_chunk))
        variances['complexity'].append(complexity)
        variances['variance'].append(np.var(fog_indices))
        variances['std'].append(np.std(fog_indices))

    # add this document's calculated GFIs
    for j in range(len(fog_indices)):
        data['document'].append(f)
        data['complexity'].append(complexity)
        data['length_of_chunk'].append(sentences_per_chunk)
        data['number_of_chunk'].append(j+1)
        data['GFI'].append(fog_indices[j])




import os
import pandas as pd

# get the theses we want to analyze
theses_to_analyze = []
# executes for all files in one directory
for f in os.listdir("PreprocessedData/German/theses"):
    if f.startswith("de"):
        theses_to_analyze.append(f)

number_of_theses = len(theses_to_analyze)
print("Analyse", number_of_theses, "German theses.............")

data = { 'document' : [],
         'complexity' : [],
        'length_of_chunk' : [],
        'number_of_chunk' : [],
        'GFI' : []}

variances = { 'length_of_chunk' : [],
              'complexity' : [],
                'variance' : [],
                'std' : [] }

# prepare set of easy words to get complicated ones
with open("germanStopWords", "r") as raw:
    easy_words = raw.read().replace("\n", " ")
    easy_word_set = easy_words.split(" ")

# analyse each thesis
for k, thesis in enumerate(theses_to_analyze):
    print("Analysing thesis", k+1, "of", len(theses_to_analyze))
    # can be adjusted to get a more robust measure!?
    for x in [3]:
        percentage_of_complex_words = []
        # number of sentences per chunk
        for m in [0, 1000, 750, 500, 450, 400, 350, 300, 250, 200, 150, 100, 75, 50, 40, 30, 20, 10]:
            process(thesis, m, x)
            #print(np.median(percentage_of_complex_words))

print("The analysis is finished. \nStoring data.............")

# convert the dictionary with the data to a dataframe
df_fog = pd.DataFrame(data=data)
# drop duplicate rows
df_fog = df_fog.drop_duplicates(keep='first')

# write the collected data into a csv-file
data_out = open("Results/German/resultsTheses.csv", "w")
# convert the data to a csv and write it into the given file
data_out.write(df_fog.to_csv())
data_out.close()

# store variances
data_out = open("Results/German/variancesTheses.csv", "w")
df_var = pd.DataFrame(variances)
data_out.write(df_var.to_csv())
data_out.close()


print("The collected data has been written to 'Results/German/resultsTheses.csv' and 'Results/German/variancesTheses.csv'. \nGo, have a look!")

sys.exit()