# **VCS**

The project VCS is developed with the intent to help users access analyzed data from traffic cam
footage. This script will greatly mitigate the manual work of the user. It handles the objects moving in
the subject video and records it if it crosses a line drawn in the frame across the road. The user inputs
the video file and the time and date information of when the video is from, then the script analyses the
video and creates a foreground mask using absolute difference of the frames and then uses centroid
tracking algorithm to track the objects to the line above mentioned then the objects are recorded into
the list if the centroid crosses the line, then as the script is closing the plotter module enters the vehicle
count to a text file.

## Modules
### Analyse module

OpenCV (Centroid algorithm)

Images are breaked down to sections and are ranked using tags, then the section with most
tags as an object is deemed as an object. Tracking is achieved by associating target objects in
sequential frames of a video. This association can be very hard to accomplish when the objects are
moving fast in relation to the frame rate of the video. Things get even more complicated when
tracked objects change their orientation over time. In this scenario, video tracking systems normally
use a motion model which details how the image of the target might look for several possible
orientations of the object. The centroid tracking algorithm assumes that we are passing in a set of
bounding box (x, y)-coordinates for each detected object in every single frame, Once we have the
bounding box coordinates we must compute the “centroid”, or more simply, the center (x, y)-
coordinates of the bounding box., unique identities are assigned it is done for each frame of the
video, then we measure Euclidean distance between centroids, then closest pairs are deemed to be
of same unique id, The primary assumption of the centroid tracking algorithm is that a given object
will potentially move in between subsequent frames, but the distance between the centroids for
frames and will be smaller than all other distances between objects. then we register new objects
and de register old objects

```python
def analyse():
    vid = cv2.VideoCapture(lst2[0])

    ret, fr1 = vid.read()

    

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
        counter(frm, cnt)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    plotter(cnt)
    #cv2.imshow('mask',msk)
    #cv2.imshow('threshould',thresh)                       
    cv2.destroyAllWindows()
    vid.release()
```
### Counting

Vehicles are counted when they leave the frame or cross a line at an exit point of the frame.
Using a counting line makes it easier to count vehicles moving in a certain direction

```python
def counter(frame, count):
    cv2.putText(frame, "Vehicle Counter :"+ str(count), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5)
    cv2.line(frame, (25, count_line_pos), (1200, count_line_pos), (0,127,255), 3)
    cv2.imshow('video output', frame)
```

### Plotting

When the script exits the loop, the result file(/result.txt) is opened and the result list element is
appended.

```python
def plotter(count):
    print("Vehicle Counter :" + str(count))
    h= open("result.txt", "a")
    h.write("\n"+"Vehicle Count :" + str(count))
```

## Software requirements
- Python 
- Tkinter (Python Library)
- OpenCV (Python Library)

> vcs.py is the final script that i am satisfied with. other files makes use of other opecv functions like MOG2 subtractor on v2.py, v4.py uses the cars.xml file using the cv2.CascadeClassifier() function.

