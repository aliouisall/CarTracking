from ultralytics import YOLO
from ultralytics.solutions import speed_estimation
import cv2

model = YOLO("models/yolov8n.pt")
names = model.model.names

cap = cv2.VideoCapture("tests/Test4.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Video writer
video_writer = cv2.VideoWriter("speed_estimation.mp4",
                               cv2.VideoWriter_fourcc(*'avc1'),
                               fps,
                               (w, h))

line_pts = [(0, 360), (1280, 360)]

# Init speed-estimation obj
speed_obj = speed_estimation.SpeedEstimator()
speed_obj.set_args(reg_pts=line_pts,
                   names=names,
                   view_img=True)

while cap.isOpened():

    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    tracks = model.track(im0, persist=True, show=False)

    im0 = speed_obj.estimate_speed(im0, tracks)
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()