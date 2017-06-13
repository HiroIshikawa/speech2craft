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
import Tkinter as tk
from collections import namedtuple
EntityInfo = namedtuple('EntityInfo', 'x, y, z, yaw, pitch, name')
# EntityInfo = namedtuple('EntityInfo', 'x, y, z, yaw, pitch, name, colour, variation, quantity')
EntityInfo.__new__.__defaults__ = (0, 0, 0, 0, 0, "")

AgentInfo = namedtuple('AgentInfo', 'XPos, YPos, ZPos, Yaw, Pitch, Name')
AgentInfo.__new__.__defaults__ = (0, 0, 0, 0, 0, "")


# Task params:
AGENT_TYPE = "Rover"
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


#Our display parameters
CANVAS_BORDER = 20
CANVAS_WIDTH = 400
CANVAS_HEIGHT = CANVAS_BORDER + ((CANVAS_WIDTH - CANVAS_BORDER) * ARENA_BREADTH / ARENA_WIDTH)
CANVAS_SCALEX = (CANVAS_WIDTH-CANVAS_BORDER)/ARENA_WIDTH
CANVAS_SCALEY = (CANVAS_HEIGHT-CANVAS_BORDER)/ARENA_BREADTH
CANVAS_ORGX = -ARENA_WIDTH/CANVAS_SCALEX
CANVAS_ORGY = -ARENA_BREADTH/CANVAS_SCALEY


sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

def getCorner(index,top,left,expand=0,y=206):
    ''' Return part of the XML string that defines the requested corner'''
    x = str(-(expand+ARENA_WIDTH/2)) if left else str(expand+ARENA_WIDTH/2)
    z = str(-(expand+ARENA_BREADTH/2)) if top else str(expand+ARENA_BREADTH/2)
    return 'x'+index+'="'+x+'" y'+index+'="' +str(y)+'" z'+index+'="'+z+'"'

############GENERATE THE XML#################
def getMissionXML():
    spawn_end_tag = ' type="mob_spawner" variant="' + MOB_TYPE + '"/>'
    missionXML = '''<?xml version="1.0" encoding="UTF-8" ?>
        <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <About>
                <Summary>Normal life</Summary>
            </About>

            <ServerSection>
                <ServerInitialConditions>
                    <Time>
                        <StartTime>6000</StartTime>
                    </Time>
                </ServerInitialConditions>
                <ServerHandlers>
                    <FlatWorldGenerator generatorString="3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"/>
                        <DrawingDecorator>
                            <DrawCuboid ''' + getCorner("1",True,True,expand=1) + " " + getCorner("2",False,False,y=226,expand=1) + ''' type="sandstone"/>
                            <DrawCuboid ''' + getCorner("1",True,True,y=207) + " " + getCorner("2",False,False,y=226) + ''' type="air"/>
                            <DrawEntity x="0.5" y="210" z="10" type="Pig"/>
                            <DrawBlock x="-4" y="207" z="4" type="diamond_block"/>
                            <DrawBlock x="-4" y="208" z="4" type="diamond_block"/>
                            <DrawBlock x="-3" y="207" z="4" type="diamond_block"/>
                            <DrawBlock x="-3" y="208" z="4" type="diamond_block"/>
                            <DrawBlock x="-2" y="207" z="4" type="diamond_block"/>
                            <DrawBlock x="-2" y="208" z="4" type="diamond_block"/>
                            <DrawBlock x="-1" y="207" z="4" type="diamond_block"/>
                            <DrawBlock x="-1" y="208" z="4" type="diamond_block"/>
                            <DrawBlock x="0" y="207" z="4" type="diamond_block"/>
                            <DrawBlock x="0" y="208" z="4" type="diamond_block"/>
                            <DrawBlock x="1" y="207" z="4" type="diamond_block"/>
                            <DrawBlock x="1" y="208" z="4" type="diamond_block"/>
                            <DrawBlock x="2" y="207" z="4" type="diamond_block"/>
                            <DrawBlock x="2" y="208" z="4" type="diamond_block"/>
                            <DrawBlock x="3" y="207" z="4" type="diamond_block"/>
                            <DrawBlock x="3" y="208" z="4" type="diamond_block"/>


                            <DrawEntity x="10" y="210" z="10" type="Sheep"/>
                            <DrawEntity x="10" y="210" z="0" type="Cow"/>
                            <!--<DrawBlock type="mob_spawner" variant="Pig" x="0" y="56" z="0"/>-->
                        </DrawingDecorator>
                </ServerHandlers>
            </ServerSection>

            <AgentSection mode="Survival">
                <Name>Rover</Name>
                <AgentStart>
                    <Placement x="0.5" y="210" z="-8.5" yaw="0"/>
                    <Inventory>
                        <InventoryBlock slot="0" type="glowstone" quantity="63"/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                    <DiscreteMovementCommands />
                    <AbsoluteMovementCommands />
                    <ContinuousMovementCommands turnSpeedDegs="360"/>
                    <InventoryCommands />
                    <ObservationFromFullStats/>
                    <ObservationFromRecentCommands/>
                    <ObservationFromGrid>
                        <Grid name="fullGrid">
                            <min x="-2" y="0" z="-2"/>
                            <max x="2" y="2" z="2"/>
                        </Grid>
                    </ObservationFromGrid>
                    <ObservationFromNearbyEntities>
                        <Range name="entities" xrange="'''+str(ARENA_WIDTH)+'''" yrange="25" zrange="'''+str(ARENA_BREADTH)+'''" />
                    </ObservationFromNearbyEntities>
                    <ObservationFromDiscreteCell/>
                </AgentHandlers>
            </AgentSection>

        </Mission>'''
    return missionXML


###########Finding object functions##########
def checkWall(agent, world_state, command):
    if len(world_state.errors) > 0:
        raise AssertionError('Could not load grid.')

    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        observations = json.loads(msg)
        current_yaw = 0
        if "Yaw" in observations:
            current_yaw = ob[u'Yaw']
        grid = observations.get(u'fullGrid', 0)

        front = grid[15:20] #this is the 5 blocks in front of the agent
        aboveFront = grid[40:45] #this is the 5 blocks above the ones in the front
        behindFront = grid[21:26] # this is the 5 blocks 2 in front
        behindAboveFront = grid[45:50]
        # print(grid)
        if aboveFront[1] != "air" and aboveFront[2] != "air" and aboveFront[3] != "air" and command:
            print("Found a wall, stopping")
            agent_host.sendCommand("move 0")
            return "move 0"
        if aboveFront[2] != u"air":
            print("Something above, try going around")
            difference = 90 - current_yaw
            while difference < -180:
                difference += 360;
            while difference > 180:
                difference -= 360;
            difference /= 180.0;
            agent_host.sendCommand("turn " + str(difference))
            time.sleep(0.1)
            agent_host.sendCommand("move 1")
        if front[2] != u"air" and aboveFront[2] == u"air":
            print("Something in front and can jump")
            agent_host.sendCommand("move 0")
            agent_host.sendCommand("jumpmove 1")
            return "jumpmove 1"
        return grid
    return []

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

def parseCommands(commandsList):
    for command in commandsList:
        if "move 1" == command:
            return True
    return False

#########CANVAS FUNCTIONS###################
def canvasX(x):
    return (CANVAS_BORDER/2) + (0.5 + x/float(ARENA_WIDTH)) * (CANVAS_WIDTH-CANVAS_BORDER)

def canvasY(y):
    return (CANVAS_BORDER/2) + (0.5 + y/float(ARENA_BREADTH)) * (CANVAS_HEIGHT-CANVAS_BORDER)

def drawMobs(entities):
    canvas.delete("all")
    canvas.create_rectangle(canvasX(-ARENA_WIDTH/2), canvasY(-ARENA_BREADTH/2), canvasX(ARENA_WIDTH/2), canvasY(ARENA_BREADTH/2), fill="#888888")
    for ent in entities:
        if ent.name == MOB_TYPE:
            canvas.create_oval(canvasX(ent.x)-2, canvasY(ent.z)-2, canvasX(ent.x)+2, canvasY(ent.z)+2, fill="#4422ff")
        elif ent.name == GOAL_TYPE:
            canvas.create_oval(canvasX(ent.x)-3, canvasY(ent.z)-3, canvasX(ent.x)+3, canvasY(ent.z)+3, fill="#4422ff")
        elif ent.name == AGENT_TYPE:
            canvas.create_oval(canvasX(ent.x)-4, canvasY(ent.z)-4, canvasX(ent.x)+4, canvasY(ent.z)+4, fill="#22ff44")
        else:
            canvas.create_oval(canvasX(ent.x)-4, canvasY(ent.z)-4, canvasX(ent.x)+4, canvasY(ent.z)+4, fill="#ff00ff")
    root.update()



# Create default Malmo objects:
# <ContinuousMovementCommands />


#SETUP the canvas environment
root = tk.Tk()
root.wm_title("NLP Simulation View")

canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, borderwidth=0, highlightthickness=0, bg="black")
canvas.pack()
root.update()

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

my_mission = MalmoPython.MissionSpec(getMissionXML(), True)
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
count = 0
posCounter = 0
trackX = 0
trackY = 0
trackZ = 0


HOW_LONG_TO_WAIT = 5
# Loop until mission ends:
# agent_host.sendCommand("move 1")    # run!
time.sleep(0.5)
stopMoving = False
while world_state.is_mission_running:
    #sys.stdout.write(".")
    time.sleep(0.1)
    count += 1
    print("Iteration:",count)
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        ob = json.loads(msg)
        # print(ob)
        if "Yaw" in ob:
            current_yaw = ob[u'Yaw']
        # if "CommandsSinceLastObservation" in ob:
        #     if parseCommands(ob["CommandsSinceLastObservation"]):
        #         if posCounter == 0 and "XPos" in ob and "YPos" in ob and "ZPos" in ob:
        #             trackX = ob["XPos"]
        #             trackY = ob["YPos"]
        #             trackZ = ob["ZPos"]
        #         posCounter += 1
        #         if posCounter > HOW_LONG_TO_WAIT and "XPos" in ob and "YPos" in ob and "ZPos" in ob:
        #             # check if the agent is within a range and isn't getting anywhere despite having an action
        #             if abs(trackX - ob["XPos"]) < 0.2 and abs(trackY - ob["YPos"]) < 0.2 and abs(trackZ - ob["ZPos"]) < 0.2:
        #             # if trackX == ob["XPos"] and trackY == ob["YPos"] and trackZ == ob["ZPos"]:
        #                 # print(ob)
        #
        #                 print("*************JUMPING*************")
        #                 agent_host.sendCommand("move 0")
        #                 agent_host.sendCommand("jumpmove 1")
        #
        #             trackX = ob["XPos"]
        #             trackY = ob["YPos"]
        #             trackZ = ob["ZPos"]
        #             posCounter == 0
        if "entities" in ob:
            # ag = {k:v for k,v in ob.iteritems() if k in ['XPos','YPos','ZPos','Yaw','Pitch','Name']}
            # agent = AgentInfo(**ag)
            entities = [EntityInfo(**k) for k in ob["entities"]]
            # print('Agent condition: ')
            # print(agent)
            # print('Entitires condition: ')
            # print(entities)
            # for ent in entities:
            #     if ent[5] == "Rover":
            #         entX = ent[0]
            #         entY = ent[1]
            #         entZ = ent[2]


            newCommand = checkWall(agent_host,world_state, False)
            if newCommand == "move 0":
                stopMoving = True
            # agent_host.sendCommand(newCommand)

            drawMobs(entities)
            best_yaw = getBestAngle(entities, current_yaw)


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
                if not stopMoving:
                    agent_host.sendCommand("move 1")


            # print('Distance to goal: '),
            # print(distance_to_goal)

            agent_host.sendCommand("turn " + str(difference))


    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:", error.text

print
print "Mission ended"
# Mission has ended.
