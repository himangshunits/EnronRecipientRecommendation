#load all directories
#This program was run as a test code for testing tfidf centroid for test users.
#It is a combination of GetVocab.py and testingtfidf.py
#The result from trainingtfidf.py is stored in a numpy array called array.npy
from __future__ import division
import mysql.connector
import math
import decimal
import string
import numpy
import getVocab
import mysql.connector
import scipy.sparse
import scipy
import numpy
from scipy import spatial

def getArray():
	tfidf = numpy.load(open('array.npy','rb'))
	return tfidf

usefulWords = []

	
def getPredictions(message):
	tfidfCentroids = getArray()


	
	cnx = mysql.connector.connect(user='root', database='enron4',password='root',host='localhost')
	cursor = cnx.cursor();
	cursor.execute("select distinct term from document_term")
	for each in cursor:
		usefulWords.append(each[0])

	cleaned_data = getVocab.getAccurateCleanedData(message, usefulWords)
	return cleaned_data
			


'''
	word_features=vectorizer.fit_transform(cleaned_data);
    a=word_features.getrow(0).toarray()

    vocab = vectorizer.get_feature_names()

    vocabSet = set(vocab)
    usefulSet = set(usefulWords)
    print vocabSet
    print usefulSet

    resultSet = vocabSet & usefulSet'''


from sklearn.feature_extraction.text import CountVectorizer

cleaned_data= getPredictions("Sushma is awesome! enron message message www thanks")
vectorizer = CountVectorizer(analyzer = "word",tokenizer = None,preprocessor = None,stop_words = None)    
word_features=vectorizer.fit_transform(cleaned_data);
a=word_features.getrow(0).toarray()

vocab = vectorizer.get_feature_names()
print "vocab is ", vocab

a=scipy.sparse.find(word_features)
vals=a[2]
print vals
#bag_of_words=list(usefulSet)
#print type(bag_of_words[0])
bag_of_words=usefulWords
###############################################
    
#vocab = [u'agreement', u'change', u'company', u'energy', u'follow', u'inc', u'note', u'please', u'remain', u'sale', u'service', u'713', u'853', u'book', u'contact', u'date', u'dave', u'follow', u'houston', u'include', u'sushma', u'sukriti', u'himangshu']
#vals = [1,12,20,8,9,13,2,10,4,5,6,7,14,15,3,18,19,16,17,11,3,7,8]
Vocab = []
Values = []
i = -1
for each in vocab:
    i = i + 1
    for every in bag_of_words:
        if each == every:
            Vocab.append(each)
            Values.append(vals[i])
            
            
no_of_terms = len(Vocab)

term_vector = [0 for x in range(len(bag_of_words))]
i = 0
temp = []
tfidf = []
sumoftfidf = 0
for each in Vocab:
    ftd = math.log(1 + (Values[i]/no_of_terms))
    idf = math.log(1 + 1/Values[i])
    temp = float(ftd) * float(idf)
    tfidf.append(temp)
    i = i + 1

for each in tfidf:
    sumoftfidf = sumoftfidf + each

i = 0
for each in Vocab:
    term_vector[bag_of_words.index(each)] = tfidf[i]/sumoftfidf
    print term_vector[bag_of_words.index(each)]
    i = i + 1 

training_Set=numpy.load(open('array.npy','rb'))
#print training_Set[1]
fp = open('UsersFiltered3319.txt', 'r')
lines = fp.readlines()
userslist = []
for each in lines:
    userslist.append(each[(each.find('\t') + 2):-2])
print userslist[0]


Cosine_similarity=[]
i=-1
for each in training_Set:
    i=i+1
    result=1-spatial.distance.cosine(each,term_vector)
    Cosine_similarity.append(result)
print "answer",Cosine_similarity[0]
