from cscore import CameraServer
import cv2
import numpy as np
import pupil_apriltags
from networktables import NetworkTables

print("starting app")

# connected = False

# def connectionListener(connected, info):
#    print(info, '; Connected=%s' % connected) 
#    connected = True


print("getting network tables")
NetworkTables.initialize(server='10.22.62.2')
inst = NetworkTables.getDefault()
table = inst.getTable("FMSInfo")

table.putNumberArray("things", [1,2,3,4])

print("network tables found")

#make apriltag detector
detector = pupil_apriltags.Detector(families='tag36h11')
print("detector configured")

width = 480
height = 320

cs = CameraServer.getInstance()
cs.enableLogging()

print("camera server found")

# Capture from the first USB Camera on the system
camera = cs.startAutomaticCapture()
camera.setResolution(width, height)

# Get a CvSink. This will capture images from the camera
cvSink = cs.getVideo()

print("camera server found")

# (optional) Setup a CvSource. This will send images back to the Dashboard
outputStream = cs.putVideo("RPI", width, height)

print("output stream made")

# Allocating new images is very expensive, always try to preallocate
img = np.zeros(shape=(height, width, 3), dtype=np.uint8)

print("app started!")

while True:
   # Tell the CvSink to grab a frame from the camera and put it
   # in the source image.  If there is an error notify the output.
   time, img = cvSink.grabFrame(img)

   if time == 0:
      # Send the output the error.
      outputStream.notifyError(cvSink.getError())
      # skip the rest of the current iteration
      continue

   img_2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

   result = detector.detect(img = img_2)

   for r in result:
      print(r)
      table.putString("things", str(r))
      img = cv2.line(img, tuple(map(int, r.corners[0])), tuple(map(int, r.corners[1])), (0,0,255), 5)
      img = cv2.line(img, tuple(map(int, r.corners[1])), tuple(map(int, r.corners[2])), (0,0,255), 5)
      img = cv2.line(img, tuple(map(int, r.corners[2])), tuple(map(int, r.corners[3])), (0,0,255), 5)
      img = cv2.line(img, tuple(map(int, r.corners[3])), tuple(map(int, r.corners[0])), (0,0,255), 5)

   # (optional) send some image back to the dashboard
   outputStream.putFrame(img)