import time

def loadFast(x,y):
    for i in range (0,x):  
        b = "Loading" + "." * i
        print (b, end="\r")
        time.sleep(y)

def loadClean(x,y):
    for i in range (0,x):  
        b = '['+ (i*'*')+((x-i)*'.') +']'
        print (b, end="\r")
        time.sleep(y)