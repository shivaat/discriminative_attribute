import pickle
import numpy as np
import random
from sklearn import svm, linear_model
from sklearn.grid_search import GridSearchCV
from gensim.models import Word2Vec, KeyedVectors
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn import metrics
import spacy
nlp = spacy.load('en')

# import method for evaluation
from PR import evaluation
# import methods to read different scores 
from readFeatures import *

CN = True                   # ConceptNet Flag
SIM = True                  # Similarity-based flag
GN = True                   # Google Ngram flag

associationMeas = ['MI', 'T', 'MI3', 'Dice', 'likelihood', 'Salience']   

# Reading conceptNet features
cnFile = "./ConceptNet/conceptNet_Scores_train_separate.txt"
cn_list_train = readConceptNet(cnFile)

cnFile = "./ConceptNet/conceptNet_Scores_validation_separate.txt"
cn_list_validation = readConceptNet(cnFile)


# Reading w2v similarity scores
simFileTrain = "./w2vSimilarity/new_train_similarity_scores.txt"
simFileTrain2 = "./w2vSimilarity/numberbatch-similarity-based-scores-train.txt"
sim_list_train = readSimilarityScores(simFileTrain, simFileTrain2)

simFileTest = "./w2vSimilarity/similarity-based-scores-validation.txt"
simFileTest2 = "./w2vSimilarity/numberbatch-similarity-based-scores-validation.txt"
sim_list_valid = readSimilarityScores(simFileTest, simFileTest2)

# Reading google Ngrams (Bigrams only)
gBiFileTrain = "./GoogleNgram/googleBigram_Scores_train.txt"
gBiListTrain = readGoogleNgram(gBiFileTrain)
gBiFileValid = "./GoogleNgram/googleBigram_Scores_validation.txt"
gBiListValid = readGoogleNgram(gBiFileValid)

# Reading Google Ngrams (up to 5-grams)
gnFileTrain = "./GoogleNgram/googleNgram_Scores_train.txt"
gnListTrain = readGoogleNgram(gnFileTrain)
gnFileValid = "./GoogleNgram/googleNgram_Scores_validation.txt"
gnListValid = readGoogleNgram(gnFileValid)

# Reading Association measures
association_list = pickle.load( open("./SketchEngine/train_bigramAssociationScores_limited.p", "rb") )
association_list_lemma = pickle.load( open("./SketchEngine/train_bigramAssociationScores_lemma_limited.p", "rb") )

# lemmatise the word 
def lem(word):
    tokens = nlp(word)
    return [token.lemma_ for token in tokens][0]

# function to load data
def read_data(filePath):
    data = []
    with open(filePath) as f:
        for line in f:
            items = line.strip().split(',')
            data.append(((items[0],items[1],items[2]), int(items[3])))
    return data
    
# load training data 
train_path = '../Task10/DiscriminAtt-master/training/train.txt'
train_data = read_data(train_path) 
print("train data:",len(train_data))

X_train = readAssociationMeasures(train_data, associationMeas, association_list, association_list_lemma)

if CN:
http://phrasefinder.io    X_train = [np.concatenate((X_train[i], cn_list_train[i])) for i in range(len(X_train))]
if SIM:
    X_train = [np.concatenate((X_train[i], sim_list_train[i])) for i in range(len(X_train))]
if GN:
    X_train = [np.concatenate((X_train[i], gBiListTrain[i])) for i in range(len(X_train))]
    X_train = [np.concatenate((X_train[i], gnListTrain[i])) for i in range(len(X_train))]

print("len train dimensions", len(X_train[0]))

# scale the feature values (train)
X_train = np.array(X_train)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
y_train = np.array([item[1] for item in train_data])

# load validation data 
validation_path = '../Task10/DiscriminAtt-master/training/validation.txt'
valid_data = read_data(validation_path)
print("validation data:",len(valid_data))

# load feature values (validation) 
X_valid = readAssociationMeasures(valid_data, associationMeas, association_list, association_list_lemma)

if CN:
    X_valid = [np.concatenate((X_valid[i], cn_list_validation[i])) for i in range(len(X_valid))]
