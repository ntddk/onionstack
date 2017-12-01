#!/usr/bin/env python
#coding: utf-8

import glob
list = glob.glob('./images/*.png')

for i in list:
    print "<div class=\"item\"><img data-original=\"images/" + i[9:]  + "\" src=\"images/loading.svg\" alt=\"" + i[9:25] + ".onion\" width=100%><a href=\"http://" + i[9:25] + ".onion\">" + i[9:25] + ".onion</a></div>"
