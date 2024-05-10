import pyautogui
import  cv2
import numpy as np

#specific resolution
resolution = (1920, 1080)

#specific video codec
codec = cv2.VideoWriter_fourcc(*"XVID")

#specify name of output file
filename = "Recording.avi"

fps = 60.0

out = cv2.VideoWriter(filename, codec, fps, resolution)

cv2.namedWindow("LIVE", cv2.WINDOW_NORMAL)

cv2.resizeWindow("LIVE", 480, 270)

while True:
    img = pyautogui.screenshot()

    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    out.write(frame)
    cv2.imshow('LIVE', frame)

    if cv2.waitKey(1) == ord('q'):
        break

out.release()
cv2.destroyAllWindows()