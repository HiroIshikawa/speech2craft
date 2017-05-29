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
import random
import sys
import time
import threading
import errno

import command_parse
import task

time.sleep(1)

current_task = ''

# Task params:
NUM_GOALS = 1
GOAL_REWARD = 100
ARENA_WIDTH = 60
ARENA_BREADTH = 60
MOB_TYPE = "Pig"  # Change for fun, but note that spawning conditions have to be correct - eg spiders will require darker conditions.


sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

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
                        <DrawEntity x="0" y="56" z="10" type="Pig"/>
                        <DrawEntity x="10" y="56" z="10" type="Sheep"/>
                        <DrawEntity x="10" y="56" z="0" type="Cow"/>
                        <!--<DrawBlock type="mob_spawner" variant="Pig" x="0" y="56" z="0"/>-->
                    </DrawingDecorator>
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>Rover</Name>
            <AgentStart>
                <Placement x="0.5" y="56.0" z="0.5" yaw="0"/>
                <Inventory>
                    <InventoryBlock slot="0" type="glowstone" quantity="63"/>
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <AbsoluteMovementCommands />
                <DiscreteMovementCommands />
                <ContinuousMovementCommands turnSpeedDegs="360"/>
                <InventoryCommands />
                <ObservationFromFullStats/>
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="'''+str(ARENA_WIDTH)+'''" yrange="2" zrange="'''+str(ARENA_BREADTH)+'''" />
                </ObservationFromNearbyEntities>
                <ObservationFromDiscreteCell/>
            </AgentHandlers>
        </AgentSection>
    </Mission>'''



def userInput(bafa, lock):
    global current_task
    while 1:
        time.sleep(0)
        raw_input("Activate command input by hit Enter: ") 
        with lock:
            text = raw_input('Your command:> ')
            doc = text_parser.parse(text)
            current_task = command_parser.parseCommands(doc)
            print('current_task: '),
            print(current_task)

            # current_task = raw_input('Your command:> ')

        if current_task == 'quit':
            break

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
# my_mission_record = MalmoPython.MissionRecordSpec()
my_mission_record = MalmoPython.MissionRecordSpec( "./chase_pig.tgz")
my_mission_record.recordCommands()
my_mission_record.recordMP4(20, 400000)
my_mission_record.recordRewards()
my_mission_record.recordObservations()

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

command_parser = command_parse.CommandParser(agent_host)
text_parser = command_parse.TextParser()

best_yaw = 0
current_yaw = 0

bafa = ''
stdout_lock = threading.Lock()
listner_thread = threading.Thread(target=userInput, args=(bafa, stdout_lock))
listner_thread.start()
while world_state.is_mission_running:
    if current_task == 'goto':
        task.runGoto(agent_host)
    elif current_task == 'stop':
        task.runStop(agent_host)
    else:
        pass
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:", error.text

print
print "Mission ended"
# Mission has ended.