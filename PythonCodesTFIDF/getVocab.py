
import numpy
import nltk
import re
import csv
import scipy
import sys
import scipy.sparse
import time
from nltk import pos_tag
import datetime
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import stopwords
import sklearn


_POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
tagger = nltk.data.load(_POS_TAGGER)
wnl = WordNetLemmatizer()

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return 'a'
    elif treebank_tag.startswith('V'):
        return 'v'
    elif treebank_tag.startswith('N'):
        return 'n'
    elif treebank_tag.startswith('R'):
        return 'r'
    else:
        return 'n'


	
def convert_words(data,stops):
     data=data.replace("=01","")
     data=data.replace("=09","")
     data=data.replace("=20"," ")
     data=data.replace("=","")
     data=data.replace("&nbsp"," ")
     data=re.sub('[\.,\,,\#,\!,\&,\@,\?,\:,\;,\>,\"]'," ",data)
     words=data.lower().split();
     
     meaningful_words = [w for w in words if not w in stops]
     tags=tagger.tag(meaningful_words)
     final_word_list=[]
     for tag in tags:
     
        type=get_wordnet_pos(tag[1])
        final_word_list.append(wnl.lemmatize(tag[0],type))
     
     return( " ".join(final_word_list))
     

def test():
    print "Hola !"


def getAccurateCleanedData(data, usefulWords):
    if not data:
        return ""
    stops=stopwords.words("english")
    stops.append("the")
    stops.append("this")
    stops.append("to")
    stops.append("they")
    stops.append("cause")
    
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer(analyzer = "word",tokenizer = None,preprocessor = None,stop_words = None)   
    stops = set(stops)
    
    data=convert_words(data,stops)
    if not data:
        return ""

    cleaned_data=[]
    cleaned_data.append(data)
    


    return cleaned_data   
	
'''
from sklearn.feature_extraction.text import CountVectorizer
cleaned_data = getVocab("Himangshu Ranjan Borah is a student at NC State.student")
vectorizer = CountVectorizer(analyzer = "word",tokenizer = None,preprocessor = None,stop_words = None)
word_features=vectorizer.fit_transform(cleaned_data);
a=scipy.sparse.find(word_features)
vocab = vectorizer.get_feature_names()
print vocab
row=a[0]
col=a[1]
vals=a[2]
print vals
for i in range(0,len(row)):
    #print " doc ",row[i]," term ",vocab[col[i]]," count ",vals[i]
    doc_term=(vocab[col[i]],vals[i])
    print doc_term
#a=word_features.getrow(0).toarray()


#temp = getAccurateVocab("Himangshu Ranjan Borah is a student at NC State", "himangshu borah")
#print temp
#print temp1'''
