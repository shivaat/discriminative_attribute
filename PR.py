import numpy
import pickle

def evaluation(trueFile= '../../DiscriminAtt-master/training/validation.txt', resFile="bestResults0.6560.txt"):

    pos = 0
    labels = {}
    with open(trueFile) as f:
        i = 1
        for line in f:
            items = line.split(',')
            labels [i] = int(items[3].strip())
            pos+= int(items[3].strip())
            i+=1
    #        words.update([items[0],items[1], items[2]])
    print("#labels:",len(labels))
    print("#positives:",float(pos))#/len(labels))
    neg = len(labels) - pos

    ones = 0
    measures = {}
    with open(resFile) as f:
    #with open("conceptnet/conceptNet_Scores_validation.txt") as f:
        i=1
        for line in f:
            items = line.strip().split(',')
            measures[i] = float(items[3])
            ones+= float(items[3])
            i+=1
    #print("predicted as True:",ones)
    zeros = len(labels) - ones
    numTru = 0
    numTruNeg = 0
    for i in measures.keys():
        label = labels[i]
        if label == 1 and measures[i]==1:
            numTru+=1
        if label == 0 and measures[i] == 0:
            numTruNeg+=1
    #print("True Positives",numTru)
    precision = float(numTru)/ones
    recall = float(numTru)/pos
    f1 = 2*precision*recall/(precision+recall)
    print("performance positive",precision, recall, f1)

    precision = float(numTruNeg)/zeros
    recall = float(numTruNeg)/neg
    f2 = 2*precision*recall/(precision+recall)
    print("performance negetive",precision, recall, f2)

    print("average f-measure",(f1+f2)/2)


'''
### PR reults for sorted measures
measures = {}
with open("../results/similarity-based-scores.txt") as f:
    i = 1
    for line in f:
        items = line.strip().split(',')
        measures[i] = float(items[3])
        i+=1

measList = []
for item in sorted(measures,key=measures.get,reverse=True):
       measList.append((item, measures[item]))

with open("results.txt", 'w') as resFile:
    precisions = []
    recalls = []
    numTru = 0
    for i in range(0,len(measList)):
        label = labels[measList[i][0]]
        if label == 1:
            numTru+=1
        precision = float(numTru)/(i+1)
        recall = float(numTru)/pos
        f = 2*precision*recall/(precision+recall)
        resFile.write(str(measList[i][1])+"\t"+str(precision)+"\t"+str(recall)+"\t"+str(f)+"\n")
        precisions.append(precision)
        recalls.append(recall)
'''
