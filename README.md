# Quantum Black Box Optimization activity

Hello QCSYSer!

In this exercise, students will attempt to optimize the parameters of
a circuit without knowing the actual contents of the circuit. Through this
activity students wilL *hopefully* reinvent some primitive form of gradient
descent, and so understand intuitively how a gradient-based optimizer works.
This will also demonstrate the difficulty that 'black box optimizers' face
when dealing with quantum circuits - i.e. variance of trigonometric functions
that can be either very large or vanishing.

## Installation

Run the commands:
```
git clone https://github.com/peterse/qcsys2019.git
cd qcsys2019
```
Make sure all packages and versions in `requirements.txt` are installed. No package installation necessary.

## Instructions

To run the program, make sure matplotlib as access to your display and run the script via command line with:
```
python3 parametrized_circuit_activity.py
```

Parameters can then be edited via command line input, and after each choice of parameters an exact loss will be printed and the Bloch sphere
display will update with the position of the current state guess (in black) and all previous guesses (color coded so that red is high loss,
blue is low loss).

To exit the script, run `Ctrl+C` then `Enter`.
