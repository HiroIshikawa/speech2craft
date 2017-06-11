---
layout: default
title:  Speech2craft
---

# Speech2craft - A Smart Speech Interface for Minecraft -

[![Description of the Video](https://user-images.githubusercontent.com/1572847/27010256-e233485c-4e54-11e7-969c-1a653d067ac1.png)](https://www.youtube.com/embed/tdBFFRMu1i0)

Speech2craft is a smart speech interface that enables users to fully play and explore the amazing Minecraft world without having to touch a keyboard or controller. Not only it supports simple movements such as move, turn, attack, jump, pitch but also complex movements like equipping a specific tool and tracking a target entitiy. If you say "go to pig", it goes to the closest pig if exist. Speech2craft integrates technical key components: speech recognizer, text parser, and command handler. The speech recognizer is implemented by the combination of the python script and library, SpeechRecognition, and Google Speech API. The text parser enables is implemented using spaCy, the modern NLP library/API. The command handler is implemented by using useful function build upon the [Project Malmo](https://www.microsoft.com/en-us/research/project/project-malmo/), AI training platform on Minecraft.

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