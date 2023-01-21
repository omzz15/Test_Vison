import cv2
import sys
import json
import os

create_data = True

video_path = "C:/Development/Robotics/FRC/Test_Vision/ML/Cone_Data/Videos/"
video_name = "vid.mp4"

data_out_path = "C:/Development/Robotics/FRC/Test_Vision/ML/Annotated_Data/"
data_out_path += video_name.split(".")[0] + "/"

width = 540
height = 960

skip_frames = 49


video : cv2 = cv2.VideoCapture(video_path + video_name)

if not video.isOpened():
    print("Could not open video")
    sys.exit()

# ok, frame = video.read()
# if not ok:
#     print('Cannot read video file')
#     sys.exit()

# save the frame
# cv2.imwrite('C:/Development/Robotics/FRC/Test_Vision/ML/Cone_Data/Videos/vid.jpg', frame)

def prosessFrame(frame):
    frame = cv2.resize(frame, (width, height))
    # find all parts in certain HSV range
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    with open("C:/Development/Robotics/FRC/Test_Vision/ML/Cone_Data/color_data.json", "r") as f:
        data = json.load(f)
    mask = cv2.inRange(hsv_frame, tuple(data["HSV_low"]), tuple(data["HSV_high"]))
    # find all contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return frame, contours, mask

if create_data and not os.path.exists(data_out_path):
    os.mkdir(data_out_path)

while True:
    ok, frame = video.read()
    if not ok:
        break

    frame, contours, mask = prosessFrame(frame)
    largest_contours = max(contours, key=cv2.contourArea)
    
    x,y,w,h = cv2.boundingRect(largest_contours)

    if create_data:
        # save the frame
        name = f"frame_{int(video.get(cv2.CAP_PROP_POS_FRAMES))}"
        cv2.imwrite(data_out_path + name + ".jpg", frame)
        center_x = x + w/2
        center_y = y + h/2

        scaled_center_x = center_x / width
        scaled_center_y = center_y / height
        scaled_w = w / width
        scaled_h = h / height

        with open(data_out_path + name + ".txt", "w") as f:
            f.write(f"1 {scaled_center_x} {scaled_center_y} {scaled_w} {scaled_h}")

    frame = cv2.drawContours(frame, [largest_contours], -1, (0, 255, 0), 3)
    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
    cv2.putText(frame, 'Cone', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    cv2.imshow('image',frame)
    cv2.imshow('mask',mask)

    c = cv2.waitKey(50)
    if c == 27:
        break

    #skip frames
    for i in range(skip_frames):
        ok, _ = video.read()
        if not ok:
            break

video.release()
cv2.destroyAllWindows()