# CODE TO GET THE VOCABULARY
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

#rvalue=sys.argv[1]
#svalue=sys.argv[2]
#data=sys.argv[3]
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
#nltk.download()
from nltk import pos_tag
_POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
tagger = nltk.data.load(_POS_TAGGER)
import mysql.connector
from nltk.corpus import stopwords
import sklearn

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
cnx = mysql.connector.connect(user='root', database='enron_merged',password='root',host='localhost')
cursor = cnx.cursor();	
def convert_words(data,stops):
     #print "hi";
     print "convert words"
     ts = time.time()
     print ts
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
        #print tag[1] 
        type=get_wordnet_pos(tag[1])
        final_word_list.append(wnl.lemmatize(tag[0],type))
     ts = time.time() 	
     #print ts	 
     st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
     print st
     return( " ".join(final_word_list))

	 
def funct(rvalue,svalue,data,alpha,beta,gamma):
    ####print stopwords.words("english")
    print "funct"
    ts = time.time()
    print ts
    stops=stopwords.words("english")
    stops.append("the")
    stops.append("this")
    stops.append("to")
    stops.append("they")
    stops.append("cause")
    
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer(analyzer = "word",tokenizer = None,preprocessor = None,stop_words = None)	 
    stops = set(stops)
    ##data="enron"
    data=convert_words(data,stops)
    cleaned_data=[]
    cleaned_data.append(data)
    word_features=vectorizer.fit_transform(cleaned_data);
    a=word_features.getrow(0).toarray()
    #print word_features.getrow(0).toarray()
    #print word_features
    vocab = vectorizer.get_feature_names()
    #print vocab

    ###############################
    #rvalue='all.worldwide@enron.com';

    #svalue='enron.announcements@enron.com';
       
    query=("select mid from recipientinfo where rvalue = \'"+rvalue+"\'")
    cursor.execute(query);
    print cursor.statement
    mid_set=""
    for mid in cursor:
        #print mid[0]
        mid_set=mid_set+str(mid[0])+","
    mid_set=mid_set.rstrip(",")
    mid_list=mid_set.split(",")
    mid_unique=set(mid_list)
    mid_set="("+mid_set+")"
    print mid_set
    #print "\nset is\n"
    #print mid_unique
    flag=0
    query=("select mid from communications_train where sender = \'"+svalue+"\' and rvalue = \'"+rvalue+"\'")
    count=cursor.execute(query);
    print cursor.statement
    print count
    s_mid_set=""
    if count==None:
        flag=1
    for mid in cursor:
        #print mid[0]
        s_mid_set=s_mid_set+str(mid[0])+","
    
	
    s_mid_set=s_mid_set.rstrip(",")
    s_mid_list=s_mid_set.split(",")
    s_mid_unique=set(s_mid_list)
    s_mid_set="("+s_mid_set+")"
    print s_mid_set
    #print "\nsender set is\n"
    #print s_mid_unique

    #alpha=0.33
    #beta=0.33
    #gamma=0.33
    prod=1
    print "loooping through" 
    ts = time.time()
    print ts
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print st
    for term in vocab:
        if flag==0:
            query=("select sum(count) from document_term where term=\""+term+"\" and number in "+s_mid_set)
            cursor.execute(query);
            #print "\n statement is\n"
            #print cursor.statement;
            result = cursor.fetchone()[0]
            if result is None:
                 result=0
            #print result
            query=("select sum(count) from document_term where number in "+s_mid_set)
            cursor.execute(query);
            #print "\n statement is\n"
            #print cursor.statement;
            result_total = cursor.fetchone()[0]
            if result_total is None:
                 result_total=0
            #print result_total
        else:
            result_total=0
        if(result_total==0):
            prob1=0
        else:
            prob1=(result/result_total);
        print "\n probability is\n"
        print prob1
        query=("select sum(count) from document_term where term=\""+term+"\" and number in "+mid_set)
        cursor.execute(query);
        #print "\n statement is\n"
        #print cursor.statement;
        result = cursor.fetchone()[0]
        if result is None:
            result=0
        #print result
        query=("select sum(count) from document_term where number in "+mid_set)
        cursor.execute(query);
        #print "\n statement is\n"
        #print cursor.statement;
        result_total = cursor.fetchone()[0]
        #print result_total
        if result_total is None:
            result_total=0
        if(result_total==0):
            prob2=0
        else:
            prob2=(result/result_total);
        print "\n probability is\n"
        print prob2
        query=("select sum(count) from document_term where term=\""+term+"\"")
        cursor.execute(query);
        #print "\n statement is\n"
        #print cursor.statement;
        result = cursor.fetchone()[0]
        if result is None:
            result=0
        #print result
        query=("select sum(count) from document_term")
        cursor.execute(query);
        #print "\n statement is\n"
        #print cursor.statement;
        result_total = cursor.fetchone()[0]
        if result_total is None:
            result_total=0
    
        #print result_total
        if(result_total==0):
            prob3=0
        else:
            prob3=(result/result_total);
        print "\n probability is\n"
        print prob3
        prob=alpha*float(prob1)+beta*float(prob2)+gamma*float(prob3);
        prod=prod*prob;
    #print "\n final probability is\n"
    print "loooping end" 
    ts = time.time()
    #print ts
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print st
    return prod
    #for (sum(count)) in cursor:
    #    print "ele is",sum(count)
        #sum_term=ele
    #print sum_term
query=("select body from messages limit 1")
cursor.execute(query);
body= cursor.fetchone()[0]
funct('tana.jones@enron.com','mark.taylor@enron.com',"enron himangshu sushma",0.33,0.33,0.33)