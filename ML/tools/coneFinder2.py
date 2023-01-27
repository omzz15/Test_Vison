import cv2
import sys
import json
import os
import utils

create_data = False #input() == "True"

video_path = "C:/Development/Robotics/FRC/Test_Vision/ML/Cone_Data/Videos/"
video_name = "cone.mp4"

data_out_path = "C:/Development/Robotics/FRC/Test_Vision/ML/Annotated_Data/"
data_out_path += video_name.split(".")[0] + "/"
data_out_json = data_out_path + "data.json"

width = 540
height = 960

skip_frames_initial = 0
skip_frames = 0

label = [0,"cone"]

video : cv2 = cv2.VideoCapture(video_path + video_name)

if not video.isOpened():
    print("Could not open video")
    sys.exit()

for i in range(skip_frames_initial):
    video.read()

# save the frame
# cv2.imwrite('C:/Development/Robotics/FRC/Test_Vision/ML/Cone_Data/Videos/vid.jpg', frame)

def prosessFrame(frame):
    # frame = cv2.resize(frame, (width, height))
    # find all parts in certain HSV range
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    with open("C:/Development/Robotics/FRC/Test_Vision/ML/Cone_Data/color_data.json", "r") as f:
        data = json.load(f)
    mask = cv2.inRange(hsv_frame, tuple(data["HSV_low"]), tuple(data["HSV_high"]))
    # find all contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return frame, contours, mask

if create_data:
    if not os.path.exists(data_out_path):
        os.mkdir(data_out_path)
    app_data = {
        "video_path": video_path,
        "video_name": video_name,
        width: width,
        height: height,
        "initial_frame": skip_frames_initial + 1,
        "skip_frames": skip_frames,

        "labels" : {label[0] : label[1]}
    }
    utils.update_app_data(data_out_json, app_data)

while True:
    ok, og_frame = video.read()
    frame = og_frame.copy()
    if not ok:
        break

    frame, contours, mask = prosessFrame(frame)
    largest_contours = max(contours, key=cv2.contourArea)
    
    x,y,w,h = cv2.boundingRect(largest_contours)

    if create_data:
        current_frame = int(video.get(cv2.CAP_PROP_POS_FRAMES))
        # save the frame
        name = f"frame_{current_frame}"
        cv2.imwrite(data_out_path + name + ".jpg", frame)

        # transfrom data
        x2,y2,w2,h2 = utils.normalize(utils.edge_with_size_to_center((x,y,w,h)), width, height)

        with open(data_out_path + name + ".txt", "w") as f:
            f.write(f"{label[0]} {x2} {y2} {w2} {h2}")
    
        data = {"last_frame": current_frame}
        utils.update_app_data(data_out_json, data)

    frame = cv2.drawContours(frame, [largest_contours], -1, (0, 255, 0), 3)
    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
    cv2.putText(frame, 'Cone', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    cv2.imshow('image',frame)
    cv2.imshow('mask',mask)

    c = cv2.waitKey(50)
    if c == ord("s"):
        current_frame = int(video.get(cv2.CAP_PROP_POS_FRAMES))
        cv2.imwrite(f"C:/Development/Robotics/FRC/Test_Vision/ML/Cone_Data/frame_{current_frame}.jpg", og_frame)
    if c == 27:
        break

    #skip frames
    for i in range(skip_frames):
        ok, _ = video.read()
        if not ok:
            break
    
    

video.release()
cv2.destroyAllWindows()