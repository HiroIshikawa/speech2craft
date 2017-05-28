import os
import sys
import time
import command
import random
import json

import spacy
from spacy.symbols import *


def printDependencies(doc):
    for word in doc:
        print(word.text, word.dep_, word.dep, word.pos_, word.head.text, [w.text for w in word.lefts], [w.text for w in word.rights])

def printSubtrees(doc):
    for word in doc:
        if word.pos == NOUN:
            for child in word.subtree:
                print child.text, ',',
        print

def printNounChunks(doc):
    for word in doc.noun_chunks:
        print word.text

def printAncestors(doc):
    for word in doc:
        print [tok for tok in word.ancestors]

def printConjuncts(doc):
    for word in doc:
        print [tok for tok in word.conjuncts]


# command map: modify this for registering malmo commands
commandMap = {
    'move': {
        'forward': 'move 1', 'back': 'move -1', 'right': 'strafe 1', 'left': 'strafe -1',
        'north': 'movenorth 1', 'south': 'movesouth 1', 'east': 'moveeast 1', 'west': 'movewest 1', 'to': ''
    },
    'look': {'up': 'look -1', 'down': 'look 1'},
    'turn': {'right': 'turn 1', 'left': 'turn -1'},
    'jump': {'forward': 'jumpmove 1', 'back': 'jumpmove -1', 'right': 'jumpstrafe 1', 'left': 'jumpstrafe -1'},
    'crouch': {'': 'crouch 1'},
    'attack': {'': 'attack 1'},
    'use': {'': 1},
    'stop': {'move': 0, 'strafe': 0, 'pitch': 0, 'jump': 0, 'crouch': 0}
}


def doAdvCommand(verb, option, agent):
    options = commandMap.get(verb.text)
    #action = options.get(option.text)
    #command = '{} {}'.format(verb.text, action)
    command = options.get(option.text)
    print 'Sending command: {}'.format(command)
    agent.sendCommand(command)
    time.sleep(1)

def doStopCommand(verb, agent):
    command = '{} {}'.format(verb.text, 0)
    print 'Sending command: {}'.format(command)
    agent.sendCommand(command)

def doBasicCommand(verb, agent):
    command = '{} {}'.format(verb.text, 1)
    print 'Sending command: {}'.format(command)
    agent.sendCommand(command)
    time.sleep(1)


def doObjCommand(verb, obj, agent):
    ### GOING TO HAVE TO DO SOME OBJECT ANALYSIS...
    ### i.e. object: 'the closest pig'
    ### could also just have a map that defines all possible objects, rendering an object like above not valid

    # prep = None
    # if obj.nbor(1).pos == ADP:
    #     prep = obj.nbor(1)
    #     pobj = obj.nbor(2)
    #
    # commandString = '{} {}'
    # if prep:
    #     commandString += '{} {}'
    #     command = commandString.format(verb.text, obj.text, prep.text, pobj.text)
    # else:
    #     command = '{} {}'.format(verb.text, obj.text)

    # send command
    pass


def doPrepCommand(verb, prep, agent):
    pobj = obj.nbor(1)
    command = '{} {} {}'.format(verb.text, prep.text, pobj.text)
    # send command


def parseVerb(verb, agent):
    # for l_child in verb.lefts:
    #     if l_child.pos == ADV: # not necessary atm
    #         continue

    if verb.text in commandMap: # check if given verb is a valid command
        rights = [child for child in verb.rights]
        if rights:
            for r_child in rights:
                print 'RIGHT CHILD: ',r_child.text
                if r_child.pos == ADV or r_child.pos == PART: # check if option is valid with given command
                    # no parsing needed, just do command
                    # i.e. move | forward
                    options = commandMap.get(verb.text)
                    if r_child.text in options:
                        doAdvCommand(verb, r_child, agent)
                elif r_child.pos == NOUN:
                    # parse for preposition and prepositional object
                    # i.e. choose | steel pickaxe (-> on -> the left)
                    doObjCommand(verb, r_child, agent)
                elif r_child.pos == ADP:
                    # parse for prepositional object
                    # i.e. go | to -> pobj
                    doPrepCommand(verb, r_child, agent)
                #elif r_child.pos == CCONJ:
                #    doBasicCommand(verb, agent)
                elif r_child.pos == VERB:
                    # parse subsequent command
                    # choose steel pickaxe | (and) dig -> ...
                    if verb.lower_ == 'stop':
                        if r_child.text in commandMap:
                            doStopCommand(verb, agent)
                    else:
                        parseVerb(r_child, agent)
        else:
            doBasicCommand(verb, agent)

def parseText(text, agent):
    doc = nlp(text.decode("utf-8"))
    printDependencies(doc)

    for np in doc.noun_chunks:
         np.merge(np.root.tag_, np.text, np.root.ent_type_)

    for sentence in doc.sents:
        root = sentence.root
        parseVerb(root, agent)


nlp = spacy.load('en')
