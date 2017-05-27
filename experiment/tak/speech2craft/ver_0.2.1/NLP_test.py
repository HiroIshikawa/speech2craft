import spacy
from spacy.symbols import *




# command map: modify this for registering malmo commands
commandMap = {
    'move': {'forward': 1, 'back': -1, 'stop': 0, 'to': ''},  # 'go':['forward','back'],
    'strafe': {'right': 1, 'left': -1, 'stop': 0},
    'pitch': {'up': -1, 'down': 1, 'stop': 0},  # 'look':['up', 'down'],
    'turn': {'right': 1, 'left': -1, 'stop': 0},
    'jump': {'': 1, 'stop': 0},
    'crouch': {'': 1, 'stop': 0},
    'attack': {'': 1},
    'use': {'': 1},
    'stop': {'move': 0, 'strafe': 0, 'pitch': 0, 'jump': 0, 'crouch': 0}
}

def getVerbs(doc):
    return [word for word in doc if word.pos == VERB]


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


def doAdvCommand(verb, option, agent):
    options = commandMap.get(verb.text)
    action = options.get(option.text)
    command = '{} {}'.format(verb.text, action)
    print 'Sending command: {}'.format(command)
    agent.sendCommand(command)
    time.sleep(0.5)

def doStopCommand(verb, agent):
    command = '{} {}'.format(verb.text, 0)
    print 'Sending command: {}'.format(command)
    agent.sendCommand(command)

def doBasicCommand(verb, agent):
    command = '{} {}'.format(verb.text, 1)
    print 'Sending command: {}'.format(verb.text)
    agent.sendCommand(command)
    time.sleep(0.5)


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
                        doStopCommand(verb, agent)
                elif r_child.pos == NOUN:
                    # parse for preposition and prepositional object
                    # i.e. choose | steel pickaxe (-> on -> the left)
                    doObjCommand(verb, r_child, agent)
                elif r_child.pos == ADP:
                    # parse for prepositional object
                    # i.e. go | to -> pobj
                    doPrepCommand(verb, r_child, agent)
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
            doStopCommand(verb, agent)

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

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately


def Menger(xorg, yorg, zorg, size, blocktype, holetype):
    # draw solid chunk
    genstring = GenCuboid(xorg, yorg, zorg, xorg + size - 1, yorg + size - 1, zorg + size - 1, blocktype) + "\n"
    # now remove holes
    unit = size
    while (unit >= 3):
        w = unit / 3
        for i in xrange(0, size, unit):
            for j in xrange(0, size, unit):
                x = xorg + i
                y = yorg + j
                genstring += GenCuboid(x + w, y + w, zorg, (x + 2 * w) - 1, (y + 2 * w) - 1, zorg + size - 1,
                                       holetype) + "\n"
                y = yorg + i
                z = zorg + j
                genstring += GenCuboid(xorg, y + w, z + w, xorg + size - 1, (y + 2 * w) - 1, (z + 2 * w) - 1,
                                       holetype) + "\n"
                genstring += GenCuboid(x + w, yorg, z + w, (x + 2 * w) - 1, yorg + size - 1, (z + 2 * w) - 1,
                                       holetype) + "\n"
        unit /= 3
    return genstring


def GenCuboid(x1, y1, z1, x2, y2, z2, blocktype):
    return '<DrawCuboid x1="' + str(x1) + '" y1="' + str(y1) + '" z1="' + str(z1) + '" x2="' + str(x2) + '" y2="' + str(
        y2) + '" z2="' + str(z2) + '" type="' + blocktype + '"/>'


"""
missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

              <About>
                <Summary>Hello world!</Summary>
              </About>

            <ServerSection>
              <ServerInitialConditions>
                <Time>
                    <StartTime>12000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
              </ServerInitialConditions>
              <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"/>
                  <DrawingDecorator>
                    <DrawSphere x="-27" y="70" z="0" radius="30" type="air"/>''' + Menger(-40, 40, -13, 27, "wool", "air") + '''
                  </DrawingDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="1000000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>

              <AgentSection mode="Survival">
                <Name>MalmoTutorialBot</Name>
                <AgentStart>
                    <Placement x="0.5" y="56.0" z="0.5" yaw="90"/>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''
"""

missionXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
              <About>
                <Summary>Default gameplay</Summary>
              </About>

              <ServerSection>
                <ServerInitialConditions>
                  <Time>
                    <StartTime>6000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                  </Time>
                  <Weather>clear</Weather>
                </ServerInitialConditions>
                <ServerHandlers>
                  <!--<FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1"/>-->
                  <DefaultWorldGenerator forceReset="true"/>
                  <ServerQuitFromTimeUp timeLimitMs="300000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>

              <AgentSection mode="Survival">
                <Name>Recorder Agent</Name>
                <AgentStart/>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <VideoProducer want_depth="false">
                    <Width>640</Width>
                    <Height>480</Height>
                  </VideoProducer>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''

# Create default Malmo objects:

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

# my_mission = MalmoPython.MissionSpec()
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

    print
    text = raw_input("Enter command: ")
    parseText(text, agent_host)

    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:", error.text

print
print "Mission ended"
# Mission has ended.



























# malmo_commands = [u'move', u'strafe', u'pitch', u'turn', u'jump', u'crouch', u'attack', u'use', u'craft', u'hotbar.', u'quit']


# def findBestMatch(user_command):
#     max = 0
#     for command in malmo_commands:
#         sim = user_command.similarity(command)
#         if (sim > max):
#             max = sim
#             best_match = command
#     return best_match


# class Adverb:
#     def __init__(self, token):
#         self.token = token
#
#     def display(self):
#         print self.token.text
#
#
# class Adjective:
#     def __init__(self, token):
#         self.token = token
#
#     def display(self):
#         print self.token.text
#
# class Preposition:
#     def __init__(self, token):
#         self.token = token
#         self.obj = None
#
#         for tok in token.rights:
#             if tok.dep == pobj:
#                 self.obj = Object(token)
#
#     def display(self):
#         if self.obj:
#             print '<-', self.obj.display(),
#         print self.token.text
#
#
#
# class Object:
#     def __init__(self, token):
#         self.token = token
#         self.adj = None
#         self.comp = None
#         self.prep = None
#
#         for tok in token.lefts:
#             if tok.pos == ADJ:
#                 self.adj = Adjective(tok)
#             elif tok.dep == nn:
#                 self.comp = tok.text
#         for tok in token.rights:
#             if tok.dep == prep:
#                 self.prep = Preposition(tok)
#
#     def display(self):
#         if self.comp:
#             print self.comp,
#         print self.token.text
#
#
# class Verb:
#     def __init__(self, token):
#         self.token = token
#         self.obj = None
#         self.adv = None
#         self.prep = None
#
#         for tok in token.rights:
#             if tok.pos == NOUN:
#                 self.obj = Object(tok)
#             elif tok.pos == ADV:
#                 self.adv = Adjective(tok)
#             elif tok.dep == prep:
#                 self.prep = Preposition(tok)
#
#     def display(self):
#         print self.token.text
#         if self.obj:
#             print '\t', self.obj.display()
#         if self.prep:
#             print '\t', self.prep.display()
#         if self.adv:
#             print '\t', self.adv.display()
#

# def parsePrep(obj, prep):
#     for r_child in prep.rights:
#         if r_child.pos == NOUN:

# class Preposition:
#     def __init__(self, prep=None, pobj=None):
#         self.prep = obj
#         self.pobj = pobj
#
# class Object:
#     def __init__(self, obj=None, prep=None):
#         self.obj = obj
#         self.prep = prep

# def parseObj(obj):
#     object = Object(obj)
#     if obj.nbor(1) == ADP:
#         prep = obj.nbor(1)
#         pobj = obj.nbor(2)
#         object.prep = Preposition(prep, pobj)
#     return object