---
layout: default
title:  Final Report
---

## Video

[![Description of the Video](https://user-images.githubusercontent.com/1572847/27010256-e233485c-4e54-11e7-969c-1a653d067ac1.png)](https://youtu.be/Xud8ZZL7Dsc)


## Project Summary


The main goal of this project is to implement an application that enables users to play Minecraft with speech input. We call the entire process as a pipeline: from the initial speech inputs to the actual actions taken by an agent in the Malmo environment. The pipeline consists of speech recognition, text parser, and command handler. The speech recognition aims at more accurate and faster results. The text parser has the parser be more flexible to complex sentences and more robust to a variety of inputs. Finally, for the command handler, given the command set provided by the parser result, aims at smoothly conducting sequences of actions that the user intended to do.
 
Implementing the fully functional pipeline for speech inputs is important since it may be applicable for other speech related applications. Beyond the Malmo environment, it can be extended to other game playing platforms. This enables users who have trouble interacting with games with traditional hardware based controllers to have the same game-playing or field operation experience as others. Malmo is a suitable environment to implement and test prototypes of the speech2craft pipeline. Once we could build a prototype, we can apply the knowledge and techniques used to other gaming environments. In addition, the potential for this application would be to eventually allow games to fully integrate speech as part of the gameplay experience, allowing players to simultaneously use a controller and voice input to play the game. 
 
Each part of the process, speech recognition, the text parser, and the command handler, requires AI/ML algorithms. The better speech recognition can be realized through learning multiple audio data to construct its model. The text parser is the part of traditional problem under the category of natural language processing. It can be improved through tailed parameter tuning and training given text inputs. The smart movements such as chasing a target in Malmo needs the agent to observe the environment and react accordingly with the appropriate AI algorithms given a model to follow. Incorporating the AI/ML technologies to its process, it can accomplish full speech input support from start to end of any game that the user wants to play. 


 
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
            print("Google Speech Recognition thinks you said "
                + r.recognize_google(audio))
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print("Could not request results from Google Speech 
                 Recognition service; {0}".format(e))
            return None
```
 
### Text Parser
 
 
![alt text](https://user-images.githubusercontent.com/1572847/27118173-ea536742-508e-11e7-99d5-d07c79543d93.png)

 
We chose spaCy as a primary library for text parsing. spaCy includes pre-trained NLP models and handy functions to handle different NLP related tasks. The advantage of using spaCy over the other NLP related libraries such as NLTK is its speed, cutting-edge algorithms, and support for modern ML applications. At this stage, the input is the text recognized by the speech recognizer. The parsing step follows basically find the root word, examine the children of the root, find a match that with predefined text patterns. If a pattern match found, it process the patterns to legal Malmo command.
 
Based on the continuous movements in Malmo, we support all the simple movements such as move, jump, attack, look, pitch etc.. In addition to that, for it enables user to play Minecraft more intuitively, we are adding several set of actions called smart movements which is triggered by a specific parsing pattern. For the current version, by the command “go to <target>” pattern, the agent initiate tracking the closest target entity in the environment. Smart movements’ implementation will be explained in more detail in the next section.
 
When we find the root and analyse the dependency, spaCy provides us with Part-of-Speech (POS) tagging and dependency tree construction. After taking the input text as an instance for text parsing, it comes with rich information associated with each word syntactically and semantically.  It is accomplished by the pre-trained English model built upon the spaCy library. POS tagging can find a word that is a root of the dependency tree of the sentence. Since our command is based on the verb initially, it confirm whether the root is verb or not. Then following process will look at the children of the root based on the syntactical dependency.
“Go to the pig” and "Use diamond pickaxe and dig": visualization of dependency tree using [displaCy](https://demos.explosion.ai/displacy/)
 
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
       'forward': 'move 1', 'back': 'move -1', 'backwards': 'move -1', 'right': 'strafe 1', 'left': 'strafe -1',
       'north': 'movenorth 1', 'south': 'movesouth 1', 'east': 'moveeast 1', 'west': 'movewest 1',
       'to': LIST OF ENTITIES/OBJECTS IN MINECRAFT
   },
   'jump': {
       '': 'jump 1', 'up': 'jump 1', 'stop': ['jump 0'], 'forward': 'jumpmove 1', 'back': 'jumpmove -1',
       'backwards': 'jumpmove -1', 'right': 'jumpstrafe 1', 'left': 'jumpstrafe -1',
       'north': 'jumpnorth 1', 'south': 'jumpsouth 1', 'east': 'jumpeast 1', 'west': 'jumpwest 1'
   },
   'strafe': {'right': 'strafe 1', 'left': 'strafe -1', 'stop': ['strafe 0']},
   'look': {'up': 'look -1', 'down': 'look 1'},
   'pitch': {'up': 'pitch -1', 'down': 'pitch 1', 'stop': ['pitch 0']},
   'turn': {'right': 'turn 1', 'left': 'turn -1', 'stop': ['turn 0', 'pitch 0'],
            'up': 'pitch -1', 'down': 'pitch 1'},
   'crouch': {'': 'crouch 1', 'stop': ['crouch 0']},
   'attack': {'': 'attack 1', 'stop': ['attack 0']},
   'use': {},
   'stop': ['move 0', 'jump 0', 'turn 0', 'strafe 0', 'pitch 0', 'crouch 0', 'attack 0'],
   'get': {'': LIST OF ENTITIES/OBJECTS IN MINECRAFT},
   'discard': {'': 'discardCurrentItem'},
   'quit': {'': 'quit'}
}
```
 
The version of code including the process of filtering the patterns with command map is defined like below:

```python
def parseVerb_( self, verb ):
    # check if given verb is a valid command
    if verb.lemma_ not in self.command_map:
        self.agent.sendCommand("chat Invalid Command")
    else:
        rights = [child for child in verb.rights]
        if rights:
            if rights[0].pos == CCONJ:
                self.doBasicCommand_(verb)

            options = self.command_map.get(verb.lemma_)
            for r_child in rights:
                # check if option is valid with given command
                if r_child.pos == ADV or r_child.pos == PART:  
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
                    # check if it's a quantitative movement 
                    # i.e. 1 block forward or forward 1 block
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
 
 
### Word Vector Similarity
We implemented word vector similarity scoring in order to expand the range of commands that a user could input into our system. Using pretrained word embeddings loaded through Genism's modeling toolkit, we were able to incorporate commands beyond the predefined set defined by Malmo.

First, we loaded in a word2vec pretrained vector trained on a portion of Google News dataset. 
```python
model = KeyedVectors.load_word2vec_format('word_embeddings/GoogleNews-vectors-negative300.bin', binary=True)
```

However, loading times were very slow, as the word vector file was 3.5 gigabytes. We decided to save the model ourselves through Genism in order to speed up loading times.
```python
model.init_sims(replace=True)
model.save('word_embeddings/GoogleNews)

# Now in other places that use the word vector, we simply load the model we saved above
self.word2vec = KeyedVectors.load('word_embeddings/GoogleNews', mmap='r')
```

Consequently, we began to parse verbs differently. We first checked if the verb we were parsing was already a pre-defined Malmo command. If it was, no word similarity analysis was required. If it was not, we searched through all possible Malmo commands, and matched the verb to the pre-defined command that had the highest similarity score. However, if the highest similarity score was below a certain threshold, we would consider the command invalid entirely.  
```python
for command in malmo_commands:
    score = word2vec.similarity(verb, command)

if highest word similarity score > threshhold:
    return command with the highest score
```

This allows the user to speak less restricted command phrases to Malmo. Instead of 'move forward', a user can say 'walk/run/go/ forward'. 'hit' and 'dig' both refer to Malmo's 'attack' command. If a user prefers to describe the bending motion of knees as 'squat' rather than 'crouch', they now have the freedom to do so.

We followed the same process when selecting inventory/hotbar items. If the user wished to use an item ('use item'), then their spoken item choice would be matched to all the items in the hotbar slots. If no hotbar items matched exactly, word similarity scoring was used to select the best match. This is clearly demonstrated within our project demo video above.
 
 
### Command Handler


 
![alt text](https://user-images.githubusercontent.com/1572847/27010014-352be00a-4e50-11e7-9db0-4a554630838d.png)
 
Command handler supports complex tasks that a user might intend to operate in Minecraft. This may cover the tasks where agent need to react the change of environment. Simple example, which is currently supported in our model, is “go to <target>”, which enable agent to get close enough to the target entity. This requires the agent to know the location of the target, if moving continuously. 
 
The key components for building the command handler are the observation models and adaptive movement algorithms. To observe the change of states, we use the Malmo’s ObservationFromNearByEntities as well as ObservationFromGrid. Using these observations, we can visualize the surrounding environment of the agent and perform the necessary actions. To control the complex movement of the agent, we use Malmo’s ContinuoutMovementCommands. We also use the AbsoluteMovementCommands and DiscreteMovementCommands for supporting wider variety of commands. For the implementation of the “go to <target>” smart movement, we only use the ContinuousMovementCommands. This "go to <target>" command uses AI algorithms to not only go to the target, but it will follow the target until told otherwise, as well as avoid minor obstacles that might be in the way of the target, such as jumping over multiple blocks, or going around an obstruction.
 
Including ObservationFromNearByEntities, the world state contains the information about entities around the agent. Using this information, we find the closest target entity that matches its name with the target contained in the output of text parser (i.e. “pig”). As soon as it gets the command request for the “go to <target>” pattern, it initiates a move forward command with continuous movement. The rest of the controls are made by finding the best angle towards the target entity. To compute this angle, we find the location of the pig in two-dimensional space and the angle that the agent is facing, then make the necessary calculations to continously turn the agent towards the location of the pig. In addition, we use mostly the same method for picking up items as well, using a command such as "pick up the <item>".

For avoiding walls and jumping over blocks, we take advantage of the three-dimensional grid created by ObservationFromGrid. At each world_state change, we check the surrounding block grid and see if there are blocks in the way of the agent's path. If there is and the agent can jump over the block, the agent will perform the necessary jump. If the obstacle turns out to be a wall, if the agent was not told to stop at a wall, the agent will attempt to go around the wall to continue going to the goal object.

 
## Evaluation


In each components of the pipeline of speech2craft, there’s several approaches to accomplish goals and these have different advantages and disadvantages. As we introduced in the project summary, three components of pipeline are speech recognition, text parser, and command handler. Entirely, the major goal of this application is to serve a greater quality of the speech based play of Minecraft leveraging the power of AI/ML. Aiming at accomplish the main goal, we will go over some variation of approaches for each component below 


### Speech Recognition
As it stands, speech recognition takes user’s voice input and convert that to text. The problem we tend to face is the inaccuracy of its recognition. The more complex the speech inputs, it gets harder to be recognized accordingly. The other factor would be the duration that the speech recognition finish the process. The relation between the accuracy and duration is trade-off. Usually, the more accuracy you aim at, the more duration you need to process. 
 
Since the quality of this application weigh more onto the text parser part, we have not conducted intensive evaluation for this part. But, from the preliminary research, we could know that the most promising results can be attained by using Google Speech Recognition API under the assumption that user has an internet connection. 
 
### Text Parser
 
#### Complexity Coverage
The baseline of the problem that converts the text to command would be looking up the total combination between each word given and the registered commands. This implementation does not have any problem to interpret simple syntax such as “attack”, or “move forward”. But it would start having issues to process more complex syntax such as “go to pig and attack cow”. As syntactic complexity grows, the complexity of parsing algorithms increases. Leveraging POS tagging and dependency makes the parsing algorithms much simple and scalable even the complexity of the sentence given increases.
 
#### Matching Efficiency
The base lines for the text parser should be the naive word based matching over the sentence given. For example, given “go to the <target>” text, the simple parser can traverse all the available commands and options for each word. Though the each input, text size, is small for this application, this method is very limited for scalability. If we assume the number of commands and its option in total as M, and the number of words given N, then the cost of the matching method above is O(M*N). Though the words given is relatively small, if we want to allow users to controls agent with more complex syntax and support more commands and its combination, this limitation is not insignificant. 
 
 
![alt text](https://user-images.githubusercontent.com/1572847/27010024-57d3be34-4e50-11e7-9358-af9428d58eb5.png)
 
Our method using the POS tagging and dependency makes the program more efficient and more scalable. The model can find the root word for searching over M words, then from there, it traverse the children of the root word to match any pattern pre-registered. Each level of the tree have corresponding search space in the command map and each search space is much smaller than the total N commands. For example, for “Move forward” command, the corresponding pattern is <verb + adj>. POS tagging and dependency given, the search space get reduced to the corresponding command header’s such as verb and adverb. The number of registered verbs, V, and adverbs, A, each are much smaller than the total number of commands N. WIth that, the time cost is O(V+A).
 
 
![alt text](https://user-images.githubusercontent.com/1572847/27010029-60173f12-4e50-11e7-82ad-8e333edfcf73.png)
 

### Word Vector Similarity
Although word similarity scoring allowed us to expand the set of possible user-spoken commands, it did not come without difficulties. For example, certain words did not match to the proper Malmo commmand. We mitigated this problem by adding a dictionary of synonyms for malmo commands that are clearly correlated, but did not match based on the pretrained word embedding. We matched the the word to the command if it was found in its list of synonyms.

```
go , crouch ==> 0.123674354369
**go , get ==> 0.589803159155**
**go , move ==> 0.494788483089**
go , stop ==> 0.288347203098
go , jump ==> 0.317825451313
go , pitch ==> 0.221837512198
go , quit ==> 0.271149826715
go , use ==> 0.25773402461
go , look ==> 0.407729331961
go , turn ==> 0.429415481639
go , attack ==> 0.0487696218339
go , strafe ==> 0.144138647322
go , discard ==> 0.213456853048
```

```python
self.synonyms = {
    'move': set(['go', 'walk']),
    'attack': set(['hit', 'dig']),
    'use': set(['hold']),
    'discard': set(['drop', 'throw']),
```



### Command Handler
 
#### Usability
The baseline implementation of this section would be the simple movement options, such as “move forward”, “turn left/right”, "got to", etc. The smart movements that are a combination of several commands and responsive to the changes of environment through observations solves the problem that users may encounter when only a simple command set is available. For example, chasing a specific target is hard if you do not have the smart movement command “go to <target>” pattern. The user needs to keep sending movement commands accordingly while monitoring a potentially moving target. The smart movements, which are going around walls, stopping at walls, and jumping over obstacles, work 99 percent of the time from the controlled tests that we have performed with these movements. From a visual standpoint, the agent will twitch a little when turning or jumping, but it moves decently and will traverse in relatively the same time as if a real person were making those movements.
 

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
- [sense2vec with spaCy](https://explosion.ai/blog/sense2vec-with-spacy)

#### Word Similarity
- [genism](https://radimrehurek.com/gensim/)
- [Word similarity vectors (word2vec)](https://radimrehurek.com/gensim/models/word2vec.html)
- [KeyedVectors](https://radimrehurek.com/gensim/models/keyedvectors.html)
- [List of pretrained word embeddings](http://ahogrammer.com/2017/01/20/the-list-of-pretrained-word-embeddings/)
- [Google News word2vec](https://code.google.com/archive/p/word2vec/)
 
#### Command Handler
- [Malmo Class References](https://microsoft.github.io/malmo/0.14.0/Documentation/classmalmo_1_1_mission_spec.html)
- [Malmo XML Schema Documentation](https://microsoft.github.io/malmo/0.21.0/Schemas/MissionHandlers.html)
- [Malmo - MissionHandlers.xsd](https://github.com/Microsoft/malmo/blob/master/Schemas/MissionHandlers.xsd)
- [Malmo/samples/Python Examples/mob_fun.py](https://github.com/Microsoft/malmo/blob/master/Malmo/samples/Python_examples/mob_fun.py)
