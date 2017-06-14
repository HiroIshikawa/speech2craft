import spacy
from spacy.symbols import *

from gensim.models import KeyedVectors

import time
import json


class CommandParser:
    def __init__( self, agent_host=None, doc=None ):
        '''Initializes the class.'''
        self.doc_ = doc
        self.agent = agent_host
        self.word2vec = KeyedVectors.load('word_embeddings/GoogleNews', mmap='r')

        self.command_map = {
            'move': {
                'stop': ['move 0', 'strafe 0'],
                'forward': 'move 1', 'back': 'move -1', 'backwards': 'move -1', 'right': 'strafe 1', 'left': 'strafe -1',
                'north': 'movenorth 1', 'south': 'movesouth 1', 'east': 'moveeast 1', 'west': 'movewest 1',
                'to': 'LIST OF ENTITIES/OBJECTS'
            },
            'jump': {
                '': 'jump 1', 'up': 'jump 1', 'stop': ['jump 0'], 'forward': 'jumpmove 1', 'back': 'jumpmove -1',
                'backwards': 'jumpmove -1', 'right': 'jumpstrafe 1', 'left': 'jumpstrafe -1',
                'north': 'jumpnorth 1', 'south': 'jumpsouth 1', 'east': 'jumpeast 1', 'west': 'jumpwest 1'
            },
            'strafe': {'right': 'strafe 1', 'left': 'strafe -1', 'stop': ['strafe 0']},
            'look': {'up': 'look -1', 'down': 'look 1'},
            'pitch': {'up': 'pitch -1', 'down': 'pitch 1', 'stop': ['pitch 0']},
            'turn': {'right': 'turn 1', 'left': 'turn -1', 'stop': ['turn 0', 'pitch 0'],
                     'up': 'pitch -1', 'down': 'pitch 1'},
            'crouch': {'': 'crouch 1', 'stop': ['crouch 0']},
            'attack': {'': 'attack 1', 'stop': ['attack 0']},
            'use': {},
            'stop': ['move 0', 'jump 0', 'turn 0', 'strafe 0', 'pitch 0', 'crouch 0', 'attack 0'],
            'get': {'': 'LIST OF ENTITIES/OBJECTS'},
            'discard': {'': 'discardCurrentItem'},
            'quit': {'': 'quit'}
        }

        self.synonyms = {
            'move': set(['go', 'run', 'walk']),
            'jump': set([]),
            'strafe': set([]),
            'look': set([]),
            'pitch': set(['gaze', 'tilt']),
            'turn': set([]),
            'crouch': set(),
            'attack': set(['hit', 'dig']),
            'use': set(['hold', 'wield']),
            'stop': set([]),
            'get': set(['pick', 'grab']),
            'discard': set(['drop', 'throw'])
        }

        self.entities = {
            'pig': 'pig',
            'cow': 'cow',
            'stone': 'stone',
            'item': 'item',

        }


    def parseCommands( self, doc, agent_host=None ):
        if agent_host is not None:
            self.agent = agent_host

        self.doc_ = doc
        if self.doc_ is not None:
            for sentence in self.doc_.sents:
                root = sentence.root
                print('root.text: '),
                print(root.lemma_, root.lower_, root.text)
                if root.lemma_ == u'go':
                    print('returning go to')
                    return 'goto'
                elif root.lemma_ == u'stop' and root.n_rights == 0:
                     print('returning stop')
                     return 'stop'
                elif root.lemma_ == 'quit':
                    print('QUITTING')
                    self.agent.sendCommand('quit')
                self.parseVerb_(root)
        return ''


    def parseVerb_( self, verb ):
        # if verb.lemma_ == 'left':
        #     malmo_verb = self.getSimilarCommand_(verb.lower_, self.command_map)
        # else:
        malmo_verb = self.getSimilarCommand_(verb.lemma_, self.command_map)

        if malmo_verb == '':
            self.agent.sendCommand("chat Could not understand command")
        else:
            rights = [child for child in verb.rights]
            if rights:
                if rights[0].pos == CCONJ:
                    self.doBasicCommand_(malmo_verb)
                options = self.command_map.get(malmo_verb)
                for r_child in rights:
                    print r_child.pos_
                    if r_child.pos == ADV or r_child.pos == PART:
                        # no parsing needed, just do command
                        # i.e. move | forward
                        print r_child.text, 'lemma: ', r_child.lemma_
                        if r_child.lemma_ in options:
                            self.doAdvCommand_(malmo_verb, r_child.lemma_)
                    elif r_child.pos == NOUN:
                        # parse for preposition and prepositional object
                        # i.e. choose | steel pickaxe (-> on -> the left)
                        # check if it's a quantitative movement i.e. 1 block forward or forward 1 block
                        if r_child.lemma_ == 'left' and r_child.lemma_ in options:
                            self.doAdvCommand_(malmo_verb, r_child)
                        else:
                            self.doObjCommand_(malmo_verb, r_child)
                    elif r_child.pos == ADP:
                        # parse for prepositional object
                        # i.e. go | to -> pobj
                        self.doPrepCommand_(malmo_verb, r_child)
                    elif r_child.pos == VERB:
                        # parse subsequent command
                        # choose steel pickaxe | (and) dig -> ...
                        # if verb.lemma_ == 'stop':
                        if malmo_verb == 'stop':
                            malmo_stop_verb = self.getSimilarCommand_(r_child.lemma_, self.command_map)
                            if malmo_stop_verb != '':
                                self.doStopCommand_(malmo_stop_verb)
                        else:
                            self.parseVerb_(r_child)
            else:
                self.doBasicCommand_(malmo_verb)



    def similarity( self, w1, w2 ):
        return self.word2vec.similarity(w1, w2)

    def getHotKeyForItem( self, item ):
        world_state = self.agent.getWorldState()
        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            ob = json.loads(msg)
            inventory_list = []
            for i in xrange(9):
                slot_name = u'Hotbar_' + str(i) + '_item'
                slot_contents = ob.get(slot_name, "")

                inventory_list.append(slot_contents)
                # slot_size = u'Hotbar_' + str(i) + '_size'
                # slot_size_contents = ob.get(slot_size, "")
                #
                # slot_colour = u'Hotbar_' + str(i) + '_colour'
                # slot_colour_contents = ob.get(slot_colour, "")
                #
                # slot_variant = u'Hotbar_' + str(i) + '_variant'
                # slot_variant_contents = ob.get(slot_variant, "")
                #
                # print slot_size + ': ' + str(slot_size_contents)
                # print slot_name + ': ' + slot_contentsx
                # print slot_colour + ': ' + str(slot_colour_contents)
                # print slot_variant + ': ' + str(slot_variant_contents)

                if slot_contents == item:
                    return i + 1  # +1 to convert from 0-based inventory slot to 1-based hotbar key.

            print inventory_list

            try:
                best_score = 0.3
                best_slot = -1
                for idx, slot in enumerate(inventory_list):
                    print slot_base
                    slot_base = slot[slot.rfind('_') + 1:]
                    score = self.similarity(item, slot_base)
                    print slot_base, score
                    if score > best_score:
                        best_score = score
                        best_slot = idx + 1
                print 'best slot - ', best_slot
                return best_slot
            except KeyError as e:
                print e
                return -1

        return -1


    def getBestMatch( self, word, options ):
        try:
            best_score = 0.25
            best_word = ''
            for malmo_word in options:
                score = self.similarity(word, malmo_word)
                if score > best_score:
                    best_score = score
                    best_word = malmo_word
            return best_word
        except KeyError:
            return ''


    def getSimilarCommand_( self, verb, options ):
        if verb in self.synonyms:
            return verb
        if verb == 'left':
            return verb
        for action in self.synonyms:
            if verb in self.synonyms.get(action):
                return action

        return self.getBestMatch(verb, options)



    def doBasicCommand_( self, verb ):
        # command = '{} {}'.format(verb.text, 1)
        command = self.command_map.get(verb).get('')
        print 'Sending command: {}'.format(command)
        self.agent.sendCommand(command)
        time.sleep(0.5)


    def doStopCommand_( self, verb ):
        stop_commands = self.command_map.get(verb).get('stop')
        for command in stop_commands:
            print 'Sending command: {}'.format(command)
            self.agent.sendCommand(command)

    def doAdvCommand_( self, verb, option ):
        command = self.command_map.get(verb).get(option)
        print 'Sending command: {}'.format(command)
        self.agent.sendCommand(command)
        time.sleep(0.5)


    def doObjCommand_( self, verb, obj ):
        objString = getObjectString(obj)
        if verb == 'use':
            hotkey = self.getHotKeyForItem(objString)
            print 'hotbar.%d' % hotkey
            self.agent.sendCommand('hotbar.%d 1' % hotkey)
            self.agent.sendCommand('hotbar.%d 0' % hotkey)
        elif verb == 'discard':
            hotkey = self.getHotKeyForItem(objString)
            print 'hotbar.%d' % hotkey
            if hotkey != -1:
                self.agent.sendCommand('hotbar.%d 1' % hotkey)
                self.agent.sendCommand('hotbar.%d 0' % hotkey)
                time.sleep(0.5)
                self.agent.sendCommand('discardCurrentItem')
        elif verb == 'attack':
            pass
        elif verb == 'get':
            pass


    def doPrepCommand_( self, verb, prep ):
        if prep.n_rights:
            pobj = prep.rights.next()
            print 'prepositional object: ' + pobj.lemma_
            ### if object exists --> Howard's code to move to said object
            ### HowardCode(verb, obj, agent)

    # def doQuitCommand( self ):
    #     print 'Sending command: {}'.format('quit')
    #     self.agent.sendCommand('quit')
    #     time.sleep(0.5)




