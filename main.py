import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2 as cv
import numpy as np
from helper_functions import ActuallyFuckingUsefulPose, Side


MODEL_PATH = "./pose_landmarker_full.task"
SKIP_FRAMES = 8
CAM_INDEX = 1

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode


# Create a pose landmarker instance with the live stream mode:
def print_result(
    result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int
):
    print("pose landmarker result: {}".format(result))


# Google wrote this don't blame me pls
def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected poses to visualize.
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

        # Draw the pose landmarks.
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend(
            [
                landmark_pb2.NormalizedLandmark(
                    x=landmark.x, y=landmark.y, z=landmark.z
                )
                for landmark in pose_landmarks
            ]
        )

        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style(),
        )
    return annotated_image


def main():
    options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=VisionRunningMode.VIDEO,
        num_poses=2,
    )

    with PoseLandmarker.create_from_options(options) as landmarker:
        cam = cv.VideoCapture(CAM_INDEX)
        if not cam.isOpened():
            print("Cannot open camera")
            exit()

        cv.namedWindow("image", cv.WINDOW_GUI_NORMAL)
        ret, bgr = cam.read()
        if not ret:
            raise SystemExit("Unable to read from camera")
        cv.imshow("image", bgr)
        # cv.setWindowProperty("image", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

        frame_id = 0
        while True:
            ret, bgr_frame = cam.read()

            if not ret:
                print("Can't recieve stream from camera")
                exit()

            if frame_id % (SKIP_FRAMES + 1) == 0:
                try:
                    mpImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=bgr_frame)
                    # hack beacuse idk something doesnt work
                    frameTimestampMs = frame_id * 17
                    # frameTimestampMs = int(cam.get(cv.CAP_PROP_POS_MSEC))

                    results = landmarker.detect_for_video(mpImage, frameTimestampMs)
                    person_1 = ActuallyFuckingUsefulPose(results, 0)
                    print(person_1.howHighIsLefttHand(Side.RIGHT))

                    frame = draw_landmarks_on_image(
                        cv.cvtColor(bgr_frame, cv.COLOR_BGR2RGB), results
                    )
                    frame = cv.resize(frame, (1900, 1000))
                    cv.imshow("image", cv.cvtColor(frame, cv.COLOR_RGB2BGR))
                except Exception as e:
                    print(e)
            else:
                bgr_frame = cv.resize(bgr_frame, (1900, 1000))
                cv.imshow("image", bgr_frame)

            if cv.waitKey(1) == ord("q"):
                break

            frame_id += 1

        cam.release()
        cv.destroyAllWindows()


if __name__ == "__main__":
    main()
