import os

def clear(): 
    # check and make call for specific operating system 
    if os.name =='posix':
        os.system('clear')
    else:
        os.system('cls') 