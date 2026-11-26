Rubik's Cube Robot by Nick Sciarretta

# Summary

The robot is essentially a Raspberry Pi connected to 5 stepper motors.
(There is no motor for the U face).

The robot can either use Kociemba's two-phase algorithm (for 5 faces) or my CFOP algorithm.

(My CFOP algorithm is by far inferior to Kociemba's algorithm,
but I kept it because I worked hard on it and I'm proud of it).

`
Note:
The two-phase tables for Kociemba's algorithm are too large to upload,
so they need to be created separately.
`

I also created a GUI (with pygame) to control the robot and enter the colours of the cube.
I use a portable touch screen connected to the RPi, but any monitor will do.

# ZMQ

In order to get the 3D animations of the GUI to sync with the motors, I had to use ZMQ.

`main.py` and `motors.py` must be run in parallel. `main.py` sends messages via ZMQ
to `motors.py` telling it what face(s) to turn and in what direction(s).

I tried other methods to get the animation and motors to turn at the same time
(multithreading, multiprocessing, etc) but this was the only option I tried that worked.

You can use this just as a generic Rubik's Cube solving program (without motors)
by setting `USE_MOTORS = False` in `python/GUI/constants.py`.

# How to use

Download the project to a folder.

(Optional) Download Kociemba's two-phase solver for 5 faces and create the tables.
Put the tables in `python/Kociemba/twophase-tables`.
(If you skip this step, the robot will default to using my CFOP algorithm).

If using this with motors:
- verify the pins in `python/Motors/constants.py` are correct (my robot and yours may differ).
- run `python/Motors/motors.py` in the background. (Remember to end `motors.py` after ending `main.py`!)

Run `python/main.py`.

Use the GUI controls (see below) to control the robot.

To adjust animation speed, adjust constants in `python/GUI/constants.py`.
To adjust motor speed, adjust constants in `python/Motors/constants.py`.

(It takes some trial and error to get the motors and animations to move at the same speed).

# GUI controls

When the GUI first boots, you are viewing the U, R, and F faces of the cube.

To change colours on the cube, select a colour on the left and click the desired cube facelet.

If the cube is solvable based on the colours that were input, the solve and scramble buttons will be enabled.
These buttons will solve / scramble the cube. (If the cube is not solvable, these buttons will be disabled).

While the motors are turning, certain buttons become disabled, but the "X" (abort) button becomes enabled.
The abort button will stop the motors. (Just in case they jam).

If the "360" button is disabled, the user can rotate the cube by swiping.
In this state, swipes rotate the cube 90° about pre-defined axes.

If the "360" button is enabled, the user can rotate the cube by dragging
their finger / mouse. In this state, the cube can rotate freely.

The "Home" button will rotate the cube back to the URF position.
The "Upside-down Home" button will rotate the cube to the DLB position.
