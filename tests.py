
'''
text = "Dies ist ein Satz, der aus 10 Woertern und Sub-stantiven besteht."

# import spacy with the English module
import spacy
nlp = spacy.load("en_core_web_sm")

tokenized_words = nlp(text)
print(tokenized_words)
    # is_alpha takes only tokens which do not contain spaces or digits
tokenized_words = [token.text.lower() for token in tokenized_words if token.is_alpha == True]
print(tokenized_words)
print(len(tokenized_words))


from nltk.tokenize import word_tokenize
tokenized_words = word_tokenize(text)
print(tokenized_words)

from string import ascii_letters
withoutNumbers = []
for word in tokenized_words:
    word = word.lower()
    if all(c in ascii_letters+'-' for c in word):
        withoutNumbers.append(word)

tokenized_words = withoutNumbers

print(tokenized_words)
'''

text2 = "Erster Satz. Und es folgt ein zweiter Satz. Und ein dritter. \
        Und auch noch ein vierter! Und Nummer 5, plumbum: Ist das Nummer 6?"
from nltk.tokenize import sent_tokenize
print(sent_tokenize(text2))

print(int(2.8))

list1 = ['bla', 'bli']

list2 = ['blub']
list1.extend(list2)
print(list1)

import os
names_of_theses = []
for i in os.listdir('PreprocessedData/thesis/'):
    names_of_theses.append(i)
print(names_of_theses)