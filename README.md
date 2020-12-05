# Ros-stage-rl

This project is used to run RL experiments on a running instance of [StageROSGym](https://github.com/iocchi/StageROSGym).

Development package.

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
