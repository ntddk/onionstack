#!/usr/bin/env python
#coding: utf-8

import sys
import os
import hashlib

def md5(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return hashlib.md5(data).hexdigest()

filenames = os.listdir(sys.argv[1])
for filename in sorted(filenames):
    if md5(filename) != md5('blank.png') and md5(filename) != md5('blank2.png') and md5(filename) != md5('404.png') :
        print filename[0:16]

