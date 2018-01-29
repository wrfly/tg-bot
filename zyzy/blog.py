#!/usr/bin/python3
# coding=utf8
'''
zyzy blog
'''

import time
import os
import subprocess
from shutil import copyfile

HUGO_SITE_DIR = "/root/Documents/i.kfd.me"
POST_DIR = os.path.join(HUGO_SITE_DIR, "content")
IMG_DIR = os.path.join(HUGO_SITE_DIR, "static/img")

class blog():
    """
    blog("hello").print_post()
    blog("hello",["tag1","你好"],"tttttitle").print_post()
    """
    def __init__(self, content, tags=None, title=None, image=None):
        date = str(int(time.time()))
        self.content = content
        self.image = image
        if tags:
            self.tags = tags
        else:
            self.tags = ["碎碎念"]
        self.date = date
        self.post = ""
        if title:
            self.title = title
        else:
            self.title = "_"
        self.filename = date+".md"
    
    def format_post(self):
        template = """---
title: {}
date: {}
tags: {}
---
{}"""
        self.content = self.content
        self.content = self.content.replace("\n\n", "#N#")
        self.content = self.content.replace("\n", "<br />")
        self.content = self.content.replace("#N#", "\n\n")
        if self.image:
            new_path = os.path.join(IMG_DIR, self.date+".jpg")
            copyfile(self.image, new_path)
            img_path = "/img/"+self.date+".jpg"
            self.content = "![{}]({})\n\n".format(self.date, img_path) \
                + self.content
        self.post = template.format(self.title, self.date,
            self.tags,
            # str(self.tags).decode('string_escape'),
            self.content)

    def write_post(self):
        self.format_post()
        with open(os.path.join(POST_DIR, self.filename),"w") as f:
            f.write(self.post)
        # hugo -s /root/Documents/i.kfd.me
        subprocess.call(["hugo", "-s", HUGO_SITE_DIR])
    
    def print_post(self):
        self.format_post()
        print(self.post)

