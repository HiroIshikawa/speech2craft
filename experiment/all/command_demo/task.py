import time
import json
import math

from collections import namedtuple
EntityInfo = namedtuple('EntityInfo', 'x, y, z, yaw, pitch, name')
EntityInfo.__new__.__defaults__ = (0, 0, 0, 0, 0, "")
# AgentInfo = namedtuple('AgentInfo', 'XPos, YPos, ZPos, Yaw, Pitch, Name')
# AgentInfo.__new__.__defaults__ = (0, 0, 0, 0, 0, "")

# Task params:
ARENA_WIDTH = 60
ARENA_BREADTH = 60
GOAL_TYPE = "Pig"

# Agent params:
agent_stepsize = 1
agent_search_resolution = 30 # Smaller values make computation faster, which seems to offset any benefit from the higher resolution.
agent_goal_weight = 100
agent_edge_weight = -100
agent_mob_weight = -10
agent_turn_weight = 0 # Negative values to penalise turning, positive to encourage.

""" Task utilities 
"""
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
    ent = getClosestGoal(agent, entities)
    dist = abs(ag_x-ent[0])+abs(ag_z-ent[2])
    return dist


""" Run task
"""
def runGoto(agent_host):
    #sys.stdout.write(".")
    # while(1):
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
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

            # print('Best yaw: '),
            # print(best_yaw)
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

            # print('Distance to goal: '),
            # print(distance_to_goal)

            agent_host.sendCommand("turn " + str(difference))

def runStop(agent_host):
    agent_host.sendCommand("move 0")
    agent_host.sendCommand("turn 0")
    agent_host.sendCommand("strafe 0")
    agent_host.sendCommand("attack 0")
    agent_host.sendCommand("jump 0")