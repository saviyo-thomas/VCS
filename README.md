# VCS
Project to write a program to count number of cars from a video input.

## Modules
### Analyse module
>  OpenCV (Centroid algorithm) 
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
### Plotting
