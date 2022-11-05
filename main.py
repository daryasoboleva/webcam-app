import cv2
import os.path
import sys
import numpy as np

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)

hsv_min = np.array((0, 54, 5), np.uint8)
hsv_max = np.array((187, 255, 253), np.uint8)
counterPhoto = 0
counterVideo = 0
avi = cv2.VideoWriter_fourcc('M','J','P','G')
mp4 = cv2.VideoWriter_fourcc(* 'XVID')
# Get information about size of frame
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_size = (frame_width, frame_height)
fps = 10
Recording = False

while True:
    pathToPhoto = f"Photos/photo_{counterPhoto}.png"
    if not os.path.exists(f"Photos/photo_{counterPhoto}.png"):
        continue
    break
while True:
    pathToVideo = f"Video/video_{counterVideo}.avi"
    if not os.path.exists(pathToVideo):
        break
while True:
    ret, frame = cap.read()
    cv2.imshow("CAMERA", frame)
    success, frameCopy = cap.read()
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # Load image, grayscale, median blur, sharpen image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpen = cv2.filter2D(blur, -10, sharpen_kernel)

    # Threshold and morph close
    thresh = cv2.threshold(sharpen, 50, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=5)

    # Find contours and filter using threshold area
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        area = cv2.contourArea(c)
        if area > 1900:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (36, 255, 12), 2)
    faces = faceCascade.detectMultiScale(frameGray, 1.1, 19)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)
    cv2.imshow("CAMERA", frame)
    pressKey = cv2.waitKey(1)
    if pressKey & 0xFF == ord('e'):
        print("Camera off")
        break
    elif pressKey & 0xFF == ord('p'):
        if cv2.imwrite(f"Photos/photo_{counterPhoto}.png", frameCopy):
            f = open("PhotoCounter.txt", 'r')
            s = f.readline()
            counterPhoto = int(s[-1])
            print("photo_" + str(counterPhoto) + ".png saved successfully")
            f.close()
            f = open("PhotoCounter.txt", 'a')
            f.write(str(counterPhoto + 1))
            f.close()
    elif pressKey & 0xFF == ord('v'):
        if not Recording:
            pathToVideo = f"Videos/video_{counterVideo}.avi"
            outputVideo = cv2.VideoWriter(pathToVideo, avi, fps, frame_size)
            if success:
                f = open("videoCounter.txt", 'r')
                s = f.readline()
                counterVideo = int(s[-1])
                f.close()
                f = open("videoCounter.txt", 'a')
                f.write(str(counterVideo + 1))
                f.close()
                print("Start record of video " + str(counterVideo) + ".avi" )
                outputVideo.write(frameCopy)
                Recording = True
            else:
                print("Error")
                outputVideo.release()
                Recording = False
        else:
            if success:
                outputVideo.write(frameCopy)
            print("Record of video_" + str(counterVideo) + ".avi is saved")
            Recording = False
            outputVideo.release()
    elif Recording:
        if success:
            outputVideo.write(frameCopy)

if Recording:
    outputVideo.release()
# release the camera from video capture
cap.release()
# De-allocate any associated memory usage
cv2.destroyAllWindows()