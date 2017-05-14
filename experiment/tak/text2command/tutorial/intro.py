import spacy

nlp = spacy.load('en')

# What are Stop Words?
# Stop words are the common words in a vocabulary which are of little value when considering word frequencies in text. This is because they don't provide much useful information about what the sentence is telling the reader.
# Example: "the","and","a","are","is"

# What is a Corpus?
# A corpus (plural: corpora) is a large collection of text or documents and can provide useful training data for NLP models. A corpus might be built from transcribed speech or a collection of manuscripts. Each item in a corpus is not necessarily unique and frequency counts of words can assist in uncovering the structure in a corpus.
# Examples:
# Every word written in the complete works of Shakespeare
# Every word spoken on BBC Radio channels for the past 30 years

doc = nlp(u'Hello, world. NLP is awesome.')

# What is a Token?
# A token is a single chopped up element of the sentence, which could be a word or a group of words to analyse. The task of chopping the sentence up is called "tokenisation".
# Example: The following sentence can be tokenised by splitting up the sentence into individual words.
# "Cytora is going to PyCon!"
# ["Cytora","is","going","to","PyCon!"]

token = doc[0]
print('token:'),
print(token)
print()

for sent in doc.sents:
	print(sent)
print()

# What is a Speech Tag?
# A speech tag is a context sensitive description of what a word means in the context of the whole sentence. More information about the kinds of speech tags which are used in NLP can be found here.
# Examples:
# CARDINAL, Cardinal Number - 1,2,3
# PROPN, Proper Noun, Singular - "Matic", "Andraz", "Cardiff"
# INTJ, Interjection - "Uhhhhhhhhhhh"

print('speech tag: '),
for token in doc:
	print('{} - {}'.format(token, token.pos_))
print()

# What are syntactic dependencies?
# We have the speech tags and we have all of the tokens in a sentence, but how do we relate the two to uncover the syntax in a sentence? Syntactic dependencies describe how each type of word relates to each other in a sentence, this is important in NLP in order to extract structure and understand grammar in plain text.
# Example:
# <img src="images/syntax-dependencies-oliver.png" align="left" width=500>

def tokens_to_root(token):
	"""
	Walk up the suntatic tree, collecting tokes to the root of the given 'token'.
	:param token: Spacy token
	:return: list of Spacy tokens
	"""

	tokens_to_r = []
	while token.head is not token:
		tokens_to_r.append(token)
		token = token.head
		tokens_to_r.append(token)

	return tokens_to_r

print('tokens to root: '),
for token in doc:
	print('{} --> {}'.format(token, tokens_to_root(token)))
print()

print('tokens to root (dependency): '),
for token in doc:
	print('->'.join(['{} - {}'.format(dependent_token, dependent_token.dep_) for dependent_token in tokens_to_root(token)]))
print()

# Named Entities
# A named entity is any real world object such as a person, location, organisation or product with a proper name.
# Example:
# 1. Barack Obama
# 2. Edinburgh
# 3. Ferrari Enzo

# Print all named entities with named entity types

print('name entities: '),
doc_2 = nlp(u"I went to Paris where I met my old friend Jack from uni.")
for ent in doc_2.ents:
    print('{} - {}'.format(ent, ent.label_))
print()

# What is a Noun Chunk?
# Noun chunks are the phrases based upon nouns recovered from tokenized text using the speech tags.
# Example:
# The sentence "The boy saw the yellow dog" has 2 noun objects, the boy and the dog. Therefore the noun chunks will be
# 1. "The boy"
# 2. "the yellow dog"

# Print noun chunks for doc_2
print('noun chunks: '),
print([chunk for chunk in doc_2.noun_chunks])
print()

# For every token in doc_2, print log-probability of the word, estimated from counts from a large corpus 
print('unigram probs: '),
for token in doc_2:
    print(token, ',', token.prob)
print()

# What are Word embeddings?
# A word embedding is a representation of a word, and by extension a whole language corpus, in a vector or other form of numerical mapping. This allows words to be treated numerically with word similarity represented as spatial difference in the dimensions of the word embedding mapping.
# Example:
# With word embeddings we can understand that vector operations describe word similarity. This means that we can see vector proofs of statements such as:
# king-queen==man-woman

# For a given document, calculate similarity between 'apples' and 'oranges' and 'boots' and 'hippos'
doc = nlp(u"Apples and oranges are similar. Boots and hippos aren't.")
apples = doc[0]
oranges = doc[2]
boots = doc[6]
hippos = doc[8]
print(apples.similarity(oranges))
print(boots.similarity(hippos))

print()
# Print similarity between sentence and word 'fruit'
apples_sent, boots_sent = doc.sents
fruit = doc.vocab[u'fruit']
print(apples_sent.similarity(fruit))
print(boots_sent.similarity(fruit))