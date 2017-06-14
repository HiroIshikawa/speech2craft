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
import random
import json
from collections import namedtuple

from command_parse import CommandParser
from command_parse import TextParser

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
            <ServerInitialConditions>
                <Time>
                    <StartTime>1000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
            </ServerInitialConditions>
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
                    <InventoryBlock slot="0" type="diamond_pickaxe" quantity="1"/>
                    <InventoryBlock slot="1" type="diamond_sword" quantity="1"/>
                    <InventoryBlock slot="2" type="iron_sword" quantity="1"/>
                    <InventoryBlock slot="3" type="stone" quantity="2"/>
                    <InventoryBlock slot="4" type="heavy_weighted_pressure_plate" quantity="1"/>
                    <InventoryBlock slot="5" type="light_weighted_pressure_plate" quantity="1"/>
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <AbsoluteMovementCommands />
                <ContinuousMovementCommands />
                <DiscreteMovementCommands />
                <InventoryCommands />
                <SimpleCraftCommands />
                <ChatCommands />
                <MissionQuitCommands />

                <ObservationFromRay />
                <ObservationFromFullInventory />
                <ObservationFromHotBar />
                <ObservationFromFullStats />
                <ObservationFromDiscreteCell />
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="''' + str(ARENA_WIDTH) + '''" yrange="2" zrange="''' + str(
    ARENA_BREADTH) + '''" />
                </ObservationFromNearbyEntities>
            </AgentHandlers>
        </AgentSection>

    </Mission>'''

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

text_parser = TextParser()
command_parser = CommandParser(agent_host)

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

import speech_recognition as sr

# Loop until mission ends:
while world_state.is_mission_running:
    # sys.stdout.write(".")
    time.sleep(0.1)

    # if world_state.number_of_observations_since_last_state > 0:
    #     msg = world_state.observations[-1].text
    #     ob = json.loads(msg)
    #     if "entities" in ob:
    #         entities = [EntityInfo(**k) for k in ob["entities"]]
    #         print(entities)
    #
    # print

    # r = sr.Recognizer()
    # with sr.Microphone() as source:
    #     print("Say something!")
    #     audio = r.listen(source)
    #
    # text = ''
    # try:
    #     text = r.recognize_google(audio)
    #     print 'I heard you say: ' + text
    # except sr.UnknownValueError:
    #     print("Could not understand audio")
    # except sr.RequestError as e:
    #     print("Could not request results from Google Speech Recognition service; {0}".format(e))

    text = raw_input("Enter command: ")

    doc = text_parser.parse(text)
    text_parser.printDependencies()
    command_parser.parseCommands(doc)

    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:", error.text

print
print "Mission ended"


# Mission has ended.