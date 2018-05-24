import os
import random
import re
import urllib.request as req

import praw
import yaml
from moviepy.editor import VideoFileClip, concatenate_videoclips


def download(config):
    rd_config = config["reddit"]

    reddit = praw.Reddit(
        client_id=rd_config["client_id"],
        client_secret=rd_config["client_secret"],
        password=rd_config["password"],
        user_agent=rd_config["user_agent"],
        username=rd_config["username"],
    )

    sub = reddit.subreddit(config["subreddit"])

    clips = []

    translator = str.maketrans(" ", "+")

    search_query = (
        f"flair:{config['flair'].translate(translator)} site:twitch.tv OR site:gfycat.com"
    )

    for result in sub.search(
        search_query, time_filter=config["time_filter"], sort="top"
    ):
        clips.append(result.url)

    if config["order"] == "random":
        random.shuffle(clips[: config["clips"]])
    elif config["order"] == "reverse":
        clips = clips[config["clips"] : 0 : -1]
    else:
        clips = clips[: config["clips"]]

    if not os.path.exists(config["workdir"]):
        os.makedirs(config["workdir"])

    for i in range(config["clips"]):
        print(f"Downloading Clips {i + 1}/{config['clips']}")

        clip = req.urlopen(clips[i])

        if "twitch" in clips[i]:
            exp = re.compile(r"\[\{\"quality\".{16,17}\"(https://[^,]*)\"")
        elif "gfycat" in clips[i]:
            exp = re.compile(r"https://giant.gfycat.com/\S*\.mp4")

        video_link = exp.findall(clip.read().decode("utf-8"))
        video = req.urlopen(video_link[0])

        with open(f"{config['workdir']}/video{i}.mp4", "wb") as file:
            file.write(video.read())


def concat(config):
    saved_clips = []

    for i in range(config["clips"]):
        saved_clips.append(
            VideoFileClip(
                f"{config['workdir']}/video{i}.mp4",
                target_resolution=config["resolution"],
            )
        )

    if not os.path.exists("output"):
        os.makedirs("output")

    final_clip = concatenate_videoclips(saved_clips)
    final_clip.write_videofile(f"output/{config['filename']}", fps=config["fps"])


def delete(config):
    for i in range(config["clips"]):
        os.remove(f"{config['workdir']}/video{i}.mp4")


if __name__ == "__main__":
    with open("config.yaml") as file:
        config = yaml.load(file.read())

    if config["download"]:
        download(config)

    if config["concatenate"]:
        concat(config)

    if config["delete"]:
        delete(config)
