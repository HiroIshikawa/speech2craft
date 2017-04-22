---
layout: default
title: Proposal
---

### Summary of the Project

This project aims at implementing speech-to-command feature to allow user to take control on actions of an agent in a world of Minecraft. It will take user speech as initial input, and convert it using online speech-to-text APIs. Then, we will analyze the text to extract a legal action using Natural Language Processing, and finally send a command for an agent to take that action as an output. Potential applications may include partially or fully speech based game playing.

We were also considering implementing a conversational AI agent, that may respond or even object to user speech commands. However, this would come secondary to our main focus of implementing the speech-to-command feature.

### AI/ML Algorithms

Automatic text classification with hybrid machine learning approach (combination of naive bayes, decision tree, neural nets, and SVM etc..).

### Evaluation Plan

We will create a set of tasks to evaluate the success of our project based on the difficulty of accomplishing those tasks. The easiest set of actions would be to make a single movement (“move forward, right, left, back, jump”). The next level would be some combinatorial actions “turn right and keep going straight, move right and jump etc..”. And the next one would be to approach/attack/collect a closest object/target (“attack it, collect it, approach to it, etc..). To make it quantitative, we can conduct an experiment over hundreds of times and see the success rate. For example, for a task such as “going straight”, we should be able to see that the agent's command is equivalent to “going straight” by inputting the speech “going straight" (or it’s variant).

# Appointment with the Instructor

4/25 (Tuesday) 3:15pm
