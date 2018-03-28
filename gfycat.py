import praw
import re
import yaml
import string
import random
import urllib.request as req

url = "https://gfycat.com/SpiritedIllegalDrafthorse"

html = req.urlopen(url).read().decode('utf-8')

exp = re.compile(r"https://giant.gfycat.com/\S*\.mp4")
links = exp.findall(html)[0]

with open("video.mp4", "wb") as file:
    video = req.urlopen(links)
    file.write(video.read())
