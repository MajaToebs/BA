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


# how to run: python fogMaja.py nameOfDataFile.py nameOfTokenizer(either nltk or spacy) numberOfSyllablesToCountAWordAsComplex

# !/usr/bin/python3
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

#import nltk
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

# set of easy words to get complicated ones
from textstat.textstat import easy_word_set

# for hyphenization
from pyphen import Pyphen

# file I/O
import sys
from io import open


# tokenize a text into alphabetical words
def word_tokenizing(text):
    # tokenize words and filter out punctuations, numbers etc (non-alpha)
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
    #print("//The number of words this sentence contains is: " + str(len(tokenized_words)))
    return tokenized_words


# count syllables
def count_syllables(word):
    # necessary for the syllable count
    dic = Pyphen(lang='en_EN')
    word_hyphenated = dic.inserted(word)
    count = max(1, word_hyphenated.count("-") + 1)
    return count


# get complex words out of all words
def get_complex_words(words):
    # difficult words are those with syllables >= 2
    # easy_word_set is provided by Textstat as
    # a list of common words
    diff_words_set = []

    for word in words:
        syllable_count = count_syllables(word)

        # word not in easy set and longer than 3 syllables
        if word not in easy_word_set \
                and syllable_count >= complexity:
            # word not a verb with 3 syllables that ends in -ed or -es (would usually have only 2 syllables)
            # if word.endswith("ed") == False or word.endswith("es") == False \
            # and syllable_count > 3 \
            # and nltk.tag.pos_tag([word])[0][1].startswith("V"):
            # no proper nouns
            # if nltk.tag.pos_tag([word])[0][1] is not "NNP":
            diff_words_set.append(word)
    print("//Wow! The number of complex words this text contains is: ", len(diff_words_set))
    return diff_words_set


def analyse(i, sentences):
    tokenized_words = []
    for sent in sentences:
        words = word_tokenizing(sent)
        tokenized_words.extend(words)
    print("//The number of tokenized words in this text is", len(tokenized_words))

    # Determine average sentence length
    average_sentence_length = len(tokenized_words) / len(sentences)
    print("//Chunk", i, "contains an average of ", round(average_sentence_length, 2), " words per sentence")

    diff_words_set = get_complex_words(tokenized_words)

    # print the percentage of complex words
    diff_word_freq = len(diff_words_set) / len(tokenized_words) * 100
    print("//The frequency of big words in chunk", i, "is", round(diff_word_freq, 2), "%")

    # calculate the fog index
    fog = (diff_word_freq + average_sentence_length) * 0.4

    print("//The Gunning Fog Index in chunk", i, "is: ", round(fog, 2), "\n")
    return fog



# read in all parameters
if len(sys.argv) == 5:
    filename = sys.argv[1]
    tokenizer = sys.argv[2]
    complexity = int(sys.argv[3])
    sentences_per_chunk = int(sys.argv[4])
else:
    filename = input("Please enter the path of the file whose reading level you would like to assess.\n")
    tokenizer = input("Please enter the type of the tokenizer you would like to use (nltk or spacy).\n")
    complexity = int(input("Please enter the minimum number of syllables to count a word as a complex word.\n"))
    sentences_per_chunk = int(input("Please enter the minimum number of sentences one chunk should contain.\nIf you enter 0, the whole document will be assessed.\n"))

# read in the document
with open(filename, "r", encoding="utf-8-sig") as raw:
    text_in = raw.read().replace("\n", " ")
    raw.close()
print("//File:", filename)
print("//Minimum number of syllables for a word to be considered complex:", complexity)
print("//Minimum number of sentences per chunk:", sentences_per_chunk, "\n")

# tokenize the text into sentences with nltk and then print how many there are
sentences = sent_tokenize(text_in)
print("//The number of sentences this text contains is: ", str(len(sentences)), "\n")

# store all fog indices of the different chunks
fog_indices = []

# the user wants to analyse the whole text
if sentences_per_chunk == 0:
    fog_indices.append(analyse(0, sentences))
else:
    n = len(sentences)/sentences_per_chunk
    for i in range(1, int(n+1)):
        chunk_i = sentences[(i-1)*sentences_per_chunk:i*sentences_per_chunk]
        fog_indices.append(analyse(i, chunk_i))

# final print
print("//The average Gunning Fog Index in this document is", round(sum(fog_indices)/len(fog_indices),2))
print("//The analysis is finished.")







# Output Reading Level
# if fog < 6: print("Yikes! It looks like a child wrote this. The reading level for this document is below grade six.")
# elif fog <=6.9: print("The reading level for this document is grade six.")
# elif fog <=7.9: print("The reading level for this document is grade seven.")
# elif fog <=8.9: print("The reading level for this document is grade eight.")
# elif fog <=9.9: print("The reading level for this document is grade nine.")
# elif fog <=10.9: print("The reading level for this document is grade ten.")
# elif fog <=11.9: print("The reading level for this document is grade eleven.")
# elif fog <=12.9: print("The reading level for this document is grade twelve.")
# elif fog  <=13.9: print("The reading level for this document is that of a college freshman.")
# elif fog  <=14.9: print("The reading level for this document is that of a college junior.")
# elif fog  <=15.9: print("The reading level for this document is that of a college sophmore.")
# elif fog  <=16.9: print("The reading level for this document is that of a college senior.")
# elif fog  >=17: print("Wow! The reading level for this document is that of a college graduate.")


sys.exit()


