"""" restart miner when gpu is low usage and kill miner if already running
"""

import GPUtil as gpu
import time
import psutil
from subprocess import CREATE_NEW_CONSOLE

gameList = []

def checkgpu():
    card = gpu.getGPUs()
    isavailable = gpu.getAvailability(card, maxLoad=.6)
    print(time.ctime())
    if isavailable == [1]:
        print("can mine")
        time.sleep(5)
        return 'isavailable'

    if isavailable == [0]:
        print("gpu in use")
        gpu.showUtilization()
        time.sleep(500)

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
    return listOfProcessObjects


def checkminer():
    minercheck = findProcessIdByName('ccminer.exe')
    if minercheck == []:
        return 'notrunning'
    else:
        return "running"


def killminer():
    miner = findProcessIdByName('ccminer.exe')
    pid = miner[0]['pid']
    psutil.Process(pid).kill()
    print('killed miner')


def startminer():
    psutil.Popen(['E:/downloads/ccminer.bat'], creationflags=CREATE_NEW_CONSOLE)


"""def log(x):
    with open('C:/Users/Death/Documents/logs/gpulog.csv', 'a') as f:
        f.write(str(time.ctime()) + '\n' + x + '\n')
        f.close()
"""
curTime = time.time()
while True:
    
    gpus = checkgpu()
    miner = checkminer()
    usage = str(gpu.showUtilization())
    #log(str(gpu.showUtilization()))
   
    if gpus is 'isavailable' and miner is 'notrunning':
        print('starting miner')
        startminer()
        time.sleep(120)
    
    if gpus is 'isavailable' and miner is 'running':
        killminer()
        time.sleep(30)
    
    if time.time() - curTime > 100:
        killminer()
        print('restarting')
        curTime = time.time()
        time.sleep(10)


##TODO:check for games running  probably best way is to make a list of all games and check against list
