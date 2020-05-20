# homewatch
A home security and automation system written in Python

##Prerequisites:
#### You need a Raspberry Pi 3+
#### You need to know the wires for your sensors. Use a multimeter continuity test to check if they work.
#### You need a GPIO breadboard and jumper wires.
#### You need to find BotFather on Telegram and get yourself a bot and its token
#### You need to install a few libs which dont come bundled with Raspian
+ sudo pip install telepot
+ sudo pip install configparser
#### Setup your home sensor pins as in the .conf file.

You will notice in the code that I am using a proxy. This is because some ISPs tend to block bots. So I have setup my pi as a proxy server as well. I followed a simple process of setting up a tor proxy server.

Give it a whirl!
