# Opens the Video file
import cv2

cap= cv2.VideoCapture('data/video/eva-veil-1.ts')
count = 0
file_number = 0

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret:
        cv2.imwrite('data/frames/frame{:d}.jpg'.format( file_number ), frame)
        file_number += 1
        count += 990 # i.e. at 30 fps, this advances one second
        cap.set(1, count)
    else:
        cap.release()
        break

cap.release()
cv2.destroyAllWindows()
