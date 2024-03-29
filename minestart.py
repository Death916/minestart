"""" restart miner when gpu is low usage and kill miner if already running
"""

import time
from subprocess import CREATE_NEW_CONSOLE
import GPUtil as gpu
#import keyboard
import psutil
import sys
import os


gameList = {"gears": "gears5.exe",
            "outer_worlds": "IndianaWindowsStore-Win64-Shipping.exe",
            "total_war": "Three_Kingdoms.exe",
            "poe": "PathOfExile_x64Steam",
            "valorant": "VALORANT-Win64-Shipping.exe",
            "Fallout 76": "fallout76.exe",
            "Total War: Troy": "troy.exe"

}

try:
    firstminer = str(sys.argv[1])
except:
    
        
    firstminer = input('choose between "ccminer" or "nanominer" or "trex" exactly:  ')
    if firstminer  == "ccminer":
            pass
    elif firstminer == "nanominer":
            global curminer
            os.chdir('C:\\Users\\death\\Documents\\code\\Scripts\\nanominer-windows-1.10.0')
            curminer = "nanominer.exe"
    elif firstminer == "trex":
            os.chdir('C:\\Users\\death\\Documents\\code\\other\\t-rex-0.26.4-win')
            curminer = "t-rex.exe"
            pass
    #TODO: add error handling for invalid input
    #TODO: clean up code above with some type of dict lookup or soemthing
    
miners = ['ccminer.exe', 'nanominer.exe']



def checkgpu():
    '''check gpu availability and utilization'''
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
    """helper function to find miner exe"""
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
    """check if miner is already running"""
    for miner in miners:
        minercheck = findProcessIdByName(miner)
        
    if minercheck == []:
        print('miner not running')
        return 'notrunning'
    else:
        print('miner running')
        print(miner)
        return "running"
    



def killminer(miner):
    minerkill = findProcessIdByName(miner)
    pid = minerkill[0]['pid']
    psutil.Process(pid).kill()
    print('killed miner')


def startminer():
    keyboard.press_and_release('alt+x') 
    psutil.Popen([curminer], creationflags=CREATE_NEW_CONSOLE)


# noinspection PySimplifyBooleanCheck
def checkgames():
    """check if games in game list are running and kill miner if found"""
    for i in gameList.values():
        game = findProcessIdByName(i)
        if game == []:
            print(i + ' is not running')

        else:
            print("game is running")

            miners = checkminer()
            if miners == 'running':
                killminer(curminer)


            return 'gamerunning'

def check_evga():
    evga = findProcessIdByName('PrecisionX_x64.exe')
    if evga == []:
        print('evga not running')
        psutil.Popen(['E:/Precision X1/PrecisionX_x64.exe'], shell=True)
        evga = findProcessIdByName('PrecisionX_x64.exe')
        if evga:
            print('evga started')

def peak_hours():
    """check if peak hours are active"""
    if time.localtime().tm_hour in range(17, 20):
        print('peak hours')
        killminer(curminer)
        return 'peak'
    else:
        print('off peak')
        return 'offpeak'

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
    check_evga()

    usage = str(gpu.showUtilization())
    #log(str(gpu.showUtilization()))

    if gpus == 'isavailable' and miner == 'notrunning':
        x = checkgames()
        if x != 'gamerunning':
            print('starting miner')
            #keyboard.press_and_release('alt+x')
            startminer()
            time.sleep(12)

    if gpus == 'isavailable' and miner == 'running':
        killminer(miner) 
        #keyboard.press_and_release('alt+y')
        time.sleep(30)

    if time.time() - curTime > 21600:
        if miner: #dont run if miner not running
            killminer(miner)
        print('restarting')
        curTime = time.time()
        time.sleep(10)


#TODO:check temp
#TODO: if no network kill and wait
#TODO: test check_evga(), get to work with uac on
#TODO: make sure evga goes to 100 when game starts
#TODO: log
#TODO: maybe make gui ???? maybe just exe
