#!/usr/bin/env python
#coding: utf-8

import sys
import glob
import cv2

list = glob.glob('./images/*.png')

def main():
    target_im = cv2.imread(sys.argv[1])
    target_hist = cv2.calcHist([target_im], [0], None, [256], [0, 256])

    for i in list:
        comparing_im = cv2.imread(i)
        comparing_hist = cv2.calcHist([comparing_im], [0], None, [256], [0, 256])
        diff = cv2.compareHist(target_hist, comparing_hist, 0)
        if diff > float(sys.argv[2]):
            print i,
            print diff
                
if __name__ == '__main__':
    main()
