import cv2
import numpy as np

ix, iy, k = 200, 200, 1


def onMouse(event, x, y, flag, param):
    global ix, iy, k
    if event == cv2.EVENT_LBUTTONDOWN:
        ix, iy = x, y
        k = -1


cv2.namedWindow("window")
cv2.setMouseCallback("window", onMouse)

cap = cv2.VideoCapture("./data/input_data/car_park.mp4")

# detection using mouse click
while True:
    ret, frame = cap.read()

    cv2.imshow("window", frame)

    if cv2.waitKey(1) == ord('p'):
        cv2.waitKey(-1)

    if cv2.waitKey(1) == 27 or k == -1:
        old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.destroyAllWindows()
        break

old_pts = np.array([[ix, iy]], dtype="float32").reshape(-1, 1, 2)
layout = cv2.imread("./data/input_data/layout.png")
mask = np.zeros_like(frame)

# tracking
while True:
    ret2, frame2 = cap.read()
    new_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    new_pts, status, err = cv2.calcOpticalFlowPyrLK(old_gray,
                                                    new_gray,
                                                    old_pts,
                                                    None, maxLevel=1,
                                                    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                                                              15, 0.08))

    # draw tracked points
    cv2.circle(mask, (new_pts.ravel()[0],
                      new_pts.ravel()[1]), 2, (0, 255, 0), 2)
    combined = cv2.addWeighted(frame2, 0.7, mask, 0.3, 0.1)

    pts1 = np.float32([[200, 270], [460, 258],
                       [275, 475], [817, 457]])

    pts2 = np.float32([[290, 36], [611, 34],
                       [290, 529], [558, 569]])

    # mapping
    p = (new_pts.ravel()[0], new_pts.ravel()[1])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    px = (matrix[0][0]*p[0] + matrix[0][1]*p[1] + matrix[0][2]) / \
        ((matrix[2][0]*p[0] + matrix[2][1]*p[1] + matrix[2][2]))
    py = (matrix[1][0]*p[0] + matrix[1][1]*p[1] + matrix[1][2]) / \
        ((matrix[2][0]*p[0] + matrix[2][1]*p[1] + matrix[2][2])) + 200

    # project tracked point on layout
    p_after = (int(px), int(py))

    cv2.circle(layout, p_after, 2, (0, 255, 0), 2)
    cv2.imshow("bird's eye", layout)
    cv2.imshow("tracking", combined)

    old_gray = new_gray.copy()
    old_pts = new_pts.copy()

    key = cv2.waitKey(1)
    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
    if key == ord('p'):
        cv2.waitKey(-1)
