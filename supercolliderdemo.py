from pythonosc import udp_client
import time

# Set IP and port of the SuperCollider machine
client = udp_client.SimpleUDPClient("127.0.0.1", 57110)

# Send a message to trigger sound

synth_name = "sine"
node_id = 1002      # Any unique number — must be tracked if you want to stop it later
add_action = 1      # Add to the head of target node
target_node = 0     # Root node
freq = 660          # Frequency in Hz


client.send_message("/s_new", [synth_name, node_id, add_action, target_node, "freq", freq])  # This will play a 660 Hz tone
time.sleep(1)
client.send_message("/n_free", [node_id])