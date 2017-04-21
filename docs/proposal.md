---
layout: default
title: Proposal
---

### Summary of the Project

This project aims at implementing a speech-to-command feature to allow the user to take control of the actions of an agent in Minecraft. It will take speech as an initial input, convert that speech to text, analyze the text to extract a legal action, and finally send a command for the agent to take as an output. Potential applications for the project may include partially or fully playing a game with speech alone.

### AI/ML Algorithms

Automatic text classification with hybrid machine learning approach (combination of naive bayes, decision tree, neural nets, and SVM etc..).

### Evaluation Plan

We will create a set of tasks to evaluate the success of our project based on the difficulty of accomplishing those tasks. The easiest set of actions would be to make a single movement (“move forward, right, left, back, jump”). The next level would be some combinatorial actions “turn right and keep going straight, move right and jump etc..”. And the next one would be to approach/attack/collect a closest object/target (“attack it, collect it, approach to it, etc..). To make it quantitative, we can conduct an experiment over hundreds of times and see the success rate. For example, for a task such as “going straight”, we should be able to see that the agent's command is equivalent to “going straight” by inputting the speech “going straight" (or it’s variant).

# Appointment with the Instructor

4/25 (Tuesday) 3:15pm
