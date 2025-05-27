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
    
    def isLeftHandUpStraight(self):
        left_elbow = self.get(Keypoints.LEFT_ELBOW)
        left_wrist = self.get(Keypoints.LEFT_WRIST)
        # print(left_elbow.x - left_wrist.x)
        if abs(left_elbow.x - left_wrist.x) < 0.03 and left_elbow.y - left_wrist.y > 0.05:
            return True
        return False
    
    def isRightHandFurtherThanElbeow(self):
        right_elbow = self.get(Keypoints.RIGHT_ELBOW)
        right_wrist = self.get(Keypoints.RIGHT_WRIST)
        if right_elbow.x - right_wrist.x > 0.05:
            return True
        return False

    def howHighIsLefttHand(self):
        left_wrist = self.get(Keypoints.LEFT_WRIST)
        left_shoulder = self.get(Keypoints.RIGHT_SHOULDER)
        dif = left_wrist.y - left_shoulder.y
        if 0.05 > dif > -0.05:
            return 0
        elif -0.05 > dif > -0.15:
            return 1
        elif -0.15 > dif > -0.25:
            return 2
        elif -0.25 > dif > -0.35:
            return 3
        elif -0.35 > dif > -0.45:
            return 4
        elif -0.45 > dif:
            return 5
        elif 0.15 > dif > 0.05:
            return -1
        elif 0.25 > dif > 0.15:
            return -2
        elif 0.35 > dif > 0.25:
            return -3
        elif 0.45 > dif > 0.35:
            return -4
        elif dif > 0.45:
            return -5