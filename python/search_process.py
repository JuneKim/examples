import psutil

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName
    '''
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print ("exception")
            pass
    return False

if checkIfProcessRunning('chrome'):
    print ("Yes a chrome process was running")
else:
    print ("No chrome process was running")


