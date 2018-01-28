#!/usr/bin/python3
# coding=utf8
'''
zyzy blog
'''
import time
import os

DIR = "/tmp/posts"

class blog():
    """
    blog("hello").print_post()
    blog("hello",["tag1","你好"],"tttttitle").print_post()
    """
    def __init__(self, content, tags=["碎碎念"], title=None, filename=None):
        date = str(int(time.time()))
        self.content = content
        self.tags = tags
        self.date = date
        self.post = ""
        if title:
            self.title = title
        else:
            self.title = "_"
        if filename:
            self.filename = filename
        else:
            self.filename = date
        self.filename += ".md"
    
    def format_post(self):
        template = """___
title: {}
date: {}
tags: {}
---
{}"""
        self.post = template.format(self.title, self.date,
            str(self.tags).decode('string_escape'),
            self.content)

    def write_post(self):
        with open(os.path.join(DIR,self.filename),"w") as f:
            f.write(self.post)
    
    def print_post(self):
        self.format_post()
        print(self.post)

