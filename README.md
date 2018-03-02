# discriminative_attribute
Code and documentation for the SemEval 2018 shared task 'Capturing Discriminative Attributes'

For this shared task we developed a classification system to determine whether an attribute word can distinguish one word from another.
To model semantic difference, we define a discriminative score, and make use of a variety of different association measures derived from huge corpora, and also pre-trained distributional semantic vectors. To augment our method with structured knowledge, we utilise [a knowledge-based ontology](http://conceptnet.io/). We use the feature set in supervised and unsupervised settings.

In order to speed up the evaluation, in this repo we upload all the pre-computed scores in separate folders (ConceptNet, Sketch Engine, Google Ngrams, and Word2vec Similarity). In the script `classify.py`, we load these scores and feed them as features to trhe classifier. 


