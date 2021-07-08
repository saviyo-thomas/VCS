import cv2
import time

vid = cv2.VideoCapture('video2.mp4')

ret, fr1 = vid.read()

while vid.isOpened():
    ret, fr2 = vid.read()
    frm = fr2.copy()
    

    if not ret:
        break
    
    msk = cv2.absdiff(fr1, fr2)

    msk = cv2.cvtColor(msk, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(msk, 25, 255, cv2.THRESH_BINARY)

    fr1 = fr2

    conts, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for c in conts:

        if cv2.contourArea(c) < 100:
            continue
        
        x, y, w, h = cv2.boundingRect(c)

        cv2.rectangle(frm, (x,y), (x+w,y+h), (0,255,0), 2)
        xcen = int((x+(x+w))/2)
        ycen = int((y+(y+h))/2)
        cv2.circle(frm, (xcen, ycen), 3, (0,0,255), 3)
    
    cv2.imshow('msk', msk)
    cv2.imshow('og', frm)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
                                
cv2.destroyAllWindows()
vid.release()
