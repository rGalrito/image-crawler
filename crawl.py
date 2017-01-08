#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-
#
# This program will download all images from one thread
#
# Folder path is *dateinseconds* - *title*
#
# Rafael Galrito, 27 March 2016
#
#

import time
import requests
import os
import sys
from bs4 import BeautifulSoup


class Crawl():
    path = ""

    def create_dir_name(self):
        return str(time.strftime("%y%m%d%H%M%S"))

    def save_on_dir(self, title):
        try:
            self.path += " - " + str(title)
            if not os.path.exists(self.path):
                os.makedirs(self.path)
                return self.path
        except Exception as e:
            print("e")

    def save_image(self, img):
        file_name = img.url
        last_char = file_name[::-1].find("/")
        file_name = file_name[len(file_name) - last_char:]
#        print "self.path", self.path
#        print "filename", file_name
        save_path_file_name = self.path + "/" + str(file_name)
        f = open(save_path_file_name, 'wb')
        f.write(img._content)
        f.close()

    def get_image(self, url):
        if not url.startswith("https://i.4") and not url.startswith("https://is.4"):
            return
#        purl = url.replace("s.", ".")
        req = requests.get(url)
        self.save_image(req)

    def get(self, url):
        print("Sending request for", url)

        req = requests.get(url)
        first_slash = url[::-1].find("/")

        title = url[-first_slash::]
        self.save_on_dir(title)

        print("Path name is", self.path)
        soup = BeautifulSoup(req.text, "lxml")
        all_images = soup.findAll('img')
        for r in all_images:
            print("(", all_images.index(r) + 1, "/", len(all_images), ")")
            try:
                rurl = "https:" + r.previous_element['href']
            except:
                print("This image couldn't be downloaded")
                continue
            self.get_image(rurl)

    def __init__(self):
        self.path = self.create_dir_name()


def has_arguments():
    if len(sys.argv) > 1:
        if len(sys.argv) == 2:
            print(sys.argv[1])
            c = Crawl()
            c.get(sys.argv[1])
        else:
            print("One argument is not more than one!")
    elif len(sys.argv) == 1:
        print("paste an url")

has_arguments()
