import praw
import re
import yaml
import string
import random
import urllib.request as req

with open("config.yaml") as file:
    config = yaml.load(file.read())

rd_config = config["reddit"]

reddit = praw.Reddit(client_id=rd_config["client_id"],
                    client_secret=rd_config["client_secret"],
                    password=rd_config["password"],
                    user_agent=rd_config["user_agent"],
                    username=rd_config["username"])

sub = reddit.subreddit(config["subreddit"])

clips = []

translator = str.maketrans(" ", "+")

search_query = "flair:{} site:gfycat.com".format(config["flair"].translate(translator))

for result in sub.search(search_query, time_filter=config["time_filter"], sort="top"):
    clips.append(result.url)


for i in range(config["clips"]):

    print("Downloading Clips {}/{}".format(i+1, config["clips"]))

    clip = req.urlopen(clips[i])

    exp = re.compile(r"https://giant.gfycat.com/\S*\.mp4")
    video_link = exp.findall(clip.read().decode("utf-8"))

    video = req.urlopen(video_link[0])

    with open("{}/video{}.mp4".format(config["workdir"], i), "wb") as file:
        file.write(video.read())