class TextParser:
    def __init__( self ):
        '''Initializes the class.'''
        self.nlp_ = spacy.load('en')
        self.doc = None


    def parse( self, text ):
        '''Parses user input arguments.

        Parameters:
        args : string, containing the command-line arguments.
        '''
        self.doc = self.nlp_(text.decode("utf-8"))
        return self.doc

    def printDependencies( self ):
        if self.doc is not None:
            for word in self.doc:
                print(word.text, word.lemma_, word.dep_, word.dep, word.pos_, word.head.text,
                    [w.text for w in word.lefts],[w.text for w in word.rights])

    def printSubtrees( self ):
        if self.doc is not None:
            for word in self.doc:
                if word.pos == NOUN:
                    for child in word.subtree:
                        print child.text, ',',
                print

    def printNounChunks( self ):
        for word in self.doc.noun_chunks:
            print word.text

    def printAncestors( self ):
        if self.doc is not None:
            for word in self.doc:
                print [tok for tok in word.ancestors]

    def printConjuncts( self ):
        if self.doc is not None:
            for word in self.doc:
                print [tok for tok in word.conjuncts]



# Helpers
def getObjectString( obj ):
    string = ''
    for child in obj.lefts:
        if child.dep_ == 'compound' or child.dep == amod:
            string += child.lower_ + '_'
    string += obj.lemma_

    return string

