[![GitHub version](https://badge.fury.io/gh/Naereen%2FStrapDown.js.svg)](https://github.com/Naereen/StrapDown.js)
[![GitHub release](https://img.shields.io/github/release/Naereen/StrapDown.js.svg)](https://GitHub.com/Naereen/StrapDown.js/releases/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Discord](https://img.shields.io/discord/591914197219016707.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/fJhhkXn)
==================================
honey v2 | Link Submission Manager
==================================
Overview
=========
honey v2 will be a simpler tool in coordinating efforts between the Speaker Haven and Speaker Honey's twitch channel.

Current Python version: 3.8.3

IDE: JetBrains - pyCharm


Pseudo Explanations
===================

**CommandHandler.py**

-Checks if the message starts with a command trigger, if it doesn't it stops.

-If the message does start with a trigger if makes sure that the trigger is valid by comparing it to the command dictionary's trigger value, if it's not it stops.

-If the trigger is valid it removes the trigger from the message string and splits it at the spaces making an array named args.

-Then it checks to see how many args the command's function takes using the command dictionary's args_num value, if it's zero it simply executes the function in the command dictionary's function value. If the command needs more than zero args it makes sure that there are at least the required amount and it passes them to the command dictionary's function.

Reference
=========

**discord.py Documentation:**
https://discordpy.readthedocs.io/en/latest/

**Current discord.py working branch:**
https://github.com/Rapptz/discord.py/tree/master
