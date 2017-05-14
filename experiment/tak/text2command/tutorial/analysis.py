# Realt text analysis in action

# We would like to:
# Extract the names of all the characters from the book (e.g. Elizabeth, Darcy, Bingley)
# Visualize characters' occurences with regards to relative position in the book
# Authomatically describe any character from the book
# Find out which characters have been mentioned in a context of marriage
# Build keywords extraction that could be used to display a word cloud (example)

# Load text file
def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()

import spacy

nlp = spacy.load('en')

# Process 'text' with Spacy NLP parser
text = read_file('data/pride_and_prejudice.txt')
processed_text = nlp(text)


# How many senteces are in the book (Pride & Prejudice)
sentences = [s for s in processed_text.sents]
print(len(sentences))

# print senteces from inex 10 to 15, to make sure that we have parsed the correct books
print(sentences[10:15])

# extract all the personal name from pride & prejudice and count their occurances.
# expected output is a list in hte following form: [('elizabeth', 622), ('darcy', 312), ('jane', 286), ('bennet', 266) ...].

from collections import Counter, defaultdict

def find_character_occurances(doc):
	""" Return a list of acrots from 'doc' with corresponding occurances.

	: prams doc: Spacy NLP pare document
	:return: list of tuples in form
	"""

	characters = Counter()
	for ent in processed_text.ents:
		if ent.label_ == 'PERSON':
			characters[ent.lemma_] += 1

	return characters.most_common()

# entity: proper nouns such as public figures, landmarks. common nouns such as restaurant, stadium etc.. 

# lemma: contains the "root" word upon which this word is based, which allows you to canonicalize word usage withint your text.
#      : i.e. "write","writing","wrote", and "written" are based on the same lemma, write

# Counter() is a handy collections of python. It creates map of key:value [https://docs.python.org/2/library/collections.html]


print(find_character_occurances(processed_text)[:20])


# Find words (adjectives) that describe Mr. Darcy.

def get_character_adjectives(doc, character_lemma):
    """
    Find all the adjectives related to `character_lemma` in `doc`
    
    :param doc: Spacy NLP parsed document
    :param character_lemma: string object
    :return: list of adjectives related to `character_lemma`
    """
    
    adjectives = []
    for ent in processed_text.ents:
        if ent.lemma_ == character_lemma:
            for token in ent.subtree:
                if token.pos_ == 'ADJ': # Replace with if token.dep_ == 'amod':
                    adjectives.append(token.lemma_)
    
    for ent in processed_text.ents:
        if ent.lemma_ == character_lemma:
            if ent.root.dep_ == 'nsubj':
                for child in ent.root.head.children:
                    if child.dep_ == 'acomp':
                        adjectives.append(child.lemma_)
    
    return adjectives

print(get_character_adjectives(processed_text, 'darcy'))