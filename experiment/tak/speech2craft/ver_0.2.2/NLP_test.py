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







# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #1: Run simple mission

import MalmoPython
import os
import sys
import time
import command
import random
import json
from collections import namedtuple
EntityInfo = namedtuple('EntityInfo', 'x, y, z, yaw, pitch, name, colour, variation, quantity')
# EntityInfo = namedtuple('EntityInfo', 'x, y, z, yaw, pitch, name, colour, variation, quantity')
EntityInfo.__new__.__defaults__ = (0, 0, 0, 0, 0, "", "", "", 1)


ARENA_WIDTH = 60
ARENA_BREADTH = 60
MOB_TYPE = "Pig"

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

spawn_end_tag = ' type="mob_spawner" variant="' + MOB_TYPE + '"/>'
missionXML = '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>Normal life</Summary>
        </About>

        <ServerSection>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"/>
                    <DrawingDecorator>
                        <DrawEntity x="0" y="56" z="0" type="Pig"/>
                        <!--<DrawBlock type="mob_spawner" variant="Pig" x="0" y="56" z="0"/>-->
                    </DrawingDecorator>
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>Rover</Name>
            <AgentStart>
                <Placement x="0.5" y="56.0" z="0.5" yaw="90"/>
                <Inventory>
                    <InventoryBlock slot="0" type="glowstone" quantity="63"/>
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <AbsoluteMovementCommands />
                <DiscreteMovementCommands />
                <InventoryCommands />
                <ObservationFromFullStats/>
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="'''+str(ARENA_WIDTH)+'''" yrange="2" zrange="'''+str(ARENA_BREADTH)+'''" />
                </ObservationFromNearbyEntities>
            </AgentHandlers>
        </AgentSection>

    </Mission>'''



# Create default Malmo objects:
# <ContinuousMovementCommands />

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse(sys.argv)
except RuntimeError as e:
    print 'ERROR:', e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)

my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission(my_mission, my_mission_record)
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print "Error starting mission:", e
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print "Waiting for the mission to start ",
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:", error.text

print
print "Mission running ",

# Loop until mission ends:
while world_state.is_mission_running:
    #sys.stdout.write(".")
    time.sleep(0.1)
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        ob = json.loads(msg)
        if "entities" in ob:
            entities = [EntityInfo(**k) for k in ob["entities"]]
            print(entities)
    print
    text = raw_input("Enter command: ")
    parseText(text, agent_host)

    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:", error.text

print
print "Mission ended"
# Mission has ended.
