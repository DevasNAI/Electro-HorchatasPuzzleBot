## Robotics Foundation Week 1
On this week we solved the first challenge and activity, which was assigned by the benefactor **Manchester Robotics Ltd**. This challenge helped us familiarized with nodes, generating packages, using launch files for displaying data and using this data for rqt plot for the sine functions; and communication between nodes by publisher & subscribers for rostopics. 

### A little description about the files in this repository:
- challenge.launch (inside the launch folder) -> This is where the nodes and rostopics are executed so their values are shown on the terminal and the rqt_plot. The rqt_plot shows the original signal (it's a sine wave) with a phased sine wave (which is the processed signal).
- signal_generator.py -> as it's name states it, it generates a sine 
- process.py (inside the scripts folder) -> This code is a node that receives the signal and process it to a phased sine wave.
- CMakeLists.txt -> This document is made when a package is created, it's purpose is to help to declare the executable files.
- package.xml -> configuration file

## Photo of the final product:

## Team members
- Jorge Askur Vázquez
- Jose Miguel Flores
- Andres Sarellano 
- Jesús Eduardo Rodríguez 
- Izel Ávila

₍⑅ᐢ..ᐢ₎
