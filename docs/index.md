---
layout: default
title:  Speech2craft
---

# Speech2craft

[![Description of the Video](https://user-images.githubusercontent.com/1572847/27010256-e233485c-4e54-11e7-969c-1a653d067ac1.png)](https://www.youtube.com/embed/tdBFFRMu1i0)

## A Smart Speech Interface for Minecraft

Speech2craft is a smart speech interface that allows users to play and explore the amazing world of Minecraft without having to touch a keyboard or controller. Not only it supports simple movements such as move, turn, attack, jump, pitch but also complex movements like equipping a specific tool and tracking a target entitiy. Do you want to dig the ground fast? Say "use diamondpickaxe and dig"! Do you want to chase the pig? Say "go to pig"! Speech2craft integrates technical key components. Speech recognizer converts the user's speech into text. Text parser restructure the text to a pattern and match that with Minecraft commands. Command handler allows the anget in the Minecraft to take actual actions. 

Library/API Used:
- Speech Recognition: [SpeechRecognition](https://pypi.python.org/pypi/SpeechRecognition/) / [Google Speech API](https://cloud.google.com/speech/)
- Text Paser: [spaCy](https://spacy.io/)(natural language processing library/API) 
- Command Handler: [Project Malmo](https://www.microsoft.com/en-us/research/project/project-malmo/)(AI training platform on Minecraft).

[Status Report][refStatus] / [Code][refCode] / [Pictures][refPictures]
[Malmo][refMalmo] / [spaCy NLP library][refSpaCy] / [Python Google Speech API Tutorial][refGoogleSpeech]

[refCode]: https://github.com/HiroIshikawa/speech2craft/tree/master/experiment/all
[refPictures]: https://github.com/HiroIshikawa/speech2craft/tree/master/docs/imgs
[refMalmo]: https://github.com/Microsoft/malmo
[refStatus]: https://github.com/HiroIshikawa/speech2craft/tree/master/docs/status.md
[refSpaCy]: https://spacy.io/
[refGoogleSpeech]: https://pythonspot.com/en/speech-recognition-using-google-speech-api/