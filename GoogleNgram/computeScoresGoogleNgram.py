#!/usr/bin/env python
from __future__ import print_function
import time
import phrasefinder as pf
import numpy as np 
import pickle 

# note:
# to see returned phrases do:

# for token in phrase.tokens:
#     print(" {}".format(token.text), end="")

def ngram_search(word1, word2):
    options = pf.SearchOptions()
    options.topk = 100 # the maximum number of phrases to return.
    query = "*"+word1+"*"+word2+"*"
    query_rev = "*"+word2+"*"+word1+"*"
    
    langs = [pf.Corpus.AMERICAN_ENGLISH, pf.Corpus.BRITISH_ENGLISH]
    queries = [query, query_rev]
    
    counts = []
    try:
        for query in queries:
            for lang in langs:
                result = pf.search(lang, query, options)
                if result.status != pf.Status.OK:
                    print('Request was not successful: {}'.format(result.status))
                    return
                for phrase in result.phrases:
                    counts.append(phrase.match_count)
    except Exception as error:
        print('Some error in querrying occurred: {}'.format(error))
    return np.sum(np.array(counts))

scores = {}
with open('../DiscriminAtt-master/training/train.txt') as f, open("googleNgram_Scores_train.txt", 'w') as o:
    i=0 # a record of the line number being processed (in cases of network failure)
    for line in f:
        i+=1 
        if i>0: # in case of failure, we can continue by changing 0 to the last line index
            items = line.split('\n')[0].split(',')
            score1 = ngram_search(items[0], items[2])
            score2 = ngram_search(items[1], items[2])
            scores[items[0]+','+items[1]+','+items[2]+','] = (score1, score2)

            o.write(items[0]+","+items[1]+","+items[2]+","+str(score1)+","+str(score2)+"\n")
           
        if i%500==0:
        	pickle.dump(scores, open('temp_results_validation_pickled.pkl', 'wb'))
        	time.sleep(30)
        	print(i)
