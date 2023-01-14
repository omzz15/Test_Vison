from cscore import CameraServer
import cv2
import numpy as np

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
      outputStream.notifyError(cvSink.getError());
      # skip the rest of the current iteration
      continue

   #
   # Insert your image processing logic here!
   #

   

   # (optional) send some image back to the dashboard
   outputStream.putFrame(img)