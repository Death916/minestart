"""" restart miner when gpu is low usage and kill miner if already running
"""

import GPUtil as gpu
import time


def checkgpu():
    card = gpu.getGPUs()
    isavailable = gpu.getAvailability(card, maxLoad=.6)

    if isavailable == [1]:
        print("can mine")
        print(time.ctime())
        time.sleep(1)

    if isavailable == [0]:
        print("cant mine")
        print(time.ctime())
        time.sleep(1)
    return isavailable

def checkminer():


while True:

    isavailable()



