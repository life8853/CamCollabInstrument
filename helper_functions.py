from enum import Enum
from mediapipe.framework.formats import landmark_pb2


class Keypoints(Enum):
    NOSE = 0
    LEFT_EYE_INNER = 1
    LEFT_EYE = 2
    LEFT_EYE_OUTER = 3
    RIGHT_EYE_INNER = 4
    RIGHT_EYE = 5
    RIGHT_EYE_OUTER = 6
    LEFT_EAR = 7
    RIGHT_EAR = 8
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16
    LEFT_PINKY = 17
    RIGHT_PINKY = 18
    LEFT_INDEX = 19
    RIGHT_INDEX = 20
    LEFT_THUMB = 21
    RIGHT_THUMB = 22
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    LEFT_HEEL = 29
    RIGHT_HEEL = 30
    LEFT_FOOT_INDEX = 31
    RIGHT_FOOT_INDEX = 32


class ActuallyFuckingUsefulPose:
    def __init__(self, landmarks, poseToExtract):
        pose_landmarks = landmarks.pose_landmarks
        poseFiltered = landmark_pb2.NormalizedLandmarkList()
        poseFiltered.landmark.extend(
            [
                landmark_pb2.NormalizedLandmark(
                    x=landmark.x, y=landmark.y, z=landmark.z
                )
                for landmark in pose_landmarks[poseToExtract]
            ]
        )

        self.keypoints = poseFiltered.landmark
    
    def get(self, keypoint: Keypoints):
        return self.keypoints[keypoint.value]
    
def isLeftHandUpStraight(pose: ActuallyFuckingUsefulPose):
    left_elbow = pose.get(Keypoints.LEFT_ELBOW)
    left_wrist = pose.get(Keypoints.LEFT_WRIST)
    # print(left_elbow.x - left_wrist.x)
    if abs(left_elbow.x - left_wrist.x) < 0.03:
        print("straight up")