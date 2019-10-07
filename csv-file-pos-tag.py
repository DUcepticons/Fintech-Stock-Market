
import nltk
import csv
Tagged_list= []
T =()
news=[]
#sentence = "Stocks rebound riding on GP. A leading broker said bargain hunters showed their appetite on selective large-cap shares, particularly on heavyweight GP, amid positive news surrounding the GP."
PerNewsTags = []
expected_pos = ["JJ","JJR","JJS","NNS","RB","RBR","RBS","VB","VBD","VBG","VBN","VBP","VBZ"]
cut_out = ["'s","s", '+0.08','in', '13-week', '2015-16', '2018-19', '2019-20', '27-member', '4,800-mark', '4-month','up1.9', '5th', '6,100-mark', '6,200-mark', '72.1percent', 'a11.8','–', '’', '“', '”', 'is', 'be', 'has','are','been','have','did','was','tk','also','said','till','soon','then','yet','had','were']

with open('GP-Square-Pharma-2010-2019.csv',encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
    	word_token = nltk.word_tokenize(row["News"])
    	news.append(row["News"])
    	token = nltk.pos_tag(word_token)				#All tagged list in [(word,tag),(word,tag),...] format
    	for t in token:
    		for exp in expected_pos:
    			if t[1]==exp:							#Checking tags.Where t[1] is the 2nd element from tuple (word,tag)
    				T=T + (t[0].lower(),)+(exp,)		#taking everything in lower case,otherwise starting and middle words will be considered different				
    				if T[0] not in cut_out:
    					Tagged_list.append(T)	
    				T = ()
    	PerNewsTags.append(Tagged_list)
    	Tagged_list = []

with open('Result.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["News","Tagged News"])
    for i in range(len(PerNewsTags)):
    	writer.writerow([news[i],PerNewsTags[i]])
    

# We took JJ JJR JJS NNS RB RBR RBS VB VBD VBG VBN VBP VBZ IN 
# where 
# JJ: adjective or numeral, ordinal
# JJR: adjective, comparative
# JJS: adjective, superlative
# NNS: noun, proper, singular
# RB: adverb
# RBR: adverb, comparative
# RBS: adverb, superlative
# VB: verb, base form
# VBD: verb, past tense
# VBG: verb, present participle or gerund
# VBN: verb, past participle
# VBP: verb, present tense, not 3rd person singular
# VBZ: verb, present tense, 3rd person singular
# IN: preposition or conjunction, subordinating
