import sys
import os
import time
import random

import spacy
import speech_recognition as sr

class DependencyPattern:
    """A root and its dependecy for matching
    Attrs:
        root   (str): the root of dependency, verb
        advmod (str): adverbial modifier
        dobj   (str): direct object
        iobj   (str): indirect object
    """
    def __init__(self):
        """Initialize root dependency
        """
        self.root = ''
        self.advmod = ''
        self.dobj = ''
        self.iobj = ''

    def set_root(self, root):
        """set root"""
        self.root = root

    def set_advmod(self, advmod):
        """set adverbial modifier"""
        self.advmod = advmod

    def set_dobj(self, dobj):
        """set direct object"""
        self.dobj = dobj

    def set_iobj(self, iobj):
        """set indirect object"""
        self.iobj = iobj

    def display(self):
        """display this dependency pattern"""
        print('{} {} {} {}').format(self.root, self.advmod, self.dobj, self.iobj)


class Command:
    """Legal command for Malmo API
    Attrs:
        action (str): action instance of this command (turn, attack etc..)
        adjustment (str): attricute name of teh action (left, eirght etc..)
        adjustzmentVaue (double): corresponding value for malmo command (1, -1 etc..)
        malmoCommand (str): Malmo compatible command
    """
    def __init__(self, action, adjustment, adjustmentValue):
        """Initialize command
        Args:
            action (str): action instance of this command (turn, attack etc..)
            adjustment (str): attricute name of teh action (left, eirght etc..)
            adjustzmentVaue (double): corresponding value for malmo command (1, -1 etc..)
        """
        self.action = action
        self.adjustment = adjustment
        self.adjustmentValue = adjustmentValue
        self.malmoCommand = self.action + ' ' + str(self.adjustmentValue)

    def display(self):
        """Dispaly command properties"""
        print('action: {:<7}').format(self.action),
        print('attr: {:<7}').format(self.adjustment),
        print('val: {:<3}').format(self.adjustmentValue)
        

class CommandSet:
    """Set of commands for Malmo API
    Attrs:
        commands (list<obj>): 
    """
    def __init__(self, comMap):
        """Initialize the set of commands"""
        self.commands = []
        for action, adjustments in comMap.iteritems():
            for adjustment, adjustmentValue in adjustments.iteritems():
                command = Command(action, adjustment, adjustmentValue)
                self.commands.append(command)

    def display(self):
        """Display the command set"""
        print(' ------ Registered Command List ------ ')
        for ith, com in enumerate(self.commands):
            print('{:<3}').format(str(ith)+'.'),
            com.display()
        print(' ------------------------------------- ')


def matching(depPattern, commandSet):
    """Match a dpendency pattern with any command instance in the command set
    Args:
        depPattern (obj): dependency pattern 
        commandSet (obj): command set
    Returns:
        match (str): formatted match result, ready to be sent to Malmo
    """
    match = None
    for command in commandSet.commands:
        # match the verb token with action
        if command.action == depPattern.root:
            # match the adverb token with adjustment
            if command.adjustment == depPattern.advmod:
                # generate Malmo compatible command
                match = command.malmoCommand
                break
    return match

def buildCommand(text):
    """Bulid a command by parsing text and match that with corresponding action
    Args:
        text (str): text given listner 
    Returns:
        command (str): malmo compatible command 
    """
    doc = nlp(text.decode("utf-8"))
    sentences = list(doc.sents)
    # identify verb token
    root_token = sentences[0].root
    st = root_token.lower_.decode("utf-8")
    depPattern = DependencyPattern()
    depPattern.set_root(st)
    # find tokesn depending on the verb identified
    for child in root_token.children:
        st = child.lower_.decode("utf-8")
        if child.dep_ == 'advmod':
            depPattern.set_advmod(st)
        if child.dep_ == 'dobj':
            depPattern.set_dobj(st)
        if child.dep_ == 'iobj':
            depPattern.set_iobj(st)
        # print(child.dep_)
    print('dependency pattern found: '),
    depPattern.display()
    # match the pattern and actionset
    command = matching(depPattern, commandSet)
    # return generated command
    if command:
        print('Sending malmo command: '),
        print(command)
    return command

def listen():
    """Listen and recognize user voice from a built-in microphone.
    Returns:
        text (str): recovgnized text with the recognizer
    """
    with sr.Microphone() as source:
        # r.adjust_for_ambient_noise(source)
        r.listen(source)
        print("Say something!")
        audio = r.listen(source)
        try:
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return None
        # text = 'Move forward'
        
# command map: modify this for registering malmo commands
commandMap = {'move':{'forward':1,'back':-1},  # 'go':['forward','back'],
                'strafe':{'left':1, 'right':-1}, 
                'pitch':{'up':1, 'down':-1}, # 'look':['up', 'down'],  
                'turn':{'left':1, 'right':-1}, 
                'jump':{'':1}, 
                'crouch':{'':1}, 
                'attack':{'':1}, 
                'use':{'':1}}

# construct command set using the command_map above
commandSet = CommandSet(commandMap)
# display registered commands
commandSet.display()
# initialize recognizer
r = sr.Recognizer()
# load spacy english model
nlp = spacy.load('en')