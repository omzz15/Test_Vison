import cv2
import numpy as np
import pupil_apriltags

#make apriltag detector
detector = pupil_apriltags.Detector(families='tag36h11')

vid = cv2.VideoCapture(0)

while(True):
    ret, img = vid.read()
    
    img_2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    result : list[pupil_apriltags.Detection] = detector.detect(img = img_2, estimate_tag_pose = True)

    for r in result:
        print(r.pose_R)
        img = cv2.line(img, tuple(map(int, r.corners[0])), tuple(map(int, r.corners[1])), (0,0,255), 5)
        img = cv2.line(img, tuple(map(int, r.corners[1])), tuple(map(int, r.corners[2])), (0,0,255), 5)
        img = cv2.line(img, tuple(map(int, r.corners[2])), tuple(map(int, r.corners[3])), (0,0,255), 5)
        img = cv2.line(img, tuple(map(int, r.corners[3])), tuple(map(int, r.corners[0])), (0,0,255), 5)

    cv2.imshow("test", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()