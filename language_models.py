import tkinter as tk
from collections import Counter
import re
import os

print("Loading corpus...")
re_pattern = r'\b[a-zA-Z0-9\-\'\*]+\b|[\.\?\!]'
directory = [
	#"data/corpus/Joji's BALLAD Song Lyrics",
	#"data/corpus/Duturte's Speeches",
	#"data/corpus/DLSU Student Publications",
	#"data/corpus/Journal Articles"
	"data/corpus/LSCS"
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
		matrix[word1][word2] = 0

for text in text_files:
	tokens = text['Tokens']
	
	for i in range(len(tokens)-1):
		matrix[tokens[i]][tokens[i+1]] += 1

for word1 in total_vocabulary:
	sum_mat = sum(matrix[word1].values())
	for word2 in total_vocabulary:
		matrix[word1][word2] = matrix[word1][word2]/sum_mat

root = tk.Tk()
root.resizable(False, False)
root.title("INTRNLP - PE#3")
text1 = tk.Text(root, height=20, width=60)
text1.configure(font=("Cambria", 12))
text1.grid(row=0, column=0, padx=(10, 10), pady=(5, 5))

text2 = tk.Text(root, height=20, width=30)
text2.configure(font=("Cambria", 12), state=tk.DISABLED)
text2.grid(row=0, column=1, padx=(10, 10), pady=(5, 5))

def press(event):
    text2.configure(state=tk.NORMAL)
    string = text1.get(1.0, tk.END)
    text2.delete(1.0, tk.END)

    token = re.findall(re_pattern, string.lower())
    if (len(token) >= 1):
        string = token[len(token) - 1]

        if (string in matrix.keys()):
            sorted_x = sorted(matrix[string].items(), key=lambda kv: kv[1])
            sorted_x.reverse()

            messages = "Suggested Words: \n"
				
            for tuples in sorted_x: messages += "{}: {:.2f}%\n".format(tuples[0], tuples[1]*100)
            text2.insert(1.0, messages)
        
    text2.configure(state=tk.DISABLED)

text1.bind('<KeyRelease>', press)

tk.mainloop()
