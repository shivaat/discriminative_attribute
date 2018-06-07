# Finding Discriminative Attributes 
Code and documentation for the SemEval 2018 shared task `Capturing Discriminative Attributes`:

If you use the code from this repository please cite the following paper:

```
@inproceedings{taslimipoor2018wolves,
  title={Wolves at SemEval-2018 Task 10: Semantic Discrimination based on Knowledge and Association},
  author={Taslimipoor, Shiva and Rohanian, Omid and Ha, Le An and Corpas Pastor, Gloria and Mitkov, Ruslan},
  booktitle={Proceedings of The 12th International Workshop on Semantic Evaluation},
  pages={972--976},
  year={2018}
}
```

For this shared task we developed a classification system to determine whether an attribute word can distinguish one word from another.
To model semantic difference, we define a discriminative score as follows:

<img src="https://latex.codecogs.com/gif.latex?DISC_-Score(w1,w2,attr)&space;=&space;Score(w1,&space;attr)&space;-&space;Score(w2,&space;attr)" title="DISC_-Score(w1,w2,attr) = Score(w1, attr) - Score(w2, attr)" />

whemojtabare w1,w2 and attr are the first, second, and third word respectively. Score is a variable function of relation between two words which we compute from different resources.

We make use of a variety of different association measures derived from huge corpora, and also pre-trained distributional semantic vectors. To augment our method with structured knowledge, we utilise [a knowledge-based ontology](http://conceptnet.io/). We use the feature set in supervised and unsupervised settings.

In summary, we have four sets of different <img src="https://latex.codecogs.com/gif.latex?Score" title="Score" />s each used in computing <img src="https://latex.codecogs.com/gif.latex?DISC_-Score" title="DISC_-Score" />s.

In order to speed up the evaluation, in this repo we upload all the pre-computed scores in separate folders ([ConceptNet](http://conceptnet.io), [Sketch Engine](https://www.sketchengine.co.uk/), [Google Ngrams](http://phrasefinder.io), and Word2vec Similarity). In the script `classify.py`, we load these scores and feed them as features to the classifier.

### To Do
The scripts for computing each set of scores will be uploaded in their corresponding directories.


