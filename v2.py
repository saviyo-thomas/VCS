import cv2
import numpy as np

cap = cv2.VideoCapture('video.mp4')

count_line_pos = 550
min_width_rect = 80
min_height_rect = 80
# initialize substractor
algo = cv2.createBackgroundSubtractorMOG2()

def centre_handle(x,y,w, h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x+x1
    cy = y+y1
    return cx, cy

detect = []
offset = 6
cnt = 0

while True:
    ret, frm1 = cap.read()
    grey = cv2.cvtColor(frm1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3,3), 5)
    # applying on each frame
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))
    kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernal)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernal)
    countershape,h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frm1, (25, count_line_pos), (1200, count_line_pos), (255,127,0), 3)

    for (i,c) in enumerate(countershape):
        (x, y, w, h) = cv2.boundingRect(c)
        val_counter = (w>= min_width_rect) and (h>= min_height_rect)
        if not val_counter:
            continue
        cv2.rectangle(frm1, (x,y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(frm1, "Vehicle"+ str(cnt), (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,244,0), 2)

        centre = centre_handle(x,y,w,h)
        detect.append(centre)
        cv2.circle(frm1, centre, 4, (0,0,255), 2, -1)

        for (x, y) in detect:
            if y<(count_line_pos+ offset) and y>(count_line_pos- offset):
                cnt+=1
                cv2.line(frm1, (25, count_line_pos), (1200, count_line_pos), (0,127,255), 3)
                detect.remove((x,y))
                print("Vehicle Counter :" + str(cnt))
    cv2.putText(frm1, "Vehicle Counter :"+ str(cnt), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5)


    cv2.imshow('detector', dilatada)



    cv2.imshow('og video', frm1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()