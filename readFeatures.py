import pickle
import numpy as np
import random
from sklearn.grid_search import GridSearchCV
from gensim.models import Word2Vec, KeyedVectors
import spacy
nlp = spacy.load('en')

# Read conceptNet features
def readConceptNet(cnFile):
    cn_list = []
    i=0
    with open(cnFile,'r') as f:
        for line in f:
            items = line.strip().split(',')
            if float(items[-2]) - float(items[-1]) > 0:
                sR = 1
            else:
                sR = 0
            #cn_list.append([float(items[-4]), float(items[-3]), float(items[-2]), float(items[-1])])
            #cn_list.append([float(items[-4]) - float(items[-3])]) #, sR])
            
            if float(items[-4]) - float(items[-3]) > 0:
                cn_list.append([1]) #, sR])    # Reverse has not been used
            else:
                cn_list.append([0]) #, sR])
            
            i+=1
    return cn_list

# read google Ngrams
def readGoogleNgram(gnFile):
    gn_list = []
    i=0
    with open(gnFile,'r') as f:
        lines = f.read().split('\n')
        for l in lines:
            items = l.strip().split(',')
            if float(items[-2]) == 0 and float(items[-1])==0:
                s = 0
            else:
                s = (float(items[-2]) - float(items[-1]))/(float(items[-2]) + float(items[-1]))
            gn_list.append([s])
    return(gn_list)
        

def readSimilarityScores(simFile, simFile2):
    # Reading w2v similarity scores
    sim_list_train = []
    with open(simFile,'r') as f:
        for line in f:
            sim_list_train.append([float(line.strip().split(',')[-1])])

    # Reading numberbatch w2v similarity scores
    with open(simFile2,'r') as f:
        i = 0
        for line in f:
            sim_list_train[i].append(float(line.strip().split(',')[-1]))
            i+=1
    
    return sim_list_train

        

def lem(word):
    tokens = nlp(word)
    return [token.lemma_ for token in tokens][0]

# A function to read Association measures
def association_based_measure(a,b,c, assoc_name, lemma, association_list, association_list_lemma):
    f = 0
    f1 = f2 = 0
    if c in association_list:
            if lem(a) in association_list[c]:
                    #f = association_list[c][a][assoc_name]
                    f = abs(association_list[c][lem(a)][assoc_name])
                    f1 = association_list[c][lem(a)][assoc_name]
            if lem(b) in association_list[c]:
                    #f -= association_list[c][b][assoc_name]
                    f -= abs(association_list[c][lem(b)][assoc_name])
                    f2 = association_list[c][lem(b)][assoc_name]
    
    if lemma ==1:
        if lem(c) in association_list_lemma:
            if lem(a) in association_list_lemma[lem(c)]:                    # This is like when lemma(a) does not exist then we don't check lemma(b)
                #f += association_list_lemma[lem(c)][lem(a)][assoc_name]
                f += abs(association_list_lemma[lem(c)][lem(a)][assoc_name])
                f1 += association_list_lemma[lem(c)][lem(a)][assoc_name]
            
            if lem(b) in association_list_lemma[lem(c)]:
                    #f -= association_list_lemma[lem(c)][lem(b)][assoc_name]
                    f -= abs(association_list_lemma[lem(c)][lem(b)][assoc_name])
                    f2 += association_list_lemma[lem(c)][lem(b)][assoc_name]
    if assoc_name=='freq' and f1+f2 != 0:
        f = (f1 - f2)/(f1 + f2)
    return f

def readAssociationMeasures(data, associationMeas, association_list, association_list_lemma):
    ams = []
    for d in data:
        vec = np.array([])
        for a in associationMeas:
            f1 = association_based_measure(d[0][0], d[0][1], d[0][2], a, 1, association_list, association_list_lemma)
            vec = np.append(vec, f1)
        ams.append(vec)
    return ams

   
