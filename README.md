# CS 4310 Project 1

## Overview
In this project, you are asked to simulate Distance Vector routing for a given network.  The main goal of this project is to study the impact of different factors on the convergence times to optimal routes.  You will be provided with multiple files that represent different network topologies.  Your simulator would need to build routing tables and then forward data packets until they reach their destinations based on the routing tables built.

## Details
This repository contains 3 text files describing the topology of three different networks. 

These files are: topology1.txt, topology2.txt, and topology3.txt

Another text file (converged_tables.txt) contains output from the simulator after passing all three topology files and running until all routing tables converged.

For more information about the project as well as other requirements, please read pr1.pdf.

Finally, the source code for the simulator is found in sim.py

To run the simulator, use this command from the command line (assuming Python 3 is default):
<br>
    `python sim.py <topology file> <number of rounds>`

You may need to use this command if Python 3 is not default:
<br>
    `python3 sim.py <topology file> <number of rounds>`