# def getHotKeyForItem( item, agent ):
#     world_state = agent.getWorldState()
#     print 'item ' + item
#     if world_state.number_of_observations_since_last_state > 0:
#         msg = world_state.observations[-1].text
#         ob = json.loads(msg)
#
#         inventory_list = []
#         for i in xrange(9):
#             slot_name = u'Hotbar_' + str(i) + '_item'
#             slot_contents = ob.get(slot_name, "")
#
#             inventory_list.append(slot_contents.split('_')[-1])
#             # slot_size = u'Hotbar_' + str(i) + '_size'
#             # slot_size_contents = ob.get(slot_size, "")
#             #
#             # slot_colour = u'Hotbar_' + str(i) + '_colour'
#             # slot_colour_contents = ob.get(slot_colour, "")
#             #
#             # slot_variant = u'Hotbar_' + str(i) + '_variant'
#             # slot_variant_contents = ob.get(slot_variant, "")
#             #
#             # print slot_size + ': ' + str(slot_size_contents)
#             # print slot_name + ': ' + slot_contents
#             # print slot_colour + ': ' + str(slot_colour_contents)
#             # print slot_variant + ': ' + str(slot_variant_contents)
#
#             if slot_contents == item:
#                 return i + 1  # +1 to convert from 0-based inventory slot to 1-based hotbar key.
#
#         best_score = 0
#         best_item = ''
#         for item in inventory_list:
#
#
#     return -1