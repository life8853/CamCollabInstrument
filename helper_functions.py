from enum import Enum
from mediapipe.framework.formats import landmark_pb2
import math


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


class Side(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"


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

    def isHandFurtherThanElbeow(self, side: Side):
        if side == Side.LEFT:
            elbow = self.get(Keypoints.LEFT_ELBOW)
            wrist = self.get(Keypoints.LEFT_WRIST)
        elif side == Side.RIGHT:
            elbow = self.get(Keypoints.RIGHT_ELBOW)
            wrist = self.get(Keypoints.RIGHT_WRIST)

        if elbow.x - wrist.x > 0.05:
            return True
        return False

    # chatgpt code
    def howHighIsHand(self, side: Side):
        if side == Side.LEFT:
            wrist = self.get(Keypoints.LEFT_WRIST)
            shoulder = self.get(Keypoints.LEFT_SHOULDER)
        elif side == Side.RIGHT:
            wrist = self.get(Keypoints.RIGHT_WRIST)
            shoulder = self.get(Keypoints.RIGHT_SHOULDER)

        dif = wrist.y - shoulder.y

        if abs(dif) <= 0.05:
            return 0

        bin_no = int((abs(dif) - 0.05) // 0.1) + 1
        bin_no = min(bin_no, 5)

        sign = 1 if dif > 0 else -1
        return -sign * bin_no

    def isCinema(self, side: Side):
        if side == Side.LEFT:
            wrist = self.get(Keypoints.LEFT_WRIST)
            elbow = self.get(Keypoints.LEFT_ELBOW)
            shoulder = self.get(Keypoints.LEFT_SHOULDER)
        elif side == Side.RIGHT:
            wrist = self.get(Keypoints.RIGHT_WRIST)
            elbow = self.get(Keypoints.RIGHT_ELBOW)
            shoulder = self.get(Keypoints.RIGHT_SHOULDER)

        def calculate_angle(a, b, c):
            """
            Returns the angle in degrees at point 'b' formed by points a-b-c.
            """
            # Vectors: ba and bc
            ba_x, ba_y = a.x - b.x, a.y - b.y
            bc_x, bc_y = c.x - b.x, c.y - b.y

            # Dot product and magnitudes
            dot_product = ba_x * bc_x + ba_y * bc_y
            mag_ba = math.sqrt(ba_x**2 + ba_y**2)
            mag_bc = math.sqrt(bc_x**2 + bc_y**2)

            if mag_ba == 0 or mag_bc == 0:
                return 0  # avoid division by zero

            angle_rad = math.acos(dot_product / (mag_ba * mag_bc))
            return math.degrees(angle_rad)

        return not calculate_angle(wrist, elbow, shoulder) > 75
