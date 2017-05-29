---
layout: default
title:  Speech2craft
---

# Speech2craft
<img src="https://github.com/HiroIshikawa/speech2craft/blob/master/docs/imgs/professor_slide_NLP.PNG" width="500">

[Slide from Professor Sameer Singh's lecture](http://sameersingh.org/courses/aiproj/sp17/slides/lecture-0406-projs-and-intro-rl.pdf "Slide 22")

### Objective
Our objective is to implement a speech-to-command feature for Minecraft that will allow the user to use verbal commands to take control of the agent's actions. The purpose of this project is to allow the user to be able to play the game without having to touch a keyboard or controller.


### Techniques
Our project uses speech recognition (Python packages), natural language processing (Spacy), and the Microsoft Malmo platform in order to accomplish our objective.


### Functionality
Our project can currently perform the following commands (and those similar):
- go (move) forward
- turn (go) left
- turn (go) right
- go backwards
- jump
- attack
- go to the pig
- character will automatically jump if encountering an obstacle


### Links:
- [Status Report][refStatus]
- [Code][refCode]
- [Pictures][refPictures]
- [Malmo][refMalmo]
- [spaCy NLP library][refSpaCy]
- [Python Google Speech API Tutorial][refGoogleSpeech]


[refCode]: https://github.com/HiroIshikawa/speech2craft/tree/master/experiment/all
[refPictures]: https://github.com/HiroIshikawa/speech2craft/tree/master/docs/imgs
[refMalmo]: https://github.com/Microsoft/malmo
[refStatus]: https://github.com/HiroIshikawa/speech2craft/tree/master/docs/status.md
[refSpaCy]: https://spacy.io/
[refGoogleSpeech]: https://pythonspot.com/en/speech-recognition-using-google-speech-api/
