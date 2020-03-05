"""" restart miner when gpu is low usage and kill miner if already running
"""

import time
from subprocess import CREATE_NEW_CONSOLE
import GPUtil as gpu
import keyboard
import psutil

gameList = {"gears": "gears5.exe",
            "outer_worlds": "IndianaWindowsStore-Win64-Shipping.exe",
            "total_war": "Three_Kingdoms.exe",
            "poe": "PathOfExile_x64Steam"
            
}


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
    keyboard.press_and_release('alt+x') 
    psutil.Popen(['E:/downloads/ccminer.bat'], creationflags=CREATE_NEW_CONSOLE)


def checkgames():

    for i in gameList.values():
        print(i)
        game = findProcessIdByName(i)
        if game == []:
            print(i + ' is not running')


        else:
            print("game is running")
            print(i)
            miners = checkminer()
            if miners == 'running':
                killminer()
                keyboard.press_and_release('alt+y')

            return 'gamerunning'

            
        
           

"""def log(x):
    with open('C:/Users/Death/Documents/logs/gpulog.csv', 'a') as f:
        f.write(str(time.ctime()) + '\n' + x + '\n')
        f.close()
"""
curTime = time.time()
while True:
    checkgames()
    gpus = checkgpu()
    miner = checkminer()

    usage = str(gpu.showUtilization())
    #log(str(gpu.showUtilization()))
   
    if gpus is 'isavailable' and miner is 'notrunning':
        x = checkgames()
        if x != 'gamerunning':
            print('starting miner')
            startminer()
            time.sleep(12)
    
    if gpus is 'isavailable' and miner is 'running':
        killminer()
        time.sleep(30)
    
    if time.time() - curTime > 21600:
        killminer()
        print('restarting')
        curTime = time.time()
        time.sleep(10)


##TODO:check temp

#TODO: if no network kill and wait
