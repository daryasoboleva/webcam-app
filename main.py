import cv2
import os.path

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)

counterPhoto = 0
counterVideo = 0
avi = cv2.VideoWriter_fourcc('M','J','P','G')
mp4 = cv2.VideoWriter_fourcc(* 'XVID')
# Получить информацию о размере кадра
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
    faces = faceCascade.detectMultiScale(frameGray, 1.1, 19)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)
    cv2.imshow("CAMERA", frame)
    pressKey = cv2.waitKey(1)

    if pressKey & 0xFF == ord('e'):
        print("Камера выключилась")
        break
    elif pressKey & 0xFF == ord('p'):
        if cv2.imwrite(f"Photos/photo_{counterPhoto}.png", frameCopy):
            f = open("PhotoCounter.txt", 'r')
            s = f.readline()
            counterPhoto = int(s[-1])
            print("photo_" + str(counterPhoto) + ".png успешно сохранено")
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
                print("Началась запись video_" + str(counterVideo) + ".avi" )
                outputVideo.write(frameCopy)
                Recording = True
            else:
                print("Произошла ошибка")
                outputVideo.release()
                Recording = False
        else:
            if success:
                outputVideo.write(frameCopy)
            print("Запись video_" + str(counterVideo) + ".avi сохранена")
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