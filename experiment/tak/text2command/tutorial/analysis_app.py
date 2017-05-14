from collections import defaultdict, Counter

import pandas as pd
import seaborn as sns
import spacy

nlp = spacy.load('en')

def read_file_to_list(file_name):
	with open(file_name, 'r') as file:
		return file.readlines()

# The file has been re-encoded in UTF-8 the source encoding is Latin-1
terrorism_articles = read_file_to_list('data/rand-terrorism-dataset.txt')

# Create a list of spacy Doc objects representing articles
terrorism_articles_nlp = [nlp(art) for art in terrorism_articles]


common_terrorist_groups = [
    'taliban', 
    'al - qaeda', 
    'hamas',  
    'fatah', 
    'plo', 
    'bilad al - rafidayn'
]

common_locations = [
    'iraq',
    'baghdad', 
    'kirkuk', 
    'mosul', 
    'afghanistan', 
    'kabul',
    'basra', 
    'palestine', 
    'gaza', 
    'israel', 
    'istanbul', 
    'beirut', 
    'pakistan'
]

