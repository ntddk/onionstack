#!/usr/bin/env python
#coding: utf-8

import argparse
import os
import hashlib
import shutil
import time
from selenium import webdriver
service_args = [ 
            # Do not insert blank to each of args.
            '--proxy=127.0.0.1:9050',
            '--proxy-type=socks5'
        ]
dcap = {
        'phantomjs.page.settings.userAgent': 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0'
}
import tweepy
from tweepy import *

parser = argparse.ArgumentParser(description='@onionstack')
parser.add_argument('--config', '-c',
        help = 'path_to_config')
parser.add_argument('--list', required = True,
        help = 'path_to_list')
parser.add_argument('--log',
        help = 'path_to_log')
parser.add_argument('--skin', '-s', action = 'store_true',
        help = 'Repaint skins')
args = parser.parse_args()

def get_oauth():
    with open(args.config, 'rb') as f:
        data = f.read()
    f.close
    lines = data.split('\n')
    consumer_key = lines[0]
    consumer_secret = lines[1]
    access_key = lines[2]
    access_secret = lines [3]
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return auth

def get_title_with_screenshot(url):
    driver = webdriver.PhantomJS(service_args = service_args, desired_capabilities = dcap)
    driver.set_window_size(1024, 512)
    driver.get('http://' + url + '.onion') # 'http://' is required.
    driver.save_screenshot(url + '.png')
    title = driver.title
    driver.close()
    return title

def md5(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return hashlib.md5(data).hexdigest()

def repaint_skin(filename):
    import cv2
    shutil.copy(filename, filename + '.bak')
    frame = cv2.imread(filename)
    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l = np.array([0, 50, 80], dtype = "uint8")
    u = np.array([23, 255, 255], dtype = "uint8")
    skin_area = cv2.inRange(HSV, l, u)
    not_skin_area = cv2.bitwise_not(frame, frame, mask = skin_area)
    cv2.imwrite(filename, not_skin_area)    

def tweet(url, title):
    message = title + ' ' + 'http://' + url + '.onion'
    try:
        api.update_with_media(url + '.png', status = message) 
    except TweepError as e:
        pass

def log(url, title):
    message = title + '\t' + 'http://' + url + '.onion\n'
    f.write(message.encode('utf-8'))

if args.config:
    auth = get_oauth()
    api = tweepy.API(auth)

f = open(args.list, 'r')
line = f.readlines()
f.close()

if args.log:
    f = open(args.log, 'a')


for i in line:
    url = i.rstrip('\n')
    filename = url + '.png'
    if not os.path.isfile(filename):
        title = get_title_with_screenshot(url)
        print title + '\t' + 'http://' + url + '.onion'
        if args.skin:
            repaint_skin(filename)
        if md5(filename) != md5('images/blank.png') and md5(filename) != md5('images/blank2.png') and md5(filename) != md5('images/404.png') :
            if args.config:
                tweet(url, title)
            if args.log:
                log(url, title)

if args.log:
    f.close()

