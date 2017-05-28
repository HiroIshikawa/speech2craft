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
import json
import errno
import math

import command
import simple_parser

from collections import namedtuple
EntityInfo = namedtuple('EntityInfo', 'x, y, z, yaw, pitch, name')
# EntityInfo = namedtuple('EntityInfo', 'x, y, z, yaw, pitch, name, colour, variation, quantity')
EntityInfo.__new__.__defaults__ = (0, 0, 0, 0, 0, "")

AgentInfo = namedtuple('AgentInfo', 'XPos, YPos, ZPos, Yaw, Pitch, Name')
AgentInfo.__new__.__defaults__ = (0, 0, 0, 0, 0, "")


# Task params:
NUM_GOALS = 1
GOAL_TYPE = "Pig"
GOAL_REWARD = 100
ARENA_WIDTH = 60
ARENA_BREADTH = 60
MOB_TYPE = "Pig"  # Change for fun, but note that spawning conditions have to be correct - eg spiders will require darker conditions.


# Agent params:
agent_stepsize = 1
agent_search_resolution = 30 # Smaller values make computation faster, which seems to offset any benefit from the higher resolution.
agent_goal_weight = 100
agent_edge_weight = -100
agent_mob_weight = -10
agent_turn_weight = 0 # Negative values to penalise turning, positive to encourage.


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


def getClosestEntity(agent, entities):
    ag_x = agent[0]
    ag_z = agent[2]
    dists = { i:abs(ag_x-ent[0])+abs(ag_z-ent[2]) for i,ent in enumerate(entities) if ent[5] != 'Rover'}
    return entities[min(dists, key=dists.get)]

def getClosestGoal(agent, entities):
    ag_x = agent[0]
    ag_z = agent[2]
    dists = { i:abs(ag_x-ent[0])+abs(ag_z-ent[2]) for i,ent in enumerate(entities) if ent[5] == GOAL_TYPE}
    return entities[min(dists, key=dists.get)]

def getBestAngle(entities, current_yaw):
    agent = next(ent for ent in entities if ent[5] == 'Rover')
    closest_entity = getClosestEntity(agent, entities)
    # print('Closest entity: ')
    # print(closest_entity)
    scores = []
    while current_yaw < 0:
        current_yaw += 360
    while current_yaw > 360:
        current_yaw -= 360

    for i in xrange(agent_search_resolution):
        # Calculate cost of turning:
        ang = 2 * math.pi * (i / float(agent_search_resolution))
        yaw = i * 360.0 / float(agent_search_resolution)
        yawdist = min(abs(yaw-current_yaw), 360-abs(yaw-current_yaw))
        turncost = agent_turn_weight * yawdist
        score = turncost

        # Calculate entity proximity cost for new (x,z):
        x = agent.x + agent_stepsize - math.sin(ang)
        z = agent.z + agent_stepsize * math.cos(ang)
        for ent in entities:
            dist = (ent.x - x)*(ent.x - x) + (ent.z - z)*(ent.z - z)
            if (dist == 0):
                continue
            weight = 0.0
            # if ent.name == MOB_TYPE:
            #     weight = agent_mob_weight
            #     dist -= 1   # assume mobs are moving towards us
            #     if dist <= 0:
            #         dist = 0.1
            current_health = 20.0
            if ent.name == GOAL_TYPE:
                weight = agent_goal_weight * current_health / 20.0
            score += weight / float(dist)

        # Calculate cost of proximity to edges:
        distRight = (2+ARENA_WIDTH/2) - x
        distLeft = (-2-ARENA_WIDTH/2) - x
        distTop = (2+ARENA_BREADTH/2) - z
        distBottom = (-2-ARENA_BREADTH/2) - z
        score += agent_edge_weight / float(distRight * distRight * distRight * distRight)
        score += agent_edge_weight / float(distLeft * distLeft * distLeft * distLeft)
        score += agent_edge_weight / float(distTop * distTop * distTop * distTop)
        score += agent_edge_weight / float(distBottom * distBottom * distBottom * distBottom)
        scores.append(score)

    # Find best score:
    i = scores.index(max(scores))
    # Return as an angle in degrees:
    return i * 360.0 / float(agent_search_resolution)

def getDistanceToGoal(entities):
    agent = next(ent for ent in entities if ent[5] == 'Rover')
    ag_x = agent[0]
    ag_z = agent[2]
    # ang = 2 * math.pi * (i / float(agent_search_resolution))
    # x = agent.x + agent_stepsize - math.sin(ang)
    # z = agent.z + agent_stepsize * math.cos(ang)
    ent = getClosestGoal(agent, entities)
    # dist = (ent.x - x)*(ent.x - x) + (ent.z - z)*(ent.z - z)
    dist = abs(ag_x-ent[0])+abs(ag_z-ent[2])
    return dist

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

best_yaw = 0
current_yaw = 0

# Loop until mission ends:
# agent_host.sendCommand("move 1")    # run!
while world_state.is_mission_running:
    #sys.stdout.write(".")
    time.sleep(0.1)
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        ob = json.loads(msg)
        # print(ob)
        if "Yaw" in ob:
            current_yaw = ob[u'Yaw']
        if "entities" in ob:
            # ag = {k:v for k,v in ob.iteritems() if k in ['XPos','YPos','ZPos','Yaw','Pitch','Name']}
            # agent = AgentInfo(**ag)
            entities = [EntityInfo(**k) for k in ob["entities"]]
            # print('Agent condition: ')
            # print(agent)
            # print('Entitires condition: ')
            # print(entities)

            best_yaw = getBestAngle(entities, current_yaw)

            print('Best yaw: '),
            print(best_yaw)
            difference = best_yaw - current_yaw;
            while difference < -180:
                difference += 360;
            while difference > 180:
                difference -= 360;
            difference /= 180.0;

            distance_to_goal = getDistanceToGoal(entities)
            if distance_to_goal <= 5:
                agent_host.sendCommand("move 0")
            else:
                agent_host.sendCommand("move 1")

            print('Distance to goal: '),
            print(distance_to_goal)

            agent_host.sendCommand("turn " + str(difference))
            # total_commands += 1
            # difference = best_yaw - current_yaw;
            # while difference < -180:
            #     difference += 360;
            # while difference > 180:
            #     difference -= 360;
            # difference /= 180.0;
            # agent_host.sendCommand("turn " + str(difference))
    # print
    # text = raw_input("Enter command: ")
    # simple_parser.parseText(text, agent_host)

    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:", error.text

print
print "Mission ended"
# Mission has ended.