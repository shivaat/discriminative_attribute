# coding: utf-8

import requests
import time
from simplejson import JSONDecodeError

def lookup(word):
    """entry for a query in concept"""
    r =  requests.get('http://api.conceptnet.io/c/en/'+word+'?offset=0&limit=1000')
    while not r.ok:
        print(r)
        time.sleep(5)
        r =  requests.get('http://api.conceptnet.io/c/en/'+word+'?offset=0&limit=1000')       
    if r.ok:
        try:
            j =  r.json()['edges']  
        except JSONDecodeError:
            print(r.json())
    return j


def lookforRelation(relation,word):
    """find all relations for a query"""
    for item in lookup(word):
        if item['rel']['label']==relation:
            if item['start']['language']=='en' and item['end']['language']=='en': 
                print(item['start']['label'], item['end']['label'])

def lookup_with_root(word):
    """in addition to the word itself, also include data related to its possible root(s)"""
    rels =  requests.get('http://api.conceptnet.io/c/en/'+word+'?offset=0&limit=1000').json()['edges']
    roots = set()
    for rel in rels:
        if (rel['rel']['label'] == 'FormOf') and (rel['end']['label'] != word):
            roots.add(rel['end']['label'])
    for w in roots:
        rels.extend(requests.get('http://api.conceptnet.io/c/en/'+w+'?offset=0&limit=1000').json()['edges'])
    return rels

def relatedness(word, related_word):
    """return degree of relatedness between two words (uses Conceptnet Numberbatch)
    since we experiment with numberbatch directly, we ended up not using it"""
    rel = requests.get('http://api.conceptnet.io/related/c/en/'+word+'?offset=0&limit=10000').json()['related']
    for item in rel:
        if '/c/en'+related_word in item['@id']:
            return item['weight']
    else:
        return 0  


