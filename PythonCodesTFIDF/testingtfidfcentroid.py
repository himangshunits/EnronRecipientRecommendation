#The code below is one of the versions of testing created before combing it to geTtfidfArrays.py
#A sample variable vocab is used to store a sample set of words from a document
from __future__ import division
import mysql.connector
import math
import decimal
import string

####CAN BE AVOIDED IF WORKSPACE IS SAVED
bag_of_words = []
cnx = mysql.connector.connect(user='sushma', database='enron4',password='Sushma26011993',host='localhost')
cursor = cnx.cursor();
cursor.execute("select distinct term from document_term")
for each in cursor:
    bag_of_words.append(each[0])

########################################
    
vocab = [u'agreement', u'change', u'company', u'energy', u'follow', u'inc', u'note', u'please', u'remain', u'sale', u'service', u'713', u'853', u'book', u'contact', u'date', u'dave', u'follow', u'houston', u'include', u'sushma', u'sukriti', u'himangshu']
vals = [1,12,20,8,9,13,2,10,4,5,6,7,14,15,3,18,19,16,17,11,3,7,8]
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
#Calculates the tfidf score of all the terms in the sample document
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
    i = i + 1 

