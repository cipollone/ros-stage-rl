"""Testing the connection.

This file will be deleted.
"""

import numpy as np

from .streaming import Sender, Receiver

# TODO: verify that actions and states are correctly exchanged
# TODO: delete this file

# Communication protocol
actions_port = 30005
states_port = 30006
state_msg_len = 20    # a numpy vector of 5 float32
action_msg_len = 4    # a numpy scalar of type int32



def test():

    # Instantiate
    action_sender = Sender(
        msg_length=action_msg_len, port=actions_port, wait=True)
    state_receiver = Receiver(
        msg_length=state_msg_len, ip="localhost", port=states_port, wait=True)

    # Start server and client
    #   NOTE: make sure that the couple is started also on the other side
    action_sender.start()
    input("Serving actions on " + str(action_sender.server.server_address))
    state_receiver.start()

    # Test loop: the agent (you) chooses an action
    while True:
        action = int(input("Next action "))
        action_sender.send(_action2binary(action))
        state = _binary2state(state_receiver.receive(wait=True))
        print("State", state)

    print("done")


def _action2binary(action):
    """Converts a action to a byte."""

    buff = np.array(action, dtype=np.int32).tobytes()
    assert len(buff) == action_msg_len
    return buff

def _binary2state(buff):
    """Converts bytes to a state vector."""

    assert len(buff) == state_msg_len
    array = np.frombuffer(buff, dtype=np.float32)
    return array
