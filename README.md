# Simple Object Tracking

## The video

I wasn’t able to find data specifically for a warehouse setting with forklifts and people to track so I imagine a car park setting would be a good substitute for now. I created a layout from the video to map the path of the object. For simplicity, I decided to track one object alone.

## Stages

- Detection
- Tracking
- Mapping

## Detection

Can be done using any object detection algorithm and we can get the centroid of the object we want to track. But since my main goal was to learn object tracking I’ve just left it for the user to do this part by selecting the object to track.


## Tracking

Using optical flow. Here, given two subsequent frames, we have to estimate the apparent motion field between them assuming consistent brightness, and similar motion between neighbouring pixels.

**Sparse optical flow** - Computing optical flow for a sparse feature set.

**Dense optical flow** - Computing optical flow for all the points in the frame.

### The math:

- **Pixel in first frame:** _I(x,y,t)_
- **Pixel moves by distance:** _(dx,dy)_
- **In the next frame after time:** _dt_
- _I(x,y,t)=I(x+dx,y+dy,t+dt)_

Taylor series approximation on RHS gives us an equation with two unknown variables. One of the methods to solve this is Lucas-Kanade. This method takes a 3x3 patch around the point and finds the constants for these 9 points. Least square fit method gives two equation-two unknown problem.

**Pyramids** - So far we deal with small motions. To deal with large motion, we go up in the pyramid and small motions are removed and large motions become small motions.


## Mapping

Mapping is basically to project the real space onto a 2D plane. Sort of like a bird’s eye view. I believe this will be useful for the system, with a layout of the warehouse. 

## Result


https://user-images.githubusercontent.com/73516876/169666457-a5ff357e-e54c-4df4-bf25-cd865139458d.mp4

## References

1. https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html
2. https://en.wikipedia.org/wiki/Optical_flow
3. https://en.wikipedia.org/wiki/Lucas%E2%80%93Kanade_method
4. https://youtu.be/4F5ZiNBxqOY
5. https://zbigatron.com/mapping-camera-coordinates-to-a-2d-floor-plan/
