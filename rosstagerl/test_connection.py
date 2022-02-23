"""Testing the connection.

This file will be deleted.
"""

import numpy as np

from .envs import RosControlsEnv


def test():

    # Instantiate
    ros_env = RosControlsEnv(n_actions=5, n_observations=5)

    ros_env.reset()

    # Test loop: the agent (you) chooses an action
    while True:
        action = int(input("Next action "))
        if action < 0:
            ros_env.reset()
        else:
            obs, reward, done, info = ros_env.step(action)

        print(obs)
