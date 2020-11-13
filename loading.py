import time

def loadFast(x,y):
    for x in range (0,7):  
        b = "Loading" + "." * x
        print (b, end="\r")
        time.sleep(0.4)

def loadClean(x,y):
    for i in range (0,x):  
        b = '['+ (i*'*')+((x-i)*'.') +']'
        print (b, end="\r")
        time.sleep(y)