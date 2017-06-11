---
layout: default
title:  Final Report
---

## Video

[![Description of the Video](https://user-images.githubusercontent.com/1572847/27010256-e233485c-4e54-11e7-969c-1a653d067ac1.png)](https://www.youtube.com/embed/tdBFFRMu1i0)


## Project Summary


The main goal of this project is to implement an application that enables users to play Minecraft with speech input. We call the entire process from the initial speech inputs to the actual actions taken by an agent in Malmo environment pipeline. The pipeline is composed of the speech recognition, text parser, command handler. The speech recognition aims at more accurate and faster result. The text parser aims at having the parser be more flexible to complex sentence and robust to variant inputs. Finally, for the command handler, given the command set provided by the parser result, aims at conducting sequence of actions that the user intended to do smoothly.
 
Implementing the fully functional pipeline for speech inputs is important since it may be applicable for other speech related applications. Beyond the Malmo environment, it can be extended to other game playing platforms. This enables users who have trouble to interact with games by traditional hardware based controllers to have same game playing or field operation experience with others. Malmo is suitable environment to implement and test prototypes of speech2craft pipeline. Once we could build a prototype, we can apply the knowledge and techniques used to other gaming environment.
 
Each part of the process, speech recognition, text parser, and the command handler, requires AI/ML algorithms. The better speech recognition can be realized through learning multiple audio data to construct its model. The text parser is the part of traditional problem under the category of natural language processing. It can be improved through tailed parameter tuning and training given text inputs. The smart movements such as chasing a target in Malmo needs agent to observe the environment and react accordingly given a model to follow. Incorporating the AI/ML technologies to its process, it can accomplish full speech input support from start to end of any game that user want to play. 


 
## Approaches
 

The major components of speech2craft: 

![alt text](https://user-images.githubusercontent.com/1572847/27010005-1bd406dc-4e50-11e7-86b5-5fa687cef0a6.png)
 
For each components of the speech2craft pipeline, we have different approaches and these have advantages and disadvantages over each other. To implement speech recognizer, we used [SpeechRecognition](https://pypi.python.org/pypi/SpeechRecognition/) and [Google Speech API](https://cloud.google.com/speech/) through its implementation. Text parser leverages the [spaCy](https://spacy.io/) library to conduct several parsing tasks. For the command handler, to implement several sets of actions including simple one time continuous actions supported by Malmo command interface, we implemented a function to control the agent reacting the states of environment through observations. 
 
### Speech Recognition
 
 
![alt text](https://user-images.githubusercontent.com/1572847/27010010-291cb78a-4e50-11e7-8b8d-70df6b786438.png)
 
We chose SpeechRecognition library because it provides python support and simple interface to interact with several speech recognition APis. We chose Google Speech Recognition API for its choice of speech recognition API over sevenral other choices such as CMU Sphinx, Wit.ai, Microsoft Bing Voice Recognition, Houndfly API, IBM speech to text. Though CMU Sphinx provides offline support, since the accuracy was too low when tested, we eliminated that from our selection. From a preliminary research about speech recognition API’s accuracy and performance, we pick Google Speech Recognition considering no requirement of registering API credential for prototyping purpose as well.
 
The implementation of the function that take speech as input and give text as an output is below:
 
```python
import speech_recognition as sr
 
r = sr.Recognizer()
 
def listen():
    """Listen and recognize user voice from a built-in microphone.
    Returns:
        text (str): recovgnized text with the recognizer
    """
    with sr.Microphone() as source:
        r.listen(source)
        print("Speech your command: !")
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
```
 
### Text Parser
 
 
![alt text](https://user-images.githubusercontent.com/1572847/27010009-23622ae6-4e50-11e7-94bf-158d92c98772.png)
 
We chose spaCy as a primary library for text parsing. spaCy includes pre-trained NLP models and handy functions to handle different NLP related tasks. The advantage of using spaCy over the other NLP related libraries such as NLTK is its speed, cutting-edge algorithms, and support for modern ML applications. At this stage, the input is the text recognized by the speech recognizer. The parsing step follows basically find the root word, examine the children of the root, find a match that with predefined text patterns. If a pattern match found, it process the patterns to legal Malmo command.
 
Based on the continuous movements in Malmo, we support all the simple movements such as move, jump, attack, look, pitch etc.. In addition to that, for it enables user to play Minecraft more intuitively, we are adding several set of actions called smart movements which is triggered by a specific parsing pattern. For the current version, by the command “go to <target>” pattern, the agent initiate tracking the closest target entity in the environment. Smart movements’ implementation will be explained in more detail in the next section.
 
When we find the root and analyse the dependency, spaCy provides us with Part-of-Speech (POS) tagging and dependency tree construction. After taking the input text as an instance for text parsing, it comes with rich information associated with each word syntactically and semantically.  It is accomplished by the pre-trained English model built upon the spaCy library. POS tagging can find a word that is a root of the dependency tree of the sentence. Since our command is based on the verb initially, it confirm whether the root is verb or not. Then following process will look at the children of the root based on the syntactical dependency.
“Go to the pig”: visualization of dependency tree
 
![alt text](https://user-images.githubusercontent.com/1572847/27010018-490af4da-4e50-11e7-9de2-f61e326a5b06.png)
 
 
Let’s go over a simple example of parsing in python code:

```python
import spacy
 
nlp = spacy.load(‘en’)  # load spaCy English trained model
doc = nlp(text.decode(“utf-8”)  # apply model to the given text
 
for sent in doc.sents:
    root = sent.root
    r_children = [ child for child in root.rights]
    if r_children:
        for r_child in r_children:
            if r_child.pos == ADV or r_child.pos == PART:
                doAdvCommand(root, r_child)
            elif r_child.pos == NOUN:
                doObjCommand(root, r_child)
            elif r_child.pos == ADP:
                doPrepCommand(root, r_child)
            elif r_child.pos == VERB:
                 if root.lemman_ == ‘stop’:
                     doStopCommand(r_child) 
    else:
        doBasicCommand(root)
```
This code is just an example code to show how a simple parsing may work. Actual implementation of our code is different so please refer to the source code.
 
To map the result of the parse onto the legal Malmo command, we defined the command_map dictionary to compare the found pattern with it. 
 
```python
        self.command_map = {
            'move': {
                'stop': ['move 0', 'strafe 0'],
                'forward': 'move 1', 'back': 'move -1', 'right': 'strafe 1', 'left': 'strafe -1',
                'north': 'movenorth 1', 'south': 'movesouth 1', 'east': 'moveeast 1', 'west': 'movewest 1',
                'to': 'LIST OF ENTITIES/OBJECTS'
            },
            'jump': {
                '': 'jump 1', 'stop': ['jump 0'],
                'forward': 'jumpmove 1', 'back': 'jumpmove -1', 'right': 'jumpstrafe 1', 'left': 'jumpstrafe -1',
                'north': 'jumpnorth 1', 'south': 'jumpsouth 1', 'east': 'jumpeast 1', 'west': 'jumpwest 1' #'use': 'jumpuse'
            },
            'strafe': {'right': 'strafe 1', 'left': 'strafe -1', 'stop': ['strafe 0']},
            'look': {'up': 'look -1', 'down': 'look 1'},
            'pitch': {'up': 'pitch -1', 'down': 'pitch 1', 'stop': ['pitch 0']},
            'turn': {'right': 'turn 1', 'left': 'turn -1', 'stop': ['turn 0'], 'to': 'LIST OF ENTITIES/OBJECTS'},
            'crouch': {'': 'crouch 1', 'stop': ['crouch 0']},
            'attack': {'': 'attack 1', 'stop': ['attack 0']},
            'dig': {'': 'attack 1'},
            'use': 'INVENTORY LIST',
            'stop': ['move 0', 'jump 0', 'turn 0', 'strafe 0', 'pitch 0', 'crouch 0', 'attack 0'],
            'go': {'to': []}, #object and entity list?
            'pick': {'up': 'LIST OF ENTITIES/OBJECTS'}
        }
```
 
The version of code including the process of filtering the patterns with command map is defined like below:

```python
    def parseVerb_( self, verb ):
        if verb.lemma_ not in self.command_map:  # check if given verb is a valid command
            self.agent.sendCommand("chat Invalid Command")
        else:
            # rightVerbs = [child for child in verb.rights if child.pos == VERB and child.dep == conj]
            # rights = [child for child in verb.rights if child.pos != VERB]
            rights = [child for child in verb.rights]
            if rights:
                if rights[0].pos == CCONJ:
                    self.doBasicCommand_(verb)
 
                options = self.command_map.get(verb.lemma_)
                for r_child in rights:
                    if r_child.pos == ADV or r_child.pos == PART:  # check if option is valid with given command
                        # no parsing needed, just do command
                        # i.e. move | forward
                        if r_child.lemma_ in options:
                            if r_child.lemma == 'up':
                                # self.doObjCommand_(verb, r_child)
                                pass
                            else:
                                self.doAdvCommand_(verb, r_child)
                    elif r_child.pos == NOUN:
                        # parse for preposition and prepositional object
                        # i.e. choose | steel pickaxe (-> on -> the left)
                        # check if it's a quantitative movement i.e. 1 block forward or forward 1 block
                        if r_child.lemma_ == 'left' and r_child.lemma_ in options:
                            self.doAdvCommand_(verb, r_child)
                        else:
                            self.doObjCommand_(verb, r_child)
                    elif r_child.pos == ADP:
                        # parse for prepositional object
                        # i.e. go | to -> pobj
                        self.doPrepCommand_(verb, r_child)
                    elif r_child.pos == VERB:
                        # parse subsequent command
                        # choose steel pickaxe | (and) dig -> ...
                        if verb.lemma_ == 'stop':
                            if r_child.lemma_ in self.command_map:
                                self.doStopCommand_(r_child)
                        else:
                            self.parseVerb_(r_child)
            else:
                self.doBasicCommand_(verb)
```
As you may notice, in this snippet, it visits command map to filter out unregistered words as it go through parsing. There’s some of the limitation of the primary POS tagging provided by the spaCy trained model. For example, the left is recognized as a noun based on that while actual interpretation may be adverb in the context of Malmo play, i.e. “turn left”. This kind of limitation is naively mitigated by adding additional filter (i.e. if r_child.lemma_ == 'left'  in code) in our current version. 
 
Compared to other approach, which is building specialized trained model for the Malmo usages, using spaCy prebuild training model and mitigating some of the corner cases by additional filtering has advantages. You just do not need to build a model, hence you do not require any data and takes no time regarding training obviously. For the processing speed, considering the small text amount given at a time and small search space on command map, this simple pattern match mechanism works well in actual run.
 
### Command Handler


 
![alt text](https://user-images.githubusercontent.com/1572847/27010014-352be00a-4e50-11e7-9db0-4a554630838d.png)
 
Command handler supports complex task that a user might intend to operate in Minecraft. This may cover the tasks where agent need to react the change of environment. Simple example, which is currently supported in our model, is “go to <target>”, which enable agent to get close enough to the target entity. This requires the agent to know the location of the target, if moving continuously. 
 
The key components for building the command handler are the observation models and adaptive movement algorithms. To observe the change of states, we use the Malmo’s ObservationFromNearByEntities. To control the complex movement of the agent, we use the Malmo’s ContinuoutMovementCommands. We actually use the AbsoluteMovementCommands and DiscreteMovementCommands for supporting wider variety of commands. For the implementation of the “go to <target>” smart movement, we only use the ContinuousMovementCommands.
 
Including ObservationFromNearByEntities, the world state can contains the information about entities around agent. Using this information, we find the closest target entity that match its name with the target contained in the output of text parser (i.e. “pig”). As soon as it gets the command request for the “go to <target>” pattern, it initiates the move forward continuous movement. The rest of controls made by finding the best angle towards the target entity. 


 
## Evaluation


In each components of the pipeline of speech2craft, there’s several approaches to accomplish goals and these have different advantages and disadvantages. As we introduced in the project summary, three components of pipeline are speech recognition, text parser, and command handler. Entirely, the major goal of this application is to serve a greater quality of the speech based play of Minecraft leveraging the power of AI/ML. Aiming at accomplish the main goal, we will go over some variation of approaches for each component below 


### Speech Recognition
As it stands, speech recognition takes user’s voice input and convert that to text. The problem we tend to face is the inaccuracy of its recognition. The more complex the speech inputs, it gets harder to be recognized accordingly. The other factor would be the duration that the speech recognition finish the process. The relation between the accuracy and duration is trade-off. Usually, the more accuracy you aim at, the more duration you need to process. 
 
Since the quality of this application weigh more onto the text parser part, we have not conducted intensive evaluation for this part. But, from the preliminary research, we could know that the most promising result can be attained by using Google Speech Recognition API under the assumption that user has an internet connection. 
 
### Text Parser
 
#### Complexity Coverage
The baseline of the problem that converts the text to command would be looking up the total combination between each word given and the registered commands. This implementation does not have any problem to interpret simple syntax such as “attack”, or “move forward”. But it would start having issues to process more complex syntax such as “go to pig and attack cow”. As syntactic complexity grows, the complexity of parsing algorithms increases. Leveraging POS tagging and dependency makes the parsing algorithms much simple and scalable even the complexity of the sentence given increases.
 
#### Matching Efficiency
The base lines for the text parser should be the naive word based matching over the sentence given. For example, given “go to the <target>” text, the simple parser can traverse all the available commands and options for each word. Though the each input, text size, is small for this application, this method is very limited for scalability. If we assume the number of commands and its option in total as M, and the number of words given N, then the cost of the matching method above is O(M*N). Though the words given is relatively small, if we want to allow users to controls agent with more complex syntax and support more commands and its combination, this limitation is not insignificant. 
 
 
![alt text](https://user-images.githubusercontent.com/1572847/27010024-57d3be34-4e50-11e7-9358-af9428d58eb5.png)
 
Our method using the POS tagging and dependency makes the program more efficient and more scalable. The model can find the root word for searching over M words, then from there, it traverse the children of the root word to match any pattern pre-registered. Each level of the tree have corresponding search space in the command map and each search space is much smaller than the total N commands. For example, for “Move forward” command, the corresponding pattern is <verb + adj>. POS tagging and dependency given, the search space get reduced to the corresponding command header’s such as verb and adverb. The number of registered verbs, V, and adverbs, A, each are much smaller than the total number of commands N. WIth that, the time cost is O(V+A).
 
 
![alt text](https://user-images.githubusercontent.com/1572847/27010029-60173f12-4e50-11e7-82ad-8e333edfcf73.png)
 
 
### Command Handler
 
#### Usability
The baseline implementation of this section would be the simple movement options such sa “move forward”, “turn left/right” etc.. available.  The smart movements that is a combination of several commands and responsive to the changes of environment through observation solves the problem that users may encounter when only simple command set is available. For example, chasing a specific target is hard if you do not have the smart movement command “go to <target>” pattern. User needs to keep sending according movement commands while monitoring potentially movement target.
 

## References
 
#### Speech Recognition
- [SpeechRecognition](https://pypi.python.org/pypi/SpeechRecognition/)
- [Coding Jarvis in Python in 2016](https://ggulati.wordpress.com/2016/02/24/coding-jarvis-in-python-3-in-2016/)
- [What are the top ten speech recognition APIs?](https://www.quora.com/What-are-the-top-ten-speech-recognition-APIs)
- [Speech Recognition - A comparison of popular services in EN and NL](https://blog.craftworkz.co/speech-recognition-a-comparison-of-popular-services-in-en-and-nl-67a3e1b0cee6)
 
#### Text Parser
- [spaCy](https://spacy.io/)
- [install spaCy](https://spacy.io/docs/usage/)
- [Part-of-speech tagging](https://spacy.io/docs/usage/pos-tagging)
- [Using the dependency parse](https://spacy.io/docs/usage/dependency-parse)
- [Intro to NLP with spaCy](https://nicschrading.com/project/Intro-to-NLP-with-spaCy/)
 
#### Command Handler
- [Malmo Class References](https://microsoft.github.io/malmo/0.14.0/Documentation/classmalmo_1_1_mission_spec.html)
- [Malmo XML Schema Documentation](https://microsoft.github.io/malmo/0.21.0/Schemas/MissionHandlers.html)
- [Malmo - MissionHandlers.xsd](https://github.com/Microsoft/malmo/blob/master/Schemas/MissionHandlers.xsd)