if SIM:
    X_valid = [np.concatenate((X_valid[i], sim_list_valid[i])) for i in range(len(X_valid))]
if GN:
    X_valid = [np.concatenate((X_valid[i], gBiListValid[i])) for i in range(len(X_valid))]
    X_valid = [np.concatenate((X_valid[i], gnListValid[i])) for i in range(len(X_valid))]

# scale the feature values (validation)
scaler = StandardScaler()
X_valid = scaler.fit_transform(X_valid)
y_valid = [item[1] for item in valid_data]

# define the classifier 
svc = svm.SVC(kernel='linear', probability=True)
Cs = np.logspace(-6, -1, 10)
clf = GridSearchCV(estimator=svc, param_grid=dict(C=Cs), n_jobs=-1)

# fit clf on training dta
clf.fit(X_train, y_train)
print("&&&&&&&&&  Trained &&&&&&&&&&&&")

# predict values 
predictions = clf.predict(X_valid)
predictions=list(predictions)

with open('validResults.txt', 'w') as o:
    for i in range(len(predictions)):
        o.write(valid_data[i][0][0]+','+valid_data[i][0][1]+','+valid_data[i][0][2]+','+str(predictions[i])+"\n")

# evaluate the predictions 
print('evaluation results on validation data: ')
evaluation(trueFile='../Task10/DiscriminAtt-master/training/validation.txt', resFile = 'validResults.txt')

##################################################

X = list(X_train) + list(X_valid)
y = list(y_train) + list(y_valid)
'''
predicted = cross_val_predict(clf, X, y, cv=10)

score1 = metrics.f1_score(y, predicted, pos_label=1)
score2 = metrics.f1_score(y, predicted, pos_label=0)
print('pos', score1)http://phrasefinder.io
print('neg', score2)
print('average F1', (score1+score2)/2.0)
'''
##################################################

# load test data 
test_path = '../Task10/DiscriminAtt-master/test/truth.txt'
test_data = []  #read_data(test_path)
with open(test_path) as f:
    for line in f:
        items = line.strip().split(',')
        test_data.append(((items[0],items[1],items[2]), -1))
print("test data:",len(test_data))

X_test = [np.array([])]*len(test_data)

X_test = readAssociationMeasures(test_data, associationMeas, association_list, association_list_lemma)

# Reading conceptNet features
cnFile = "./ConceptNet/conceptNet_Scores_test_separate.txt"
cn_list_test = readConceptNet(cnFile)

# Reading similarity features
simFileTest = "./w2vSimilarity/wvWiki-similarity-based-scores-test.txt"
simFileTest2 = "./w2vSimilarity/numberbatch-similarity-based-scores-test.txt"
sim_list_test = readSimilarityScores(simFileTest, simFileTest2)

# Reading googleNgram
gBiFileTest = "./GoogleNgram/googleBigram_Scores_test.txt"
gBiListTest = readGoogleNgram(gBiFileTest)
gnFileTest = "./GoogleNgram/googleNgram_Scores_test.txt"
gnListTest = readGoogleNgram(gnFileTest)

if CN:
    X_test = [np.concatenate((X_test[i], cn_list_test[i])) for i in range(len(X_test))]
if SIM:
    X_test = [np.concatenate((X_test[i], sim_list_test[i])) for i in range(len(X_test))]

if GN:
    X_test = [np.concatenate((X_test[i], gBiListTest[i])) for i in range(len(X_test))]
    X_test = [np.concatenate((X_test[i], gnListTest[i])) for i in range(len(X_test))]

scaler = StandardScaler()
X_test = scaler.fit_transform(X_test)

clf.fit(X, y)

predictions = clf.predict(X_test)

with open("prediction.txt", 'w') as o:
    for i in range(len(predictions)):
        o.write(test_data[i][0][0]+','+test_data[i][0][1]+','+test_data[i][0][2]+','+str(predictions[i])+"\n")

print('evaluation results on test data: ')
evaluation(trueFile='../Task10/DiscriminAtt-master/test/truth.txt',resFile = 'prediction.txt')
