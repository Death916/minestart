"""" restart miner when gpu is low usage and kill miner if already running
"""

import GPUtil as gpu
import time


def isavailable():
    card = gpu.getGPUs()
    isAvailable = gpu.getAvailability(card, maxLoad=.6)

    if isAvailable == [1]:
        print("can mine")
        print(time.ctime())
        time.sleep(1)

    if isAvailable == [0]:
        print("cant mine")
        print(time.ctime())
        time.sleep(1)
    return isAvailable

while True:

    isavailable()



