from collections import Counter
import re
import os
from time import time

def log(message):
    print("[{}] {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.time()), message))


def load_corpus(directory):
    text_files = []
    term_counter = Counter()

    # print("Loading corpus")
    re_pattern = r'\b[a-zA-Z0-9\-\'\*]+\b|[\.\?\!]'

    for folder in directory:
        file_names = os.listdir(folder)

        for file_name in file_names[:]:
            with open(folder + "/" + file_name, 'r', encoding='utf8') as f:
                title = file_name[:-4]
                temp = {
                    "Title": title,
                    "Raw Text": f.read()
                }
                temp['Tokens'] = re.findall(
                    re_pattern, temp["Raw Text"].lower())
                temp['Vocabulary'] = list(
                    set(re.findall(re_pattern, temp["Raw Text"].lower())))

                # print("===%s===" % title)
                # print("Total tokens: %s" % len(temp['Tokens']))
                # print("Total vocabulary: %s" % len(temp['Vocabulary']))

                text_files.append(temp)
                term_counter.update(temp['Tokens'])
    # print("Loading corpus: Done!")
    return text_files, term_counter


def identify_vocabulary(text_files):
    total_vocabulary = set()
    for song in text_files:
        total_vocabulary |= set(song['Vocabulary'])
    total_vocabulary = list(total_vocabulary)
    # print("Vocabulary count: {}".format(len(total_vocabulary)))
    return total_vocabulary


w = input("Input: ")

directory = [
    "data/corpus/Joji's BALLAD Song Lyrics",
    "data/corpus/Duturte's Speeches",
    "data/corpus/DLSU Student Publications",
    "data/corpus/Journal Articles",
    "data/corpus/LSCS"
]

text_files, term_counter = load_corpus(directory)

total_vocabulary = identify_vocabulary(text_files)

# total_vocabulary2 = Counter(dict(text_files,term_counter))

# print(term_counter)

def P(word, N=sum(term_counter.values())):
    "Probability of `word`."
    return term_counter[word] / N


def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)


def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or [word])


def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in total_vocabulary)


def edits1(word):
    "All edits that are one edit away from `word`."
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


# def edits2(word):
#     "All edits that are two edits away from `word`."
#     return (e2 for e1 in edits1(word) for e2 in edits1(e1))

print("Output: ")

if w in total_vocabulary:
    print("No error")
else:
    for word in candidates(w):
        print(word)
        print(P(word))
    print(correction(w))


