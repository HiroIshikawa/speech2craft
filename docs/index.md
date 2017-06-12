---
layout: default
title:  Speech2craft
---

# Speech2craft

[![Description of the Video](https://user-images.githubusercontent.com/1572847/27010256-e233485c-4e54-11e7-969c-1a653d067ac1.png)](https://youtu.be/jMOXL3SkKSw)

## A Smart Speech Interface for Minecraft

Speech2craft is a smart speech interface that allows users to play and explore the amazing world of Minecraft without having to touch a keyboard or controller. Not only it supports simple movements such as move, turn, attack, jump, pitch but also complex movements like equipping a specific tool and tracking a target entitiy. Do you want to dig the ground fast? Say "use diamondpickaxe and dig"! Do you want to chase the pig? Say "go to pig"! Speech2craft integrates technical key components. Speech recognizer converts the user's speech into text. Text parser restructure the text to a pattern and match that with Minecraft commands. Command handler allows the anget in the Minecraft to take actual actions. Let's speech and craft!

Library/API Used:
- Speech Recognition: [SpeechRecognition](https://pypi.python.org/pypi/SpeechRecognition/)/[Google Speech API](https://cloud.google.com/speech/)
- Text Paser: [spaCy](https://spacy.io/)
- Command Handler: [Project Malmo](https://www.microsoft.com/en-us/research/project/project-malmo/)

[Source Code][refCode] / [Detailed Doc][refDoc] / [Pictures][refPictures]

[refCode]: https://github.com/HiroIshikawa/speech2craft/tree/master/experiment/all
[refDoc]: https://github.com/HiroIshikawa/speech2craft/tree/master/docs/final.md
[refPictures]: https://github.com/HiroIshikawa/speech2craft/tree/master/docs/imgs
