#will implement it with pandas next

import nltk
import csv
from numpy import unique

Tagged_list= []
T =()
news=[]
All_words = []

expected_pos = ["JJ","JJR","JJS","NNS","RB","RBR","RBS","VB","VBD","VBG","VBN","VBP","VBZ"]  # NN ta katlam
cut_out = ['is', 'be', 'has','are','been','have','did','was','tk','also','said','till','soon','then','yet',"n't","'s","s", '+0.08', '13-week', '2015-16', '2018-19', '2019-20', '27-member', '4,800-mark', '4-month','up1.9', '5th', '6,100-mark', '6,200-mark', '72.1percent', 'a11.8','–', '’', '“', '”']

with open('GP-Square Pharma 2010-2019.csv',encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
    	word_token = nltk.word_tokenize(row["News"])
    	news.append(row["News"])
    	token = nltk.pos_tag(word_token)				#All tagged list in [(word,tag),(word,tag),...] format
    	for t in token:
    		for exp in expected_pos:
    			if t[1]==exp:							#Checking tags.Where t[1] is the 2nd element from tuple (word,tag)
    				T=T + (t[0],)+(exp,)
    				Tagged_list.append(T)
    				if T[0] not in cut_out:
    					All_words.append(T[0].lower())	#taking everything in lower case,otherwise starting and middle words will be considered different
    				T = ()

All_words = list(unique(All_words))

pattern = []
All_words.append("Binary Score")# add binary score column
with open('Dataset Matrix.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(All_words)
    del All_words[-1]#delete Binary Score after writing in column
    with open('GP-Square Pharma 2010-2019.csv',encoding="utf-8") as file:
    	reader = csv.DictReader(file, delimiter=',')
    	for row in reader:
    		for word in All_words:
    			pattern.append("1") if word in row["News"].lower() else pattern.append("0")
    		pattern.append(row["Binary Score"])
    		writer.writerow(pattern)
    		pattern = []
    		



#print(Tagged_list)
# print(All_words)
print(len(All_words))