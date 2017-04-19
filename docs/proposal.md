---
layout: default
title: Proposal
---

### Summary of the Project

This project aims at implementing speech-to-command feature to allow user to take control on actions of an agent in a world of Minecraft. It will take a speech as initial input, convert that speech to text, analyze text to extract a legal action, and finally send a command for an agent to take that action as an output. Applications of this feature may include partial or fully speech based MInecraft playing.

### AI/ML Algorithms

Alexa/Google speech recognition API to take in user speech
NLTK, spaCy, Stanford CoreNLP to recognize entities, dependencies, coreferences in text taken from user speech
Once we recognize the user has specified an object (i.e. cut down a tree), how do we know what a tree is (computer vision)? Should the AI know to equip an axe? What the character does not have an axe?
(thanks Brian)

Other preliminary research:
Awesome NLP on github (curated list for NLP)
Automatic Text Classification: A Technical Review (Paper)
A Review of Machine Learning Algorithms for Text-Documents Classification (Paper)

### Evaluation Plan

Ideas:
We can make a set of tasks to evaluate the success of our project based on its difficulty to accomplish. The easiest set of actions would be make a single movement (“move forward, right, left, back, jump”). The next level would be some combinatorial actions “turn right and keep going straight, move right and jump etc..”. And the next one would be approach/attack/collect a closest object/target (“attack it, collect it, approach to it”) etc..
To make it quantitative, we can conduct hundred times of experiment and see the successful rate. i.e. for the task for the agent “going straight”, we should be able to see the agent command is “going straight” by inputting the speech “going straight (or it’s variant)”.
