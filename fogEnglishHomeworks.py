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

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

import nltk
#nltk.download('punkt') #only DL if don't already have
#nltk.download('popular')

import numpy as np

# import the tokenizer from nltk
#from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

# to find out whether a word contains only alphabetic characters (works only with english texts, since äöü are not included)
from string import ascii_letters

# import spacy with the English module
import spacy
nlp = spacy.load("en_core_web_sm")

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
            if (word.endswith("ed") == True or word.endswith("es") == True or word.endswith("ing") == True) \
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

    # print the percentage of complex words
    diff_word_freq = len(diff_words_set) / len(tokenized_words) * 100
    percentage_of_complex_words.append(diff_word_freq)

    # calculate the fog index
    fog = (diff_word_freq + average_sentence_length) * 0.4

    return round(fog, 4)


def process (f, c, x):
    tokenizer = "nltk"
    filename = "PreprocessedData/homework/" + f
    complexity = x
    sentences_per_chunk = c

    # read in the document
    with open(filename, "r", encoding="utf-8-sig") as raw:
        text_in = raw.read().replace("\n", " ")
        raw.close()

    # tokenize the text into sentences with nltk and then print how many there are
    sentences = my_tokenizer.tokenize(text_in)

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
        variances['variance'].append(np.var(fog_indices))
        variances['complexity'].append(complexity)

    # add this document's calculated GFIs
    for j in range(len(fog_indices)):
        data['document'].append(f)
        data['complexity'].append(complexity)
        data['length_of_chunk'].append(sentences_per_chunk)
        data['number_of_chunk'].append(j+1)
        data['GFI'].append(fog_indices[j])




import os
import pandas as pd

# abbreviations for sentence tokenisation
extra_abbreviations_en = ['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'i.e', 'e.g', 'approx', 'apt', 'appt', 'dept', 'est',
                       'min', 'max', 'misc', 'no', 'acc', 'fig', 'a.m', 'p.m', 'a.d', 'b.c', 'etc', 'ca', 'cf', 'ed',
                       'est', 'f', 'ff', 'pres']
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
punkt_param = PunktParameters()
punkt_param.abbrev_types = set(extra_abbreviations_en)
my_tokenizer = PunktSentenceTokenizer(punkt_param)

# get the theses we want to analyze
theses_to_analyze = []
# executes for all files in directories

# executes for all files in one directory
essays = []
for f in os.listdir("PreprocessedData/homework/essays"):
    essays.append("essays/" + f)
aff_case = []
for f in os.listdir("PreprocessedData/homework/aff-case"):
    aff_case.append("aff-case/" + f)
osmosis = []
for f in os.listdir("PreprocessedData/homework/osmosis"):
    osmosis.append("osmosis/" + f)
mission_command = []
for f in os.listdir("PreprocessedData/homework/mission-command"):
    mission_command.append("mission-command/" + f)

theses_to_analyze = [essays, aff_case, osmosis, mission_command]

for i in range(len(theses_to_analyze)):
    print("Analyse folder " + str(i+1) + " out of " + str(len(theses_to_analyze)))
    number_of_homeworks = len(theses_to_analyze[i])
    print("Analyse", number_of_homeworks, "homeworks.............")

    data = { 'document' : [],
             'complexity' : [],
            'length_of_chunk' : [],
            'number_of_chunk' : [],
            'GFI' : []}

    variances = {'length_of_chunk': [],
                 'complexity' : [],
                 'variance': [],
                 'std' : []}

    # analyse each homework
    for k, homework in enumerate(theses_to_analyze[i]):
        print("Analysing homework", k+1, "of", len(theses_to_analyze[i]))
        # try different complexities
        for x in [3, 4, 5]:
            percentage_of_complex_words = []
            for m in [0, 200, 150, 100, 90, 80, 70, 60, 50, 45, 40, 35, 30, 28, 26, 24, 22, 20, 18, 16, 14, 12, 10]:
                process(homework, m, x)
            #print(np.median(percentage_of_complex_words))


    print("The analysis of this folder is finished. \nStoring data.............")

    # convert the dictionary with the data to a dataframe
    df = pd.DataFrame(data=data)
    # remove duplicate rows (they exist due to m going down from a high number to a low number)
    df = df.drop_duplicates(keep='first')

    # write the collected data into csv-files
    data_out = open("Results/results_" + str(i) + ".csv", "w")
    # convert the data to a csv and write it into the given file
    data_out.write(df.to_csv())
    data_out.close()

    # store variances
    data_out = open("Results/variancesHomework_" + str(i) + ".csv", "w")
    df_var = pd.DataFrame(variances)
    data_out.write(df_var.to_csv())
    data_out.close()

    print("The collected data has been written to 'Results/results_i.csv' and 'Results/variancesHomework_i.csv'. \nGo, have a look!")

print("Completely finished.")

sys.exit()