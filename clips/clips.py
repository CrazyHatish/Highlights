import yaml
from functions import download, concat, delete

if __name__ == "__main__":
    with open("config.yaml") as file:
        config = yaml.load(file.read())

    if config["download"]:
        download(config)

    if config["concatenate"]:
        concat(config)

    if config["delete"]:
        delete(config)
