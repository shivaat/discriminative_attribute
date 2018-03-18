from concept_query import lookup, lookup_with_root


# depending on whether you want to include the root of the word or not, uncomment one of the following two lines 
word_lookup = lookup
#word_lookup = lookup_with_root


taskScores = []
with open('../DiscriminAtt-master/training/train.txt') as f, open("conceptNet_Scores_train_pure.txt", 'w') as o:
    i=0 # a record of the line numebr being processed (in cases of network failure)
    for line in f:
        i+=1 
        if i>0: # in case of failure, we can continue by changing 0 to the last line index
            items = line.split(',')
            score = scoreR = 0 # R refers to "reverse", meaning the reverse direction from the feature to the word
            score1 = score2 = scoreR1 = scoreR2 = 0 # indices 1, and 2 mean "from 1st word to feature" and "from 2nd word to feature"
            rNum = 0 # relation number, to keep track of the number of features 
            
            ### score from word to feature
            for r in word_lookup(items[0]):
                rNum+=1
                if items[2] in r['start']['label'] or items[2] in r['end']['label']: # or (r['surfaceText'] and items[2] in r['surfaceText']):
                    score+=1
                    score1+= (1 * float(r['weight'])) 

            for r in word_lookup(items[1]):
                if items[2] in r['start']['label'] or items[2] in r['end']['label']: # or (r['surfaceText'] and items[2] in r['surfaceText']):
                    #print('loss', r)
                    score-=1
                    score2+= (1 * float(r['weight'])) 
            ### now, reverse score from the feature to the word 
            for r in word_lookup(items[2]):
                if items[0] in r['start']['label'] or items[0] in r['end']['label']:
                    scoreR+=1
                    scoreR1+= (1 * float(r['weight'])) 
            for r in word_lookup(items[1]):
                if items[0] in r['start']['label'] or items[0] in r['end']['label']:
                    scoreR-=1
                    scoreR2+= (1 * float(r['weight'])) 
                    
            o.write(items[0]+","+items[1]+","+items[2]+","+str(score1)+","+str(score2)+","+str(scoreR1)+","+str(scoreR2)+"\n")
                        
        if i%500==0:
            print(i)
