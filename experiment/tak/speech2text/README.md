# Speech2Craft Draft 1:

## Progres
5/21: implemented the draft for the pipeline (speech to action in running Malmo environment)

## Scripts
- process.py: set up neccesarry Malmo environment, trigger listner and command builder
- command.py: listen user to make a test, analyse text to match with registered command list, return Malmo compatible command string 

## Dependencies
- [speech recognition](https://pypi.python.org/pypi/SpeechRecognition/)
- [spacy](https://spacy.io/docs/usage/)

## Note
- Implemented in python2.7

## Insturuction
0.a. install spacy,'pip install spacy', if not yet
0.b. install speech recognition, satisfy all requirements and pip install it, if not yet
0.c. download spacy english model, 'python -m spacy download en', if noy yet
1. put 'process.py' and 'command.py' in /Python_Examples folder
2. start Minecraft, './launchClinet.sh' in the /Minecraft folder in Malmo package
3. run '$ python process.py' in /Python_Examples folder
4. wait to see the prompt 'Say something!', and actually say something to the microphone (you should see the registered malmo compatible commands displayed when you run it)
5. if any match found, the agent should take that action
6. it repeats listen -> action -> listen -> action..

## References
- [Malmo platform tutorial](https://github.com/Microsoft/malmo/blob/master/Malmo/samples/Python_examples/Tutorial.pdf)
- [spacy: Token](https://spacy.io/docs/api/token)
- [What do spaCy's part-of-speech and dependency tags mean?](http://stackoverflow.com/questions/40288323/what-do-spacys-part-of-speech-and-dependency-tags-mean)
- [How to get the dependency tree with spaCy?](http://stackoverflow.com/questions/36610179/how-to-get-the-dependency-tree-with-spacy)
- [spacy: Rule based matching](https://spacy.io/docs/usage/rule-based-matching)
- [spacy: Using word vectors and semantic similarities](https://spacy.io/docs/usage/word-vectors-similarities)