from time import time


def log(message):
    print("[{}] {}".format(time.strftime(
        "%Y-%m-%d %H:%M:%S", time.time()), message))
