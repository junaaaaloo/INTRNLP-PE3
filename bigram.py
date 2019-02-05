from collections import Counter
import re
import os

print("Loading corpus...")
re_pattern = r'\b[a-zA-Z0-9\-\'\*]+\b|[\.\?\!]'
directory = [
	"Joji's BALLAD Song Lyrics",
	"Duturte's Speeches",
#	"DLSU Student Publications",
#	"Journal Articles"
]
text_files = []
term_counter = Counter()
for folder in directory:
	file_names = os.listdir(folder)

	for file_name in file_names[:]:
		with open(folder + "/" + file_name, 'r', encoding='utf8') as f:
			title = file_name[:-4]
			temp = {
				"Title": title,
				"Raw Text": f.read()
			}
			temp['Tokens'] = re.findall(re_pattern, temp["Raw Text"].lower())
			temp['Vocabulary'] = list(set(re.findall(re_pattern, temp["Raw Text"].lower())))
			
			print("===%s===" % title)
			print("Total tokens: %s" % len(temp['Tokens']))
			print("Total vocabulary: %s" % len(temp['Vocabulary']))

			text_files.append(temp)
			term_counter.update(temp['Tokens'])

print("Identifying vocabulary...")
# Find vocabulary set
total_vocabulary = set()
for song in text_files:
	total_vocabulary |= set(song['Vocabulary'])
total_vocabulary = list(total_vocabulary)
vocabulary_count = len(total_vocabulary)
print("Vocabulary count: %s" % vocabulary_count)
print(total_vocabulary)

print("--------")

matrix = {}

for word1 in total_vocabulary:
	matrix[word1] = {}
	for word2 in total_vocabulary:
		matrix[word1][word2] = {}
		for word3 in total_vocabulary:
			matrix[word1][word2][word3] = {}

for text in text_files:
	tokens = text['Tokens']
	
	for i in range(len(tokens)-2):
		matrix[tokens[i]][tokens[i+1]][tokens[i+2]] += 1

import operator

string = "hello"
while (string != ""):
	string = input("Input: ")
	if (string in matrix.keys()):
		sorted_x = sorted(matrix[string].items(), key=lambda kv: kv[1])
		sorted_x.reverse()
		for key, value in sorted_x:
			if (value != 0): print("{}: {}".format(key, value))
