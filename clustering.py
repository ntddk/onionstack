#!/usr/bin/env python
#coding: utf-8

import sys
import glob
import cv2
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans
import os
import shutil

n_clusters = int(sys.argv[1])
list = glob.glob('./images/*.png')

def main():
    features = []

    for i in list:
        im = cv2.imread(i)
        hist, bins = np.histogram(im.ravel(), 256, [0, 256])
        features.append(hist)

    lsa = TruncatedSVD(10)
    features = lsa.fit_transform(features)
    features = Normalizer(copy = False).fit_transform(features)

    km = KMeans(
        init='k-means++',
        n_clusters=n_clusters,
    )
    km.fit(features)

    for i in range(n_clusters):
        if not os.path.exists('./result/' + str(i)):
            os.makedirs('./result/' + str(i))

    cnt = 0

    for i in list:
        filename = i.split('/')[-1]
        print filename,
        print km.labels_[cnt]
        shutil.copyfile(i, './result/' +  str(km.labels_[cnt]) + '/' + filename)
        cnt += 1

if __name__ == '__main__':
    main()

