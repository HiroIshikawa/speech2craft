import spacy
from spacy.symbols import *

import time
import json


class CommandParser:
    def __init__( self, agent_host, doc=None ):
        '''Initializes the class.'''
        self.doc_ = doc
        self.agent = agent_host

        self.command_map = {
            'move': {
                'stop': ['move 0', 'strafe 0'],
                'forward': 'move 1', 'back': 'move -1', 'right': 'strafe 1', 'left': 'strafe -1',
                'north': 'movenorth 1', 'south': 'movesouth 1', 'east': 'moveeast 1', 'west': 'movewest 1',
                'to': 'LIST OF ENTITIES/OBJECTS'
            },
            'jump': {
                '': 'jump 1', 'stop': ['jump 0'],
                'forward': 'jumpmove 1', 'back': 'jumpmove -1', 'right': 'jumpstrafe 1', 'left': 'jumpstrafe -1',
                'north': 'jumpnorth 1', 'south': 'jumpsouth 1', 'east': 'jumpeast 1', 'west': 'jumpwest 1' #'use': 'jumpuse'
            },
            'strafe': {'right': 'strafe 1', 'left': 'strafe -1', 'stop': ['strafe 0']},
            'look': {'up': 'look -1', 'down': 'look 1'},
            'pitch': {'up': 'pitch -1', 'down': 'pitch 1', 'stop': ['pitch 0']},
            'turn': {'right': 'turn 1', 'left': 'turn -1', 'stop': ['turn 0'], 'to': 'LIST OF ENTITIES/OBJECTS'},
            'crouch': {'': 'crouch 1', 'stop': ['crouch 0']},
            'attack': {'': 'attack 1', 'stop': ['attack 0']},
            'dig': {'': 'attack 1'},
            'use': 'INVENTORY LIST',
            'stop': ['move 0', 'jump 0', 'turn 0', 'strafe 0', 'pitch 0', 'crouch 0', 'attack 0'],
            'go': {'to': []}, #object and entity list?
            'pick': {'up': 'LIST OF ENTITIES/OBJECTS'}
        }


    def parseCommands( self, doc ):
        self.doc_ = doc
        if self.doc_ is not None:
            for sentence in self.doc_.sents:
                root = sentence.root
                print('root.text: '),
                print(root.text)
                if root.text == u'go':
                    print('returning go to')
                    return 'goto'
                elif root.text == u'stop':
                    print('returning stop')
                    return 'stop'
                self.parseVerb_(root)
        return ''

    def parseVerb_( self, verb ):
        if verb.lemma_ not in self.command_map:  # check if given verb is a valid command
            self.agent.sendCommand("chat Invalid Command")
        else:
            # rightVerbs = [child for child in verb.rights if child.pos == VERB and child.dep == conj]
            # rights = [child for child in verb.rights if child.pos != VERB]
            rights = [child for child in verb.rights]
            if rights:
                if rights[0].pos == CCONJ:
                    self.doBasicCommand_(verb)

                options = self.command_map.get(verb.lemma_)
                for r_child in rights:
                    if r_child.pos == ADV or r_child.pos == PART:  # check if option is valid with given command
                        # no parsing needed, just do command
                        # i.e. move | forward
                        if r_child.lemma_ in options:
                            if r_child.lemma == 'up':
                                # self.doObjCommand_(verb, r_child)
                                pass
                            else:
                                self.doAdvCommand_(verb, r_child)
                    elif r_child.pos == NOUN:
                        # parse for preposition and prepositional object
                        # i.e. choose | steel pickaxe (-> on -> the left)
                        # check if it's a quantitative movement i.e. 1 block forward or forward 1 block
                        if r_child.lemma_ == 'left' and r_child.lemma_ in options:
                            self.doAdvCommand_(verb, r_child)
                        else:
                            self.doObjCommand_(verb, r_child)
                    elif r_child.pos == ADP:
                        # parse for prepositional object
                        # i.e. go | to -> pobj
                        self.doPrepCommand_(verb, r_child)
                    elif r_child.pos == VERB:
                        # parse subsequent command
                        # choose steel pickaxe | (and) dig -> ...
                        if verb.lemma_ == 'stop':
                            if r_child.lemma_ in self.command_map:
                                self.doStopCommand_(r_child)
                        else:
                            self.parseVerb_(r_child)
            else:
                self.doBasicCommand_(verb)


    def doBasicCommand_( self, verb ):
        # command = '{} {}'.format(verb.text, 1)
        command = self.command_map.get(verb.lemma_).get('')
        print 'Sending command: {}'.format(command)
        self.agent.sendCommand(command)
        time.sleep(0.5)


    def doStopCommand_( self, verb ):
        # command = self.command_map.get(verb.lemma_).get('stop')
        # print 'Sending command: {}'.format(command)
        # self.agent.sendCommand(command)
        stop_commands = self.command_map.get(verb.lemma_).get('stop')
        for command in stop_commands:
            print 'Sending command: {}'.format(command)
            self.agent.sendCommand(command)

    def doAdvCommand_( self, verb, option ):
        command = self.command_map.get(verb.lemma_).get(option.lemma_)
        print 'Sending command: {}'.format(command)
        self.agent.sendCommand(command)
        time.sleep(0.5)


    def doObjCommand_( self, verb, obj ):
        objString = getObjectString(obj)
        if verb.lemma_ == 'use':
            hotkey = getHotKeyForItem(objString, self.agent)
            print 'hotbar.%d' % hotkey
            self.agent.sendCommand('hotbar.%d 1' % hotkey)
            self.agent.sendCommand('hotbar.%d 0' % hotkey)
        elif verb.lemma_ == 'attack':
            pass
        elif verb.lemma_ == 'grab':
            pass


    def doPrepCommand_( self, verb, prep ):
        if prep.n_rights:
            rights = list(prep.rights)
            pobj = prep.rights[0]
            ### if object exists --> Howard's code to move to said object
            ### HowardCode(verb, obj, agent)




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
            string += child.lemma_ + '_'
    string += obj.lemma_

    return string

def getHotKeyForItem( item, agent ):
    world_state = agent.getWorldState()
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        ob = json.loads(msg)
        for i in xrange(9):
            slot_name = u'Hotbar_' + str(i) + '_item'
            slot_contents = ob.get(slot_name, "")
            if slot_contents == item:
                return i + 1  # +1 to convert from 0-based inventory slot to 1-based hotbar key.

    return -1