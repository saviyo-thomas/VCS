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

### Counting

Vehicles are counted when they leave the frame or cross a line at an exit point of the frame.
Using a counting line makes it easier to count vehicles moving in a certain direction

### Plotting

When the script exits the loop, the result file is opened and the result list element is
appended.

### Software requirements
- Python 
- Tkinter (Python Library)
- OpenCV (Python Library)
