import cv2
import time

vid = cv2.VideoCapture('video.mp4')

ret, fr1 = vid.read()

count_line_pos = 550

def centre_handle(x,y,w, h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x+x1
    cy = y+y1
    return cx, cy


detect = []
offset = 6
cnt = 0

while vid.isOpened():
    ret, fr2 = vid.read()
    if not ret:
        break
    frm = fr2.copy()
    

    
    
    msk = cv2.absdiff(fr1, fr2)

    msk = cv2.cvtColor(msk, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(msk, 25, 255, cv2.THRESH_BINARY)

    fr1 = fr2

    conts, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for c in conts:

        if cv2.contourArea(c) < 3400:
            continue
        
        x, y, w, h = cv2.boundingRect(c)

        cv2.rectangle(frm, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frm, "Vehicle"+ str(cnt), (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,244,0), 2)
        centre = centre_handle(x,y,w,h)
        detect.append(centre)
        cv2.circle(frm, centre, 4, (0,0,255), 2, -1)
        for (x, y) in detect:
            if y<(count_line_pos+ offset) and y>(count_line_pos- offset):
                cnt+=1
                cv2.line(frm, (25, count_line_pos), (1200, count_line_pos), (0,127,255), 3)
                detect.remove((x,y))
                print("Vehicle Counter :" + str(cnt))
    cv2.putText(frm, "Vehicle Counter :"+ str(cnt), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5)
    
    #cv2.imshow('msk', msk)
    cv2.imshow('og', frm)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
                                
cv2.destroyAllWindows()
vid.release()
