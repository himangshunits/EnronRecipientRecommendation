##The aim of the code is to calculate the tfidf-centroid for each of the users in the recipient list
##The body of each email is preprocessed and represented as a table called the document_term table
##Each row in the document_term table is as follows:
#1. The document number representaing an id given to each email (N)
#2. The term (T) in the document (N)
#3. A raw count of the number of times term T was found in document N

#load directories
from __future__ import division
import mysql.connector
import math
import decimal
import string
cnx = mysql.connector.connect(user='sushma', database='enron4',password='Sushma26011993',host='localhost')
cursor = cnx.cursor();
cursor.execute("select count(distinct number) from document_term")
#Counts the total number of distinct documents in the dataset
for each in cursor:
  no_of_docs = each[0]


tfidf = []
doc_total_terms = {}
cnx = mysql.connector.connect(user='sushma', database='enron4',password='Sushma26011993',host='localhost')
cursor = cnx.cursor();
cursor.execute("SELECT number, sum(count) from document_term group by number");
#Counts the total number of terms per document
for each in cursor:
    doc_total_terms[each[0]] = each[1]


term_occurence = {} #Holds the value n(t)

cursor.execute("select term, count(*) from document_term group by term");
for each in cursor:
    term_occurence[each[0]] = each[1]

cnx = mysql.connector.connect(user='sushma', database='enron4',password='Sushma26011993',host='localhost')
cursor = cnx.cursor();
###Calculates the Document Term Weight
### (f(t,d) *  log(N/n(t)))
cursor.execute("SELECT * from document_term");
for each in cursor:
    temp = []
    ftd = math.log(1 + (each[2]/doc_total_terms[each[0]]))
    idf = math.log((no_of_docs/term_occurence[each[1]]), 10)
    temp.append(each[0])
    temp.append(each[1])
    temp.append(float(ftd) * float(idf))
    tfidf.append(temp)

#Normaliding the tfidf scores
#sumoftfidf[] contains the toal of tfidf scores per document
i = tfidf[0][0]
sumoftfidf = []
tempsum = 0
for each in tfidf:
    if each[0] == i:
        tempsum = tempsum + each[2]
    else:
        i = each[0]
        sumoftfidf.append(tempsum)
        tempsum = each[2]
sumoftfidf.append(tempsum)
#document vector is a matrix with three values in each row:
#1. The document number (N)
#2. The term (T) in the document (N)
#3. The normalised tfidf score of T in N

document_vector = {}
i = tfidf[0][0]
count = 0
for each in tfidf:
	temp = []
	if each[0] == i:
	        temp.append(each[2]/sumoftfidf[count])
	else:
		i = each[0]
		count = count + 1
		if sumoftfidf[count] <= 0:
		    temp.append(0)
		else:
		    temp.append(each[2]/sumoftfidf[count])
	document_vector[each[0], each[1]] = temp




#################TO CREATE THE TFIDF CENTROID

#Fetches the Receive List
fp = open('C:\\Users\\Master Admin\\Documents\\ALDA_project\\UsersFiltered3319.txt', 'r')
lines = fp.readlines()
userslist = []
for each in lines:
    userslist.append(each[(each.find('\t') + 2):-2])

#Counts the total number of terms in all the documents
cursor.execute("select count(distinct term) from document_term")##Takes a little time
for each in cursor:
  no_of_words = each[0]

#fetches all the terms in the data set
bag_of_words = []
cursor.execute("select distinct term from document_term")
for each in cursor:
    bag_of_words.append(each[0])

#Fetches all the distinct documents from the data set
list_of_documents = []
mid_set=""
cursor.execute("select distinct number from document_term")
for each in cursor:
    list_of_documents.append(each[0])
    mid_set=mid_set+str(each[0])+","
mid_set=mid_set.rstrip(",")
mid_set="("+mid_set+")"

users_mid = {}


##Creates a dictionary where:
# Key: Each recipient user
# Value: List of document number corresponding to the emails he/she received
for each in userslist:
	cnx = mysql.connector.connect(user='sushma', database='enron4',password='Sushma26011993',host='localhost')
	cursor = cnx.cursor();
	cursor.execute("select mid from recipientinfo where rvalue = '%s' and rtype = 'TO' and mid in %s" %(each, mid_set))
	users_mid[each] = list(cursor.fetchall())




#CREATE TFIDF_CENTROID MATRIX)
tfidf_centroid = [[0 for x in range(no_of_words)] for x in range(len(userslist))]
i = -1
for eachuser in userslist:
	i = i + 1
	print "Calculating for ", eachuser, ". He's User No. ", i
	for each in users_mid.values()[i]:
		cnx = mysql.connector.connect(user='sushma', database='enron4',password='Sushma26011993',host='localhost')
		cursor = cnx.cursor();
		cursor.execute("select term from document_term where number = %s" %each)
		for every in cursor:
			tfidf_centroid[userslist.index(users_mid.keys()[i])][bag_of_words.index(unicode(str(every)[3:-3]))] = tfidf_centroid[userslist.index(users_mid.keys()[i])][bag_of_words.index(unicode(str(every)[3:-3]))] + document_vector[(int(str(each)[1:-2])), (unicode(str(every)[3:-3]))][0]
