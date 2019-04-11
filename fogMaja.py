# coding: utf-8

# # Gunning Fog Calculator
# The purpose of this calculator is to determine the readability of a text. Readability is defined as the level of education an individual needs to understand a text on the first reading.
# Gunning Fog is calculated by adding the average sentence length to the percentage of difficult words (words comprising of 3 or more syllables) multiplied by 0.4.
# This program opens a file, calculates the number of words, sentences, average number of words per sentence and the percentage of difficult words in the overall text before outputting a reading level the text is assigned to. For the curious, difficult words in a text are also printed.
# For more information on Gunning Fog: http://www.readabilityformulas.com/gunning-fog-readability-formula.php
# the slight difference in results from online calculators is probably due to the count of complex words

# !/usr/bin/python3
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import sys, imp
import nltk
#nltk.download('punkt') #only DL if don't already have
#nltk.download('popular')

# used to get individual words and sentences

from nltk.tokenize import sent_tokenize

# set of easy words to get complicated ones
from textstat.textstat import easy_word_set

# file I/O
import sys

# word tokenization
import spacy
nlp = spacy.load("en_core_web_sm")

filename = sys.argv[1]

from io import open

# r = input("Please enter the path of the file whose reading level you would like to assess")

with open(filename, "r", encoding="utf-8-sig") as raw:
    text = raw.read().replace("\n", " ")

# newer version above
# raw = open(filename, "+r", encoding="utf-8-sig")
# text = raw.read()
# raw.close()

# tokenize sentence and then print how many there are
sentences = sent_tokenize(text)
print("//The number of sentences this text contains is: " + str(len(sentences)))

# tokenize words, then print how many there are
#word_tokenize_list = (word_tokenize(text))
# filter out punctuation old
#word_tokenize_list = [word for word in word_tokenize_list if word.isalpha()]

# tokenize words and filter out punctuations, numbers etc (non-alpha)
tokenized_words = nlp(text)
# is_alpha takes only tokens which do not contain spaces or digits
tokenized_words = [token.text for token in tokenized_words if token.is_alpha == True]

print("//The number of words this text contains is: " + str(len(tokenized_words)))

# Determine average sentence length
avgSent = len(tokenized_words) / len(sentences)
# print("//This text contains an average of " + x[:5] + " words per sentence")
print("//This text contains an average of ", avgSent, " words per sentence")


# count syllables
def syllables(word):
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count += 1
    if count == 0:
        count += 1
    return count

# EDIT: better use only words without non-alpha chars
# Return total Difficult Words in a text
#words = nltk.tokenize.word_tokenize(text)


# difficult words are those with syllables >= 2
# easy_word_set is provided by Textstat as
# a list of common words
diff_words_set = []

for word in tokenized_words:
    syllable_count = syllables(word)

    # word not in easy set and longer than 3 syllables
    if word not in easy_word_set \
            and syllable_count >= 3:
        # word not a verb with 3 syllables that ends in -ed or -es (would usually have only 2 syllables)
        if word.endswith("ed") == False or word.endswith("es") == False \
                and syllable_count > 3 \
                and nltk.tag.pos_tag([word])[0][1].startswith("V"):
            # no proper nouns
            if nltk.tag.pos_tag([word])[0][1] is not "NNP":
                diff_words_set.append(word)



print("//Wow! The number of big words this text contains is: ", len(diff_words_set))

#print the percentage of big words
diff_word_freq = len(diff_words_set) / len(tokenized_words) * 100
print("//The frequency of big words in this document is", round(diff_word_freq, 2), "%")

fog = (diff_word_freq + avgSent) * 0.4

print("//The Gunning Fog Index in this document is: ", round(fog,2))
print(fog)
'''
#count the number of big words
bigwords = []
for x in word_tokenize_list:
    #print(syllables(x))
    if syllables(x) >= 3:
       bigwords.append(x) 
'''

# Output Reading Level
# if fog < 6: print("Yikes! It looks like a child wrote this. The reading level for this document is below grade six.")


# Grade School Cases
# elif fog <=6.9: print("The reading level for this document is grade six.")
# elif fog <=7.9: print("The reading level for this document is grade seven.")
# elif fog <=8.9: print("The reading level for this document is grade eight.")
# elif fog <=9.9: print("The reading level for this document is grade nine.")
# elif fog <=10.9: print("The reading level for this document is grade ten.")
# elif fog <=11.9: print("The reading level for this document is grade eleven.")
# elif fog <=12.9: print("The reading level for this document is grade twelve.")

# College Cases

# elif fog  <=13.9: print("The reading level for this document is that of a college freshman.")
# elif fog  <=14.9: print("The reading level for this document is that of a college junior.")
# elif fog  <=15.9: print("The reading level for this document is that of a college sophmore.")
# elif fog  <=16.9: print("The reading level for this document is that of a college senior.")

# University Graduate Level
# elif fog  >=17: print("Wow! The reading level for this document is that of a college graduate.")


sys.exit()


