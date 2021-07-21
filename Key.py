#!/usr/bin/env python2

import cv2 as cv

# ESC = 1048603
ESC = 27

def WaitKey(delay = 0):
    c = cv.WaitKey(delay)
    if c == -1:
        ret = -1
    else:
        ret = c & ~0b100000000000000000000 

    return ret

if __name__ == '__main__':
    cv.cv.NamedWindow("janela", cv.CV_WINDOW_AUTOSIZE)

    cv.cv.ShowImage("janela", None)
    c = cv.cv.WaitKey()
    print "%d - %d" % (c & ~0b100000000000000000000,c)
