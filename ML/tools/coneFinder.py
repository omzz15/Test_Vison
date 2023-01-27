import cv2
import sys

tracker = cv2.TrackerCSRT_create()

video = cv2.VideoCapture("C:/Development/Robotics/FRC/Test_Vision/ML/Cone_Data/Videos/vid.mp4")

if not video.isOpened():
    print("Could not open video")
    sys.exit()

ok, frame = video.read()
if not ok:
    print('Cannot read video file')
    sys.exit()

pointsX = []
pointsY = []

img = frame.copy()
img = cv2.resize(img, (540,960))

cv2.imshow('image',img)

def mousePosition( event,x,y,flags,param):
    imgCopy = img.copy()
    
    if event == cv2.EVENT_LBUTTONDOWN:  
        pointsX.append(x) 
        pointsY.append(y)
    if event == cv2.EVENT_RBUTTONDOWN:
        pointsX.pop()
        pointsY.pop()
    
    if len(pointsX) > 0:
        cv2.line(imgCopy, (pointsX[-1], pointsY[-1]), (x,y), (0,255,0), 3)
    
    if len(pointsX) > 1:
        cv2.line(imgCopy, (x, y), (pointsX[0], pointsY[0]), (0,255,0), 3)


    for i in range(len(pointsX) - 1):
        cv2.line(imgCopy, (pointsX[i], pointsY[i]), (pointsX[i+1], pointsY[i+1]), (0,255,0), 3)
  
    
    cv2.imshow('image',imgCopy)
        
def wait():
    cv2.waitKey(0)
    if(len(pointsX) >= 3): cv2.destroyAllWindows()
    else:
        print("make shape!!")
        wait()

cv2.setMouseCallback('image', mousePosition)    
wait()

pointsX = [x * 2 for x in pointsX]
pointsY = [y * 2 for y in pointsY]

bbox = (pointsX[0], pointsY[0], pointsX[1] - pointsX[0], pointsY[1] - pointsY[0])

ok = tracker.init(frame, bbox)

while True:
    ok, frame = video.read()
    if not ok:
        break

    ok, bbox = tracker.update(frame)
    if ok:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

    s_img = cv2.resize(frame, (540,960))
    cv2.imshow("Tracking", s_img)

    k = cv2.waitKey(1) & 0xff
    if k == 27 : break