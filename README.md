# Ros-stage-rl

This project is used to run RL experiments on a running instance of [stage-controls](https://github.com/cipollone/stage-controls).

## Install and use

Install for normal use as:

    pip install git+https://github.com/cipollone/ros-stage-rl
  
or install for development as:

    git clone https://github.com/cipollone/ros-stage-rl
    cd ros-stage-rl
    poetry install

This package requires Python ^3.7. If this version is not installed in your system, we suggest to use the very convenient `pyenv`.

To use this package, simply run:

    python3 -m rosstagerl              # if installed
    poetry run python3 -m rosstagerl   # if under development
	

NOTE: together with stage-controls, this package defines a communication protocol for observations and actions.
Both spaces need to match between the two packages' versions, otherwise communication won't take place as expected.
In particular, actions are in a discrete set, sent as int32 indexes, starting from 0, and observations are a numpy array of float32.
The two versions must agree on the number of actions and observations.
