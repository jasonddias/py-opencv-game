#!/usr/bin/env python2
#
# OpenCV Python reference: http://opencv2.cv.willowgarage.com/documentation/python/index.html

import cv2 as cv
import Key
import random
import cv2

class Target:
    """ Class representing the target """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.speed = (0,1)
        self.active = True

    def getDimensions(self):
        return (self.x, self.y, self.width, self.height)

    def centerOrigin(self):
        return (self.x - self.width/2, self.y - self.height/2)

    def update(self):
        self.x += self.speed[0]
        self.y += self.speed[1]

# Create windows to show the captured images
cv.namedWindow("window_a", cv2.cv.CV_WINDOW_AUTOSIZE)
cv.namedWindow("window_b", cv2.cv.CV_WINDOW_AUTOSIZE)

# Structuring element
es = cv2.cv.CreateStructuringElementEx(9,9, 4,4, cv2.cv.CV_SHAPE_ELLIPSE)

## Webcam settings
# Use default webcam.
# If that does not work, try 0 as function's argument
cam = cv2.cv.CaptureFromCAM(0)
# Dimensions of player's webcam
frame_size = (int(cv2.cv.GetCaptureProperty(cam, cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),int(cv2.cv.GetCaptureProperty(cam, cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

## Video settings
# Set to True if you want to record a video of the game
writeVideo = False
# Video format
fourcc = cv2.cv.FOURCC('M', 'J', 'P', 'G')
fps = 30
# Create video file
if writeVideo:
    video_writer = cv2.cv.CreateVideoWriter("movie.avi", fourcc, fps, frame_size)

previous = cv2.cv.CreateImage(frame_size, 8L, 3)
cv2.cv.SetZero(previous)

difference = cv2.cv.CreateImage(frame_size, 8L, 3)
cv2.cv.SetZero(difference)

current = cv2.cv.CreateImage(frame_size, 8L, 3)
cv2.cv.SetZero(current)

bola_original = cv2.cv.LoadImage("Aqua-Ball-Red-icon.png")
bola = cv2.cv.CreateImage((64,64), bola_original.depth, bola_original.channels)
cv2.cv.Resize(bola_original, bola)

mask_original = cv2.cv.LoadImage("input-mask.png")
mask = cv2.cv.CreateImage((64,64), mask_original.depth, bola_original.channels)
cv2.cv.Resize(mask_original, mask)

def hit_value(image, target):
    roi = cv2.cv.GetSubRect(image, target.getDimensions())
    return cv2.cv.CountNonZero(roi)
counts=5
def create_targets(count):
    targets = list()
    for i in range(count):
        tgt = Target(random.randint(0, frame_size[0]-bola.width), 0)
        tgt.width = bola.width
        tgt.height = bola.height
        targets.append(tgt)

    return targets

nbolas = 5
targets = create_targets(nbolas)

initialDelay = 100

score = 0

font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1)

# capture - original footage
# current - blurred footage
# difference - difference frame
# frame - difference frame gray scaled > threshold > dilate | working image
# bola_original - imagem da bola
# bola - imagem da bola menor
# mask_original - imagem da mascara
# mask - imagem da mascara menor
# Main loop
while True:
    # Capture a frame
    capture = cv2.cv.QueryFrame(cam)
    cv2.cv.Flip(capture, capture, flipMode=1)

    # Difference between frames
    #cv2.cv.Smooth(capture, current, cv2.cv.CV_BLUR_NO_SCALE,15, 15);
    #cv2.cv.Smooth(capture, current, cv2.cv.CV_BLUR_NO_SCALE, 3, 3); 

    cv2.cv.Smooth(capture, current, cv.cv.CV_BLUR, 15,15)
    #cv2.cv.Smooth(capture, current,  cv.cv.CV_GAUSSIAN, 15,15)
    cv2.cv.AbsDiff(current, previous, difference)

    frame = cv2.cv.CreateImage(frame_size, 8, 1)
    cv2.cv.CvtColor(difference, frame, cv2.cv.CV_BGR2GRAY)
    cv2.cv.Threshold(frame, frame, 10, 0xff, cv2.cv.CV_THRESH_BINARY)
    cv2.cv.Dilate(frame, frame, element=es, iterations=3)

    if initialDelay <= 0:
        for t in targets:
            if t.active:
                nzero = hit_value(frame, t)
                if nzero < 1000:
                    # Draws the target to screen
                    cv2.cv.SetImageROI(capture, t.getDimensions())
                    cv2.cv.Copy(bola, capture, mask)
                    cv2.cv.ResetImageROI(capture)
                    t.update()
                    # If the target hits the bottom
                    if t.y + t.height >= frame_size[1]:
                        t.active = False
                        nbolas -= 1
                else:
                    t.y = 0
                    t.x = random.randint(0, frame_size[0]-bola.width)
                    if t.speed[1] < 15:
                        t.speed = (0, t.speed[1]+1)
                    score += nbolas

    cv2.cv.PutText(capture, "Score: %d" % score, (10,frame_size[1]-10), font, cv2.cv.RGB(0,0,0))
    cv2.cv.ShowImage("window_a", frame)
    if writeVideo:
        cv2.cv.WriteFrame(video_writer, capture)
    cv2.cv.ShowImage("window_b", capture)

    previous = cv2.cv.CloneImage(current)

    # Exit game if ESC key is pressed
    c = cv2.waitKey(2)
    if c == 27:
        break

    initialDelay -= 1

print score
