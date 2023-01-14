from cscore import CameraServer
import cv2
import numpy as np
import pupil_apriltags

#make apriltag detector
detector = pupil_apriltags.Detector(families='tag36h11')


width = 480
height = 320

cs = CameraServer.getInstance()
cs.enableLogging()

# Capture from the first USB Camera on the system
camera = cs.startAutomaticCapture()
camera.setResolution(width, height)

# Get a CvSink. This will capture images from the camera
cvSink = cs.getVideo()

# (optional) Setup a CvSource. This will send images back to the Dashboard
outputStream = cs.putVideo("Name", width, height)

# Allocating new images is very expensive, always try to preallocate
img = np.zeros(shape=(height, width, 3), dtype=np.uint8)

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

   result : list[pupil_apriltags.Detection] = detector.detect(img = img_2)

   for r in result:
      img = cv2.line(img, tuple(map(int, r.corners[0])), tuple(map(int, r.corners[1])), (0,0,255), 5)
      img = cv2.line(img, tuple(map(int, r.corners[1])), tuple(map(int, r.corners[2])), (0,0,255), 5)
      img = cv2.line(img, tuple(map(int, r.corners[2])), tuple(map(int, r.corners[3])), (0,0,255), 5)
      img = cv2.line(img, tuple(map(int, r.corners[3])), tuple(map(int, r.corners[0])), (0,0,255), 5)

   # (optional) send some image back to the dashboard
   outputStream.putFrame(img)