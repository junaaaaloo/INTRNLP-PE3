from collections import Counter
import re
import os
import datetime
import time
import tkinter as tk
from utils.logger import log
import numpy as np

DEBUG = False
def log(message, debug_bypass = False):
    global DEBUG;
    if (DEBUG and not debug_bypass):
        print("[{}] {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))

def load_corpus(directory):
    text_files = []
    term_counter = Counter()

    log("Loading corpus")
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

                log("===%s===" % title)
                log("Total tokens: %s" % len(temp['Tokens']))
                log("Total vocabulary: %s" % len(temp['Vocabulary']))

                text_files.append(temp)
                term_counter.update(temp['Tokens'])

    log("Loading corpus: Done!")
    return text_files, term_counter

def load_matrix (matrix_directory):
    text_file = ""

    f = open(matrix_directory, 'r', encoding='utf8')
    
    lines = f.readlines()
    matrix = {}
    for line in lines:
        attr = (line.split("\t"))

        mistake, correct = attr[0].split("|")
        count = int(attr[1])
        
        if (mistake in matrix):
            if (correct in matrix[mistake]):
                matrix[mistake][correct] = count;
            else:
                matrix[mistake].update({correct: count})
        else:
            matrix[mistake] = {
                correct: count
            }
        
    return matrix

def identify_vocabulary(text_files):
    total_vocabulary = set()
    for song in text_files:
        total_vocabulary |= set(song['Vocabulary'])
    total_vocabulary = list(total_vocabulary)
    log("Vocabulary count: {}".format(len(total_vocabulary)))
    return total_vocabulary

directory = [
    "data/corpus/Joji's BALLAD Song Lyrics",
    "data/corpus/Duturte's Speeches",
    "data/corpus/DLSU Student Publications",
    "data/corpus/Journal Articles",
    "data/corpus/LSCS",
	"data/corpus/MASC"
]
matrix_directory = "data/confusion_matrix.txt"

text_files, term_counter = load_corpus(directory)

matrix = load_matrix(matrix_directory)
total_vocabulary = identify_vocabulary(text_files)

def P(word, N=sum(term_counter.values())):
    "Probability of `word`."
    return term_counter[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([{'word': word, 'error_probability': 0}]) or known(edits1(word))) or [word]

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return list(w for w in words if w['word'] in total_vocabulary)

def find_matrix (x, y):
    global matrix

    if (x in matrix):
        if (y in matrix[x]):
            return matrix[x][y]/sum([matrix[x][i] for i in matrix[x]])
            
    return 0

def edits1(word):
    "All edits that are one edit away from `word`."
    letters = 'abcdefghijklmnopqrstuvwxyz'

    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [{'word': L + R[1:], 'error_probability': find_matrix(R[0], ' ')} for L, R in splits if R]
    transposes = [{'word': L + R[1] + R[0] + R[2:], 'error_probability': find_matrix(R[0] + R[1], R[1] + R[0])} for L, R in splits if len(R) > 1]
    replaces = [{'word': L + c + R[1:], 'error_probability': find_matrix(R[0], c)} for L, R in splits if R for c in letters]
    inserts = [{'word': L + c + R, 'error_probability': find_matrix(' ', c)} for L, R in splits for c in letters]
    return list(deletes + transposes + replaces + inserts)

# def edits2(word):
#     "All edits that are two edits away from `word`."
#     return (e2 for e1 in edits1(word) for e2 in edits1(e1))

# input_word = input("Input: ")
# print("Output: ")

# if input_word in total_vocabulary:
#     print("No error")
# else:
#     candidates_probabilities = []
#     for word in candidates(input_word):
#         candidates_probabilities.append({
#             "word": word,
#             "probability": P(word)
#         })
    
#     candidates_probabilities = sorted(candidates_probabilities, key=lambda k: 1-k['probability'])
#     count = 0
#     for candidate in candidates_probabilities:
#         print("{}{}: {}".format("" if count != 0 else "*", candidate["word"], candidate["probability"]))
#         count += 1


root = tk.Tk()
root.resizable(False, False)
root.title("INTRNLP - PE#3")

label1 = tk.Label(root, justify = "left", anchor="e", text="Type a word:", font=("Lucida Sans Typewriter", 12))
label1.grid(row=0, column=0, padx=(10, 10), pady=(5, 5))

text1 = tk.Text(root, height=1, width=40, font=("Lucida Sans Typewriter", 12))
text1.grid(row=1, column=0, padx=(10, 10), pady=(5, 5))

label2 = tk.Label(root, justify = "left", anchor="e", text="Suggestions:", font=("Lucida Sans Typewriter", 12))
label2.grid(row=2, column=0, padx=(10, 10), pady=(5, 5))

label3 = tk.Label(root, justify = "left", anchor="e", text="* - Suggested Word", font=("Lucida Sans Typewriter", 12))
label3.grid(row=3, column=0, padx=(10, 10), pady=(5, 5))

text2 = tk.Text(root, height=5, width=40, font=("Lucida Sans Typewriter", 12), state=tk.DISABLED)
text2.grid(row=4, column=0, padx=(10, 10), pady=(5, 5))

label4 = tk.Label(root, justify = "left", anchor="e", text="Error", font=("Lucida Sans Typewriter", 12))
label4.grid(row=5, column=0, padx=(10, 10), pady=(5, 5))

text3 = tk.Text(root, height=5, width=40, font=("Lucida Sans Typewriter", 12), state=tk.DISABLED)
text3.grid(row=6, column=0, padx=(10, 10), pady=(5, 5))

label5 = tk.Label(root, justify = "left", anchor="e", text="Frequency", font=("Lucida Sans Typewriter", 12))
label5.grid(row=7, column=0, padx=(10, 10), pady=(5, 5))

text4 = tk.Text(root, height=5, width=40, font=("Lucida Sans Typewriter", 12), state=tk.DISABLED)
text4.grid(row=8, column=0, padx=(10, 10), pady=(5, 5))

def press(event):
    text2.configure(state=tk.NORMAL)
    text3.configure(state=tk.NORMAL)
    text4.configure(state=tk.NORMAL)
    input_word = text1.get(1.0, tk.END)
    text2.delete(1.0, tk.END)
    text3.delete(1.0, tk.END)
    text4.delete(1.0, tk.END)

    re_pattern = r'\b[a-zA-Z0-9\-\'\*]+\b|[\.\?\!]'
    token = re.findall(re_pattern, input_word.lower())
    
    if token == [] or token[0] in total_vocabulary:
        text2.insert(1.0, "No error")
        text3.insert(1.0, "No error")
        text4.insert(1.0, "No error")
    else:
        candidates_probabilities = []
        for word in candidates(token[0]):
            candidates_probabilities.append({
                "word": word['word'],
                "error_probability": word['error_probability'],
                "word_probability": P(word['word'])
            })
        
        candidates_probabilities = sorted(candidates_probabilities, key=lambda k: 1-(k["error_probability"] * k["word_probability"]))
        count = 0
        message = ""

        for candidate in candidates_probabilities:
            message += ("{}{} ({}%)\n".format("" if count != 0 else "*", candidate["word"], candidate["error_probability"] * candidate["word_probability"]))
            count += 1

        text2.insert(1.0, message)

        candidates_probabilities = sorted(candidates_probabilities, key=lambda k: 1-(k["error_probability"]))
        count = 0
        message = ""

        for candidate in candidates_probabilities:
            message += ("{}{} ({}%)\n".format("" if count != 0 else "*", candidate["word"], candidate["error_probability"]))
            count += 1
        
        text3.insert(1.0, message)

        candidates_probabilities = sorted(candidates_probabilities, key=lambda k: 1-(k["word_probability"]))
        count = 0
        message = ""

        for candidate in candidates_probabilities:
            message += ("{}{} ({}%)\n".format("" if count != 0 else "*", candidate["word"], candidate["word_probability"]))
            count += 1
        text4.insert(1.0, message)
        
    text2.configure(state=tk.DISABLED)
    text3.configure(state=tk.DISABLED)
    text4.configure(state=tk.DISABLED)

text1.bind('<KeyRelease>', press)



tk.mainloop()