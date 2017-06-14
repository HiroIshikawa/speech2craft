from gensim.models import KeyedVectors
folder = 'word_embeddings/'

model = KeyedVectors.load(folder + 'GoogleNews', mmap='r')
#model.syn0norm = model.syn0


# print '\nJUMP'
# print model.most_similar(positive=['jump'], topn=20)
# print 'hop:', model.similarity('jump', 'hop')
# print 'leap:', model.similarity('jump', 'leap')
#
# print '\nUSE'
# print model.most_similar(positive=['use'], topn=20)
# print 'wield:', model.similarity('use', 'wield')
# print 'hold:', model.similarity('use', 'hold')
# print 'grab:', model.similarity('use', 'grab')
#
# print '\nMOVE'
# print model.most_similar(positive=['move'], topn=20)
# print 'walk:', model.similarity('move', 'walk')
# print 'run:', model.similarity('move', 'run')
# print 'go:', model.similarity('move', 'go')
#
# print '\nTURN'
# print model.most_similar(positive=['turn'], topn=20)
# print 'spin:', model.similarity('turn', 'spin')
#
# print '\nCROUCH'
# print model.most_similar(positive=['crouch'], topn=20)
# print 'duck:', model.similarity('crouch', 'duck')
#
# print '\nATTACK'
# print model.most_similar(positive=['attack'], topn=20)
# print 'duck:', model.similarity('attack', 'hit')
# print 'duck:', model.similarity('attack', 'kill')
# print 'duck:', model.similarity('attack', 'swipe')
# print 'duck:', model.similarity('attack', 'maim')

import spacy
nlp = spacy.load('en', vectors='en_glove_cc_300_1m_vectors')

synonyms = {
    'move': set(['go', 'run', 'walk']),
    'jump': set([]),
    'strafe': set([]),
    'look': set([]),
    'pitch': set(['gaze', 'tilt']),
    'turn': set([]),
    'crouch': set(['duck']),
    'attack': set(['hit', 'dig']),
    'use': set(['hold', 'wield']),
    'stop': set([]),
    'get': set(['pick', 'grab']),
    'discard': set(['drop'])
}

other_synonyms = {
    'forward': set(['straight']),

}

command_map = {
    'move': {
        'stop': ['move 0', 'strafe 0'],
        'forward': 'move 1', 'back': 'move -1', 'right': 'strafe 1', 'left': 'strafe -1',
        'north': 'movenorth 1', 'south': 'movesouth 1', 'east': 'moveeast 1', 'west': 'movewest 1'#,
        #'to': 'LIST OF ENTITIES/OBJECTS'
    },
    'jump': {
        '': 'jump 1', 'stop': ['jump 0'],
        'forward': 'jumpmove 1', 'back': 'jumpmove -1', 'right': 'jumpstrafe 1', 'left': 'jumpstrafe -1',
        'north': 'jumpnorth 1', 'south': 'jumpsouth 1', 'east': 'jumpeast 1', 'west': 'jumpwest 1'  # 'use': 'jumpuse'
    },
    'strafe': {'right': 'strafe 1', 'left': 'strafe -1', 'stop': ['strafe 0']},
    'look': {'up': 'look -1', 'down': 'look 1'},
    'pitch': {'up': 'pitch -1', 'down': 'pitch 1', 'stop': ['pitch 0']},
    'turn': {'right': 'turn 1', 'left': 'turn -1', 'stop': ['turn 0', 'pitch 0'], 'up': 'pitch -1', 'down': 'pitch 1',
             'to': 'LIST OF ENTITIES/OBJECTS'},
    'crouch': {'': 'crouch 1', 'stop': ['crouch 0']},
    'attack': {'': 'attack 1', 'stop': ['attack 0']},
    'use': {'': 'INVENTORY LIST'},
    'stop': ['move 0', 'jump 0', 'turn 0', 'strafe 0', 'pitch 0', 'crouch 0', 'attack 0'],
    'get': {'': 'LIST OF ENTITIES/OBJECTS'},
    'discard': {'': 'discardCurrentItem'},
}



def most_similar(word):
   queries = [w for w in word.vocab if w.is_lower == word.is_lower and w.prob >= -15]
   by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
   return by_similarity[:25]


while True:
    input = raw_input('Command: ')
    if input != '':
        #l = [(model.similarity(input, command), command) for command in command_map]
        l = [(model.similarity(input, command), command) for command in command_map.get('move')]
        for score, command in sorted(l):
            print command, ':', score


        # #for word in most_similar(nlp.vocab[unicode(input)]):
        # #    print word.lower_
        #
        #
        # for word in model.similar_by_word(input, topn=10, restrict_vocab=30000):
        #     print word

        # for command in command_map:
        #     print command, ':', nlp.vocab[unicode(input)].similarity(nlp.vocab[unicode(command)])
        #print model.most_similar(positive=[input], topn=10)




# model = KeyedVectors.load(folder + 'lexvec', mmap='r')
# model.syn0norm = model.syn0
# print model.similarity('pig', 'pork')
# print model.similarity('run', 'move')
# print model.similarity('jump', 'hop')
# print model.similarity('get', 'grab')
# print model.similarity('use', 'wield')
#
#
# model = KeyedVectors.load(folder + 'dep', mmap='r')
# model.syn0norm = model.syn0
# print model.similarity('pig', 'pork')
# print model.similarity('run', 'move')
# print model.similarity('jump', 'hop')
# print model.similarity('get', 'grab')
# print model.similarity('use', 'wield')