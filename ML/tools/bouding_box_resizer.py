import cv2
import sys
import os
import utils

data_path = "C:/Development/Robotics/FRC/Test_Vision/ML/Annotated_Data/vid/"
json_path = data_path + "data.json"
frame_numbers = [] #if this is blank it will go through all the frames

pointsX = []
pointsY = []
curr_pos = (0,0)

img = None
frame_name = "image"
img_x = 540
img_y = 960

def get_img(name, rect : tuple = None, show = True):
    global img, frame_name
    img = cv2.imread(data_path + name)
    img = cv2.resize(img, (img_x,img_y))
    # frame_name = name
    cv2.putText(img, name, (10,30), cv2.FONT_ITALIC, 1, (0,0,0), 2, cv2.LINE_AA)
    if not rect == None:
        cv2.rectangle(img, (rect[0],rect[1]), (rect[2],rect[3]), (0,255,0), 1)
    if show:
        cv2.imshow(frame_name,img)

def onMouseMove( event,x,y,flags,param):
    # if img is None: return

    global pointsX, pointsY, curr_pos

    curr_pos = (x,y)
    imgCopy = img.copy()

    if event == cv2.EVENT_LBUTTONDOWN and len(pointsX) < 2:    
        pointsX.append(x) 
        pointsY.append(y)
    elif event == cv2.EVENT_RBUTTONDOWN:
        pointsX.pop()
        pointsY.pop()
    
    if len(pointsX) == 1:
        cv2.rectangle(imgCopy, (pointsX[0],pointsY[0]), (x,y), (255,0,0), 2)
    elif len(pointsX) == 2:
        cv2.rectangle(imgCopy, (pointsX[0],pointsY[0]), (pointsX[1],pointsY[1]), (255,0,0), 2)

    cv2.imshow(frame_name,imgCopy)
        
def getRect(clear : bool = True):
    if clear:
        pointsX.clear()
        pointsY.clear()
    k = cv2.waitKey(0)
    #check if esc was pressed
    if k == 27:
        cv2.destroyAllWindows()
        sys.exit()
    
    if(len(pointsX) == 0):
        return None
    if(len(pointsX) == 1): 
        return (pointsX[0],pointsY[0],curr_pos[0],curr_pos[1])
    elif(len(pointsX) == 2):
        return (pointsX[0],pointsY[0],pointsX[1],pointsY[1])

if frame_numbers == []:
    data = utils.read_app_data(json_path)
    start = int(data["initial_frame"])
    step = int(data["skip_frames"]) + 1
    end = int(data["last_frame"])
    frame_numbers = range(start, end + 1, step)

files = []

for frame in frame_numbers:
    file_name = f"frame_{frame}"
    file_path = data_path + file_name
    with open(file_path + ".txt", "r") as f:
        data = f.read().split(" ")
        
    cls = data.pop(0)
    data = list(map(float, data))
    data = utils.center_to_edges(utils.denormilize(data, img_x, img_y))
    data = list(map(int, data))

    get_img(file_name + ".jpg", rect=data)

    cv2.setMouseCallback(frame_name, onMouseMove)

    rect = getRect()

    if rect == None:
        continue
    
    rect = utils.normalize(utils.edges_to_center(rect), img_x, img_y)

    with open(file_path + ".txt", "w") as f:
        f.write(f"{cls} {rect[0]} {rect[1]} {rect[2]} {rect[3]}")
    
cv2.destroyAllWindows()