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
import math
# from collections import namedtuple
# EntityInfo = namedtuple('EntityInfo', 'x, y, z, yaw, pitch, name, colour, variation, quantity')

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately


def Menger(xorg, yorg, zorg, size, blocktype, holetype):
    #draw solid chunk
    genstring = GenCuboid(xorg,yorg,zorg,xorg+size-1,yorg+size-1,zorg+size-1,blocktype) + "\n"
    #now remove holes
    unit = size
    while (unit >= 3):
        w=unit/3
        for i in xrange(0, size, unit):
            for j in xrange(0, size, unit):
                x=xorg+i
                y=yorg+j
                genstring += GenCuboid(x+w,y+w,zorg,(x+2*w)-1,(y+2*w)-1,zorg+size-1,holetype) + "\n"
                y=yorg+i
                z=zorg+j
                genstring += GenCuboid(xorg,y+w,z+w,xorg+size-1, (y+2*w)-1,(z+2*w)-1,holetype) + "\n"
                genstring += GenCuboid(x+w,yorg,z+w,(x+2*w)-1,yorg+size-1,(z+2*w)-1,holetype) + "\n"
        unit/=3
    return genstring

def GenCuboid(x1, y1, z1, x2, y2, z2, blocktype):
    return '<DrawCuboid x1="' + str(x1) + '" y1="' + str(y1) + '" z1="' + str(z1) + '" x2="' + str(x2) + '" y2="' + str(y2) + '" z2="' + str(z2) + '" type="' + blocktype + '"/>'


def getMissionXML(distance):
    """Build the XML string"""

    missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <About>
                    <Summary>NLP Simulation</Summary>
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
                        <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1"/>
                        <!--<DefaultWorldGenerator forceReset="true"/>-->
                        <DrawingDecorator>

                            <DrawEntity x="3" y="227.0" z="5" type="Pig"/>
                            <DrawEntity x="0.5" y="230.0" z="0.5" type="Chicken"/>
                            <DrawEntity x="15" y="230.0" z="0.5" type="Pig"/>
                            <DrawEntity x="3" y="190.0" z="0.5" type="Pig"/>
                            <DrawEntity x="-10" y="227.0" z="0.5" type="Pig"/>
                        </DrawingDecorator>
                        <ServerQuitFromTimeUp timeLimitMs="300000"/>
                        <ServerQuitWhenAnyAgentFinishes/>
                    </ServerHandlers>
                </ServerSection>

                <AgentSection mode="Survival">
                    <Name>Recorder Agent</Name>
                    <AgentStart>
                        <Placement x="0.5" y="227.0" z="0.5" />
                    </AgentStart>
                    <AgentHandlers>
                        <AbsoluteMovementCommands/>
                        <ObservationFromFullStats/>
                        <ObservationFromRay/>
                        <ObservationFromGrid>
                            <Grid name="floor''' + str(distance) + '''x''' + str(distance) + '''">
                                <min x="-1" y="-1" z="-1"/>
                                <max x="1" y="-1" z="1"/>
                            </Grid>
                        </ObservationFromGrid>
                        <ObservationFromNearbyEntities>
                            <Range name="entities" xrange="40" yrange="40" zrange="40"/>
                        </ObservationFromNearbyEntities>


                        <ContinuousMovementCommands turnSpeedDegs="180"/>
                    </AgentHandlers>
                </AgentSection>
            </Mission>'''
    return missionXML



def findEntities(agent_host, world_state):
    """Builds the grid and labels the area to paint a picture for the agent"""
    entities = {}
    while True:
        # if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        observations = json.loads(msg)
        # print("OBSERVATIONS: ", observations)
        if 'entities' in observations:
            for block in observations['entities']:
                # print("BLOCK: ", block)
                name = block['name']
                # print("NAME: ", name)
                entities[name] = (block['yaw'], block['x'], block['z'])
            return entities
        else:
            print("ERROR: Could not find 'entities' in observations.")
            entities['Recorder Agent'] = (observations['Yaw'], observations['XPos'], observations['ZPos'])
            return entities

def findLineOfSight(agent_host, world_state):
    entities = {}
    while True:
        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            print(msg)
            observations = json.loads(msg)
            # print("OBSERVATIONS: ", observations)
            if "LineOfSight" in observations:
                for block in observations['LineOfSight']:
                    # print("BLOCK: ", block)
                    name = block['name']
                    # print("NAME: ", name)
                    entities[name] = (block['yaw'], block['x'], block['z'])
                return entities
            else:
                print("No objects in the line of sight currently.")
                return entities

def buildGrid(agent_host):
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        observations = json.loads(msg)
        grid = observations.get(u'floor9x9', 0)
        # if jumping and grid[4]!=u'lava':
        #     agent_host.sendCommand("jump 0")
        #     jumping = False
        # if grid[3]==u'lava':
        #     agent_host.sendCommand("jump 1")
        #     jumping = True
        # print("grid",grid)
        return grid


def getDistanceToObject(agent_host, world_state, getItem):
    surroundingArea = findEntities(agent_host, world_state)
    # objectLocation = findLineOfSight(agent_host, world_state)
    # print(objectLocation)
    # print("OBJECT:",objectLocation)
    myYaw, myX, myZ = surroundingArea["Recorder Agent"]
    if getItem in surroundingArea:
        goYaw, goX, goZ = surroundingArea[getItem]
    else:
        return 100
    distanceToEntity = math.sqrt((myX - goX)**2 + (myYaw - goYaw)**2)
    return distanceToEntity


def goToLocation(agent_host, world_state, getItem):
    """Goes to a location based on where the object is.
        Build a grid, find the object, record the location of both"""
    print("LOCATIONNNNNNNNNNNNNNNNNN")
    surroundingArea = findEntities(agent_host, world_state)
    # objectLocation = findEntities(agent_host, world_state)
    print(surroundingArea)
    # print("OBJECT:",objectLocation)
    myYaw, myX, myZ = surroundingArea["Recorder Agent"]
    if getItem in surroundingArea:
        goYaw, goX, goZ = surroundingArea[getItem]
    else:
        print("ERROR: Object cannot be found.")
        return "turn 0"
    # print("MYDISTANCE:",myYaw, myX, myZ)
    # print("PIGDISTANCE:",goYaw, goX, goZ)
    distanceToEntity = math.sqrt((myX - goX)**2 + (myYaw - goYaw)**2)
    # print(distanceToEntity)

    '''OTHER IDEA: if the agent hasn't changed position for a short time, jump, because
        it must be running into something'''
    if distanceToEntity > 1:
        difference = goYaw - myYaw;
        while difference < -180:
            difference += 360;
        while difference > 180:
            difference -= 360;
        difference /= 180.0;
        # print(difference)
        return ("turn " + str(difference))
    # getMissionXML(distanceToEntity)
    else:
        return ("move 0")


def getBestAngle(entities, current_yaw, current_health):
    '''Scan through 360 degrees, looking for the best direction in which to take the next step.'''
    us = findUs(entities)
    scores=[]
    # Normalise current yaw:
    while current_yaw < 0:
        current_yaw += 360
    while current_yaw > 360:
        current_yaw -= 360

    # Look for best option
    for i in xrange(agent_search_resolution):
        # Calculate cost of turning:
        ang = 2 * math.pi * (i / float(agent_search_resolution))
        yaw = i * 360.0 / float(agent_search_resolution)
        yawdist = min(abs(yaw-current_yaw), 360-abs(yaw-current_yaw))
        turncost = agent_turn_weight * yawdist
        score = turncost

        # Calculate entity proximity cost for new (x,z):
        x = us.x + agent_stepsize - math.sin(ang)
        z = us.z + agent_stepsize * math.cos(ang)
        for ent in entities:
            dist = (ent.x - x)*(ent.x - x) + (ent.z - z)*(ent.z - z)
            if (dist == 0):
                continue
            weight = 0.0
            if ent.name == MOB_TYPE:
                weight = agent_mob_weight
                dist -= 1   # assume mobs are moving towards us
                if dist <= 0:
                    dist = 0.1
            elif ent.name == GOAL_TYPE:
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




# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print 'ERROR:',e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)

# my_mission = MalmoPython.MissionSpec()
my_mission = MalmoPython.MissionSpec(getMissionXML(9), True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print "Error starting mission:",e
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
        print "Error:",error.text

print
print "Mission running ",

texts = ['attack', 'jump',
        'move forward', 'move back', 'turn left', 'turn right',
        'attack and move forward', ]

ith = 0
##test
# agent_host.sendCommand("move 1")
count = 1
# Loop until mission ends:
while world_state.is_mission_running:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:",error.text


    ###########Howard's CODE#############
    # buildGrid(agent_host)
    # if getDistanceToObject(agent_host, world_state, "Pig") > 1:
    #
    #     turn = goToLocation(agent_host, world_state, "Pig")
    #     print("TURN:",turn)
    #     agent_host.sendCommand(str(turn))
    # else:
    #     agent_host.sendCommand("move 0")
    getItem = "Pig"
    stop = False
    if world_state.number_of_observations_since_last_state > 0:
        if not stop:
            agent_host.sendCommand("move 1")
        msg = world_state.observations[-1].text
        ob = json.loads(msg)

        entities = {}
        if "Yaw" in ob:
            myYaw = ob[u'Yaw']
        if "entities" in ob:

            # entities = [EntityInfo(**k) for k in ob["entities"]]
            for block in ob['entities']:
                # print("BLOCK: ", block)
                name = block['name']
                # print("NAME: ", name)
                entities[name] = (block['yaw'], block['x'], block['z'])
            # print(entities)
            # goYaw = getBestAngle(entities, myYaw, 100)
            myYaw, myX, myZ = entities["Recorder Agent"]
            if getItem in entities:
                print("HERE:",getItem)
                goYaw, goX, goZ = entities[getItem]
            else:
                print("RESETTING VARIABLES")
                goYaw, goX, goZ = myYaw, myX, myZ
            difference = goYaw - myYaw;
            print("HAHA",difference)
            while difference < -180:
                difference += 360;
            while difference > 180:
                difference -= 360;
            difference /= 180.0;
            print("DIFFERENCE:",difference)
            agent_host.sendCommand("turn " + str(difference))
            distanceToEntity = math.sqrt((myX - goX)**2 + (myYaw - goYaw)**2)
            print("DISTANCE:",distanceToEntity)
            if distanceToEntity < 1.5:
                print("STOPPING")
                agent_host.sendCommand("turn 0")
                agent_host.sendCommand("move 0")
                stop = True


    if count == 100:
        break
    print(count)
    count += 1

    # if findEntities(agent_host, world_state, "Pig"):




    ###end####

    # if ith == len(texts):
    #     ith = 0
    # # ri = random.randint(0,len(texts)-1)
    # # text = texts[ri]
    # text = texts[ith]
    # # text = command.listen()
    # if text:
    #     com = command.manageCommand(text)
    #     if com:
    #         time.sleep(.3)
    #         agent_host.sendCommand(com)
    #         time.sleep(.3)
    # time.sleep(5)
    # if com:
    #     stopCom = command.stopCurrentCommand(com)
    #     if stopCom:
    #         agent_host.sendCommand(stopCom)
    # print('')
    # ith = ith + 1

print
print "Mission ended"
# Mission has ended.
