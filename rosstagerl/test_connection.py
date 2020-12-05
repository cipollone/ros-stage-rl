"""Testing the connection.

This file will be deleted.
"""

from .streaming import Sender, Receiver

# TODO: verify that actions and states are correctly exchanged
# TODO: delete this file

# Communication protocol
actions_port = 30005
states_port = 30006
state_msg_len = 20    # a numpy vector of 5 float32
action_msg_len = 1    # a numpy scalar of type uint8



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

    input()
    print("done")
