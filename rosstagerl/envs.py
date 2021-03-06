"""Definition of Gym environments."""

import gym
import numpy as np

from .streaming import Sender, Receiver


class RosControlsEnv(gym.Env):
    """Gym environment that controls ROS.

    Actions performed on this environment are forwarded to a running ROS
    instance and the states are those returned from the robot.
    This environment communicates with a running instance of
    https://github.com/iocchi/StageROSGym. See that repo to setup also the
    other side.
    """
    
    # NOTE: many settings depend on the communication protocol.
    #   Make sure that the other side respects the same actions, signals,
    #   and observation space.

    # Other (non-RL) signals
    _signals = {
        "reset": -1,
    }

    # Communication protocol
    actions_port = 30005
    states_port = 30006
    state_msg_len = 20    # a numpy vector of 5 float32
    action_msg_len = 4    # a positive numpy scalar of type int32


    class StateReceiver(Receiver):
        """Just a wrapper that deserializes state vectors."""

        def receive(self):
            """Return a state vector received.

            :return: a numpy vector of the most recent state.
            """

            # Receive
            buff = Receiver.receive(self, wait=True)

            # Deserialize
            assert len(buff) == RosControlsEnv.state_msg_len
            array = np.frombuffer(buff, dtype=np.float32)
            return array


    class ActionSender(Sender):
        """Just a wrapper that serializes actions."""

        def send(self, action):
            """Send an action.

            :param action: a scalar action or signal.
            """

            # Serialize
            buff = np.array(action, dtype=np.int32).tobytes()
            assert len(buff) == RosControlsEnv.action_msg_len

            # Send
            Sender.send(self, buff)


    def __init__(self, n_actions):
        """Initialize.

        :param n_actions: the number of action allowed from the 
            remote ROS Controller.
        """

        # Define spaces
        self.action_space = gym.spaces.Discrete(n_actions)
        self.observation_space = gym.spaces.Box(
            low=float("-inf"), high=float("inf"), shape=[5], dtype=np.float32)
            # NOTE: Actually the third is an angle

        # Initialize connections
        self.action_sender = RosControlsEnv.ActionSender(
            msg_length=self.action_msg_len, port=self.actions_port, wait=True,
        )
        self.state_receiver = RosControlsEnv.StateReceiver(
            msg_length=self.state_msg_len, ip="localhost",
            port=self.states_port, wait=True,
        )

        # Connect now
        self.action_sender.start()
        print("> Serving actions on", self.action_sender.server.server_address)
        print("> Connecting to ", self.state_receiver.ip, ":",
            self.state_receiver.port, " for states. (pause)",
            sep="", end=" ",
        )
        input()
        self.state_receiver.start()


    def reset(self):
        """Reset the environment to the initial state.

        :return: The initial observation.
        """

        # Send signal
        self.action_sender.send(
            self._signals["reset"]
        )

        # TODO: return initial state


    def step(self, action):
        """Run one timestep of the environment's dynamics.

        :param action: the action to perform.
        :return:
            observation: the next observation
            reward (float): the scalar reward
            done (bool): whether the episode has ended
            info (dict): other infos
        """

        # Check
        if not 0 <= action < self.action_space.n:
            raise RuntimeError(str(action) + " is not an action.")

        # Execute
        self.action_sender.send(action)

        # Read observation
        observation = self.state_receiver.receive()

        # TODO: compute reward and done according to a criterion implemented
        #   in some external class
        return (observation, 0.0, False, {})

