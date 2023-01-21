import cv2
import sys
import os
import utils

data_path = "C:/Development/Robotics/FRC/Test_Vision/ML/Annotated_Data/vid/"
frame_numbers = [] #if this is blank it will go through all the frames

pointsX = []
pointsY = []
curr_pos = (0,0)

img = None
frame_name = None
img_x = 540
img_y = 960

def get_img(name, rect : tuple = None, show = True):
    global img, frame_name
    img = cv2.imread(data_path + name)
    img = cv2.resize(img, (img_x,img_y))
    frame_name = name
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
        
def getRect():
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

files = []

if frame_numbers == []:
    for path in os.listdir(data_path):
        if os.path.isfile(os.path.join(data_path, path)):
            files.append(path)
else:
    for frame in frame_numbers:
        files.append(f"frame_{str(frame)}.jpg")
        files.append(f"frame_{str(frame)}.txt")

for i in range(0,len(files),2):
    with open(data_path + files[i+1], "r") as f:
        data = f.read().split(" ")
    
    cls = data.pop(0)
    data = list(map(float, data))
    data = utils.center_to_edges(utils.denormilize(data, img_x, img_y))
    data = list(map(int, data))

    get_img(files[i], rect=data)

    cv2.setMouseCallback(frame_name, onMouseMove)

    rect = getRect()

    if rect == None:
        continue
    
    rect = utils.normalize(utils.edges_to_center(rect), img_x, img_y)

    with open(data_path + files[i+1], "w") as f:
        f.write(f"{cls} {rect[0]} {rect[1]} {rect[2]} {rect[3]}")

cv2.destroyAllWindows()