"""" restart miner when gpu is low usage and kill miner if already running
"""

import GPUtil as gpu
import time
import psutil

def checkgpu():
    card = gpu.getGPUs()
    isavailable = gpu.getAvailability(card, maxLoad=.6)
    print(time.ctime())
    if isavailable == [1]:
        print("can mine")
        time.sleep(5)
        return 'isavailable'

    if isavailable == [0]:
        print("cant mine")
        time.sleep(5)
        return 'notavailable'



def findProcessIdByName(processName):

    listOfProcessObjects = []

    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            # Check if process name contains the given name string.
            if processName.lower() in pinfo['name'].lower():
                listOfProcessObjects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return listOfProcessObjects;


def checkminer():
    minercheck = findProcessIdByName('ccminer.exe')
    if minercheck == []:
        return 'notrunning'
    else:
        return "running"




while True:
    gpus = checkgpu()
    miner = checkminer()
    if gpus is 'isavailable' and miner is 'notrunning':
        print('can start miner')
    else:
        print('cant start miner')






