from pythonosc import udp_client
from helper_functions import ActuallyFuckingUsefulPose, Side
import mediapipe as mp

client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

playing = False

def sendMessagesFromPersonDataAsync(results: mp.tasks.vision.PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):

    if(len(results.pose_landmarks) > 0):
        person = ActuallyFuckingUsefulPose(results, 0)
        global playing
        if(person.isHandFurtherThanElbeow(Side.RIGHT) and not playing):
            client.send_message("/startpattern",[])
            playing = True
        elif (not person.isHandFurtherThanElbeow(Side.RIGHT) and playing):
            # client.send_message("/stoppattern",[])
            playing = False

        if(person.howHighIsHand(Side.LEFT) > 0):
            client.send_message("/changeinstrument",["bd",22])
        else:
            client.send_message("/changeinstrument",["arpy",0])

        if(len(results.pose_landmarks) > 0):
            person2 = ActuallyFuckingUsefulPose(results, 0)
            if(person2.isCinema(Side.LEFT)):
                print("reverb")
                client.send_message("/setreverb",[True])
            else:
                print("noreverb")
                client.send_message("/setreverb", [False])
