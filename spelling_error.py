from collections import Counter
import re
import os
from time import time


def log(message):
    print("[{}] {}".format(time.strftime(
        "%Y-%m-%d %H:%M:%S", time.time()), message))


def load_corpus(directory):
    text_files = []
    term_counter = Counter()

    log("Loading corpus")
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

                print("===%s===" % title)
                print("Total tokens: %s" % len(temp['Tokens']))
                print("Total vocabulary: %s" % len(temp['Vocabulary']))

                text_files.append(temp)
                term_counter.update(temp['Tokens'])
    log("Loading corpus: Done!")
    return text_files, term_counter


def identify_vocabulary(text_files):
    total_vocabulary = set()
    for song in text_files:
        total_vocabulary |= set(song['Vocabulary'])
    total_vocabulary = list(total_vocabulary)
    print("Vocabulary count: {}".format(len(total_vocabulary)))
    return total_vocabulary